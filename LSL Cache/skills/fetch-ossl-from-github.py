#!/usr/bin/env python3
# Skill: fetch-ossl-from-github
# Version: 0.2.0.0
# Purpose: Generate OSSL docs from the OpenSim GitHub repository source files
# Usage: python3 fetch-ossl-from-github.py [--force] [--dry-run]
# Created: 2026-03-18
# Last modified: 2026-03-19

"""
Fetches two C# source files from the opensim/opensim GitHub repository and
generates OSSL function documentation from them — no wiki required:

  IOSSL_Api.cs  — function signatures + //ApiDesc descriptions
  OSSL_Api.cs   — CheckThreatLevel() calls for per-function threat levels

Cross-references local kwdb.xml and makopo/tooltipdata.json for extra metadata
(parameter names, energy cost, forced delay) where available.

Output: one .md file per OSSL function in lsl-docs/ossl/
Updates cache-manifest.json sections.ossl = true on success.
"""

import io
import json
import os
import re
import ssl
import sys
import urllib.request
from datetime import date
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# ── Config ─────────────────────────────────────────────────────────────────────

_env_base     = os.environ.get("LSL_CACHE_BASE", "").strip()
CACHE_ROOT    = Path(_env_base) if _env_base else Path(__file__).resolve().parents[1]
DOCS_DIR      = CACHE_ROOT / "lsl-docs"
OSSL_DIR      = DOCS_DIR / "ossl"
MANIFEST_PATH = CACHE_ROOT / "cache-manifest.json"
CHANGELOG     = DOCS_DIR / "CHANGELOG.md"
TODAY         = date.today().isoformat()

KWDB_PATH   = DOCS_DIR / "vscode-extension-data" / "kwdb" / "kwdb.xml"
MAKOPO_PATH = DOCS_DIR / "vscode-extension-data" / "makopo" / "tooltipdata.json"

GITHUB_RAW = "https://raw.githubusercontent.com/opensim/opensim/master"
IFACE_URL  = f"{GITHUB_RAW}/OpenSim/Region/ScriptEngine/Shared/Api/Interface/IOSSL_Api.cs"
IMPL_URL   = f"{GITHUB_RAW}/OpenSim/Region/ScriptEngine/Shared/Api/Implementation/OSSL_Api.cs"

FORCE   = "--force"   in sys.argv
DRY_RUN = "--dry-run" in sys.argv

OS_WIKI_BASE = "https://opensimulator.org/wiki/"

OSSL_DIR.mkdir(parents=True, exist_ok=True)


# ── HTTP ────────────────────────────────────────────────────────────────────────

_SSL_CTX = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
_SSL_CTX.check_hostname = False
_SSL_CTX.verify_mode    = ssl.CERT_NONE

HEADERS = {"User-Agent": "Mozilla/5.0 SLCode-cache-tool/1.0"}

def fetch_text(url: str, label: str = "") -> str:
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=60, context=_SSL_CTX) as resp:
            total = int(resp.headers.get("Content-Length") or 0)
            enc   = resp.headers.get_content_charset("utf-8")
            tag   = f"  Downloading {label or url.split('/')[-1]}"
            chunks, received = [], 0
            while True:
                chunk = resp.read(65536)
                if not chunk:
                    break
                chunks.append(chunk)
                received += len(chunk)
                kb = received // 1024
                if total:
                    pct = received * 100 // total
                    print(f"{tag}: {kb} KB / {total//1024} KB ({pct}%)", end="\r", flush=True)
                else:
                    print(f"{tag}: {kb} KB...", end="\r", flush=True)
            print(f"{tag}: {received//1024} KB — done.                    ", flush=True)
            return b"".join(chunks).decode(enc, errors="replace")
    except Exception as e:
        print(f"  [fetch error] {url}: {e}", flush=True)
        return ""


# ── C# → LSL type normalisation ────────────────────────────────────────────────

_TYPE_MAP = {
    "LSL_String":   "string",
    "LSL_List":     "list",
    "LSL_Key":      "key",
    "LSL_Integer":  "integer",
    "LSL_Float":    "float",
    "LSL_Rotation": "rotation",
    "LSL_Vector":   "vector",
    "LSL_Types.LSL_String":   "string",
    "LSL_Types.LSL_List":     "list",
    "LSL_Types.LSL_Key":      "key",
    "LSL_Types.LSL_Integer":  "integer",
    "LSL_Types.LSL_Float":    "float",
    "LSL_Types.LSL_Rotation": "rotation",
    "LSL_Types.LSL_Vector":   "vector",
    "bool":        "integer",
    "int":         "integer",
    "long":        "integer",
    "uint":        "integer",
    "double":      "float",
    "object":      "list",
    "Hashtable":   "list",
    "Object":      "list",
    "string":      "string",
    "float":       "float",
    "void":        "void",
}

def _norm_type(t: str) -> str:
    """Map a C# type to its canonical LSL equivalent."""
    return _TYPE_MAP.get(t, t)


# ── Parse IOSSL_Api.cs ─────────────────────────────────────────────────────────

# Matches:  //ApiDesc Some description text
#           ReturnType osFunctionName(Type param1, Type param2, ...);
_APIDESC_RE = re.compile(
    r'//ApiDesc\s+(.+?)\r?\n\s+'
    r'([\w<>\[\]]+(?:\s*\[\])?)\s+'      # return type
    r'(os\w+)\s*\(([^)]*)\)\s*;',        # name + params
    re.MULTILINE,
)

# Fallback: pick up any public method starting with os that has no ApiDesc
_METHOD_RE = re.compile(
    r'(?:^|\n)\s+([\w<>\[\]]+(?:\s*\[\])?)\s+(os\w+)\s*\(([^)]*)\)\s*;',
    re.MULTILINE,
)


def _parse_params(raw: str) -> list[tuple[str, str]]:
    """Parse a C# parameter list into [(type, name), ...] tuples with LSL types."""
    raw = raw.strip()
    if not raw:
        return []
    result = []
    for part in raw.split(","):
        part = part.strip()
        # strip ref/out/params modifiers
        part = re.sub(r'^(ref|out|params)\s+', '', part)
        tokens = part.split()
        if len(tokens) >= 2:
            param_name = re.sub(r'LSL_\w+', '', tokens[-1]).strip('_') or tokens[-1]
            result.append((_norm_type(tokens[-2]), param_name))
        elif len(tokens) == 1:
            result.append((_norm_type(tokens[0]), ""))
    return result


def parse_interface(src: str) -> dict[str, dict]:
    """
    Parse IOSSL_Api.cs.
    Returns dict: name -> {description, return_type, params: [(type, name)]}
    """
    funcs = {}

    for m in _APIDESC_RE.finditer(src):
        desc, ret, name, raw_params = m.group(1).strip(), m.group(2).strip(), m.group(3), m.group(4)
        funcs[name] = {
            "description": desc,
            "return_type": _norm_type(ret),
            "params":      _parse_params(raw_params),
        }

    # Fallback pass — pick up any os* method that didn't get an ApiDesc
    for m in _METHOD_RE.finditer(src):
        ret, name, raw_params = m.group(1).strip(), m.group(2), m.group(3)
        if name not in funcs:
            funcs[name] = {
                "description": "",
                "return_type": _norm_type(ret),
                "params":      _parse_params(raw_params),
            }

    return funcs


# ── Parse OSSL_Api.cs for threat levels ────────────────────────────────────────

_THREAT_RE = re.compile(
    r'CheckThreatLevel\s*\(\s*ThreatLevel\s*\.\s*(\w+)\s*,\s*"(os\w+)"'
)

def parse_threat_levels(src: str) -> dict[str, str]:
    """Returns dict: function_name -> threat_level_string"""
    return {m.group(2): m.group(1) for m in _THREAT_RE.finditer(src)}


# ── Load local supplementary sources ───────────────────────────────────────────

def _strip_html(html: str) -> str:
    text = re.sub(r"<[^>]+>", "", html)
    text = text.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
    text = text.replace("&quot;", '"').replace("&#160;", " ").replace("&nbsp;", " ")
    return re.sub(r"\s+", " ", text).strip()


def load_kwdb(path: Path) -> dict[str, dict]:
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8", errors="replace")
    funcs = {}
    for m in re.finditer(r"<function([^>]*)>(.*?)</function>", text, re.DOTALL):
        attrs, body = m.group(1), m.group(2)
        name_m = re.search(r'name="(os[A-Z]\w*)"', attrs)
        if not name_m:
            continue
        name = name_m.group(1)
        params = re.findall(r'<param\s+type="([^"]+)"\s+name="([^"]+)"', body)
        desc_m = re.search(r'<description[^>]*>(.*?)</description>', body, re.DOTALL)
        desc   = _strip_html(desc_m.group(1)).strip() if desc_m else ""
        if "TODO" in desc:
            desc = ""
        funcs[name] = {"params_named": params, "description": desc}
    return funcs


_DELAY_RE  = re.compile(r"([\d.]+)\s*Forced Delay",  re.IGNORECASE)
_ENERGY_RE = re.compile(r"([\d.]+)\s*Energy",         re.IGNORECASE)

def load_makopo(path: Path) -> dict[str, dict]:
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8", errors="replace"))
    result = {}
    for key, html in data.items():
        if not (key.startswith("os") and key[2:3].isupper()):
            continue
        delay_m  = _DELAY_RE.search(html)
        energy_m = _ENERGY_RE.search(html)
        plain = _strip_html(html)
        plain = re.sub(r"Function:\s*\w+\s+\w+\(.*?\)\s*;?\s*", "", plain)
        plain = re.sub(r"[\d.]+\s*Forced Delay[^,\n]*,?\s*", "", plain)
        plain = re.sub(r"[\d.]+\s*Energy[^,\n]*", "", plain)
        plain = re.sub(r"\s+", " ", plain).strip().strip(";, ")
        result[key] = {
            "description": plain if len(plain) > 5 else "",
            "delay":       delay_m.group(1)  if delay_m  else "",
            "energy":      energy_m.group(1) if energy_m else "",
        }
    return result


# ── Doc generation ──────────────────────────────────────────────────────────────

def _build_signature(name: str, ret: str, params: list[tuple[str, str]]) -> str:
    param_str = ", ".join(
        f"{t} {n}".strip() for t, n in params if t
    )
    return f"{ret} {name}({param_str})"


def _build_body(name: str, ret: str, params: list[tuple[str, str]],
                desc: str, delay: str, energy: str,
                threat: str, wiki_url: str) -> str:
    lines = []
    if desc:
        lines += [desc, ""]

    lines += ["## Syntax", "", "```lsl", _build_signature(name, ret, params), "```", ""]

    if params:
        lines += ["## Parameters", "", "| Type | Name |", "|------|------|"]
        for t, n in params:
            if t:
                lines.append(f"| `{t}` | `{n}` |")
        lines.append("")

    lines += ["## Return Value", "", f"`{ret}`", ""]

    meta = []
    if threat:
        meta.append(f"**Threat Level:** {threat}")
    if delay:
        meta.append(f"**Forced Delay:** {delay} seconds")
    if energy:
        meta.append(f"**Energy:** {energy}")
    if meta:
        lines += ["## Timing, Energy and Permissions", ""]
        lines += [f"- {item}" for item in meta]
        lines.append("")

    lines += [
        "## Notes",
        "",
        "- OSSL function — requires appropriate threat level in the region's OpenSim configuration.",
        f"- Reference: [{wiki_url}]({wiki_url})",
        "",
    ]
    return "\n".join(lines)


# ── Selective update helpers ────────────────────────────────────────────────────

# Sections regenerated from source on every --force run; all others are preserved
_AUTO_SECTIONS = {"Syntax", "Parameters", "Return Value", "Timing, Energy and Permissions"}

_PLACEHOLDER_RE = re.compile(r'^OSSL function:\s+\w+\.$')

_FM_RE = re.compile(r'^---\n(.*?)\n---\n', re.DOTALL)
_FM_FIELD_RE = re.compile(r'^(\w+):\s*(.*)', re.MULTILINE)


def _parse_fm(text: str) -> tuple[dict, str]:
    """Return (fields_dict, body_after_frontmatter). Values are unquoted strings."""
    m = _FM_RE.match(text)
    if not m:
        return {}, text
    fields = {}
    for fm in _FM_FIELD_RE.finditer(m.group(1)):
        fields[fm.group(1)] = fm.group(2).strip().strip('"')
    return fields, text[m.end():]


def _rebuild_fm(fields: dict) -> str:
    """Serialise front-matter dict back to YAML block."""
    key_order = [
        "name", "category", "type", "language", "description", "signature",
        "return_type", "threat_level", "energy_cost", "sleep_time",
        "wiki_url", "source", "first_fetched", "last_updated",
    ]
    lines = ["---"]
    seen = set()
    for k in key_order:
        if k in fields:
            lines.append(f'{k}: "{fields[k]}"')
            seen.add(k)
    for k, v in fields.items():
        if k not in seen:
            lines.append(f'{k}: "{v}"')
    lines.append("---\n")
    return "\n".join(lines)


def _split_sections(body: str) -> list[tuple[str, str]]:
    """Split markdown body into [(title, raw_text), ...].
    title="" for text before the first ## heading.
    raw_text includes the heading line itself.
    """
    parts = re.split(r'(?m)^(## [^\n]*\n?)', body)
    sections = []
    if parts[0]:
        sections.append(("", parts[0]))
    i = 1
    while i < len(parts) - 1:
        heading_text = parts[i].lstrip('#').strip()
        sections.append((heading_text, parts[i] + parts[i + 1]))
        i += 2
    return sections


def _merge_body(existing_body: str, new_body: str) -> str:
    """Replace auto-generated sections with fresh content; keep all others."""
    existing = _split_sections(existing_body)
    new_map  = {h: c for h, c in _split_sections(new_body) if h in _AUTO_SECTIONS}
    seen     = set()
    result   = []

    for heading, content in existing:
        if heading in _AUTO_SECTIONS:
            result.append(new_map.get(heading, content))
            seen.add(heading)
        else:
            result.append(content)

    # Append any new auto sections not already present
    for h, c in _split_sections(new_body):
        if h in _AUTO_SECTIONS and h not in seen:
            result.append(c)

    return "".join(result)


def save_doc(name: str, iface: dict, threats: dict,
             kwdb: dict, makopo: dict) -> bool:
    out_path = OSSL_DIR / f"{name}.md"

    ret    = iface.get("return_type", "void")
    params = iface.get("params", [])
    threat = threats.get(name, "")

    # Description: prefer ApiDesc, then kwdb, then makopo, then placeholder
    github_desc = (iface.get("description", "")
                   or kwdb.get(name, {}).get("description", "")
                   or makopo.get(name, {}).get("description", "")
                   or f"OSSL function: {name}.")

    # Parameter names: kwdb often has names where the interface only has types.
    # Strip any embedded LSL_ type fragments from kwdb param names (kwdb artifact).
    kwdb_params = kwdb.get(name, {}).get("params_named", [])
    if kwdb_params and len(kwdb_params) == len(params):
        params = [
            (iface_t or kwdb_t,
             re.sub(r'LSL_\w+', '', kwdb_n).strip('_') or kwdb_n)
            for (iface_t, _), (kwdb_t, kwdb_n) in zip(params, kwdb_params)
        ]

    delay  = makopo.get(name, {}).get("delay", "")
    energy = makopo.get(name, {}).get("energy", "")
    wiki   = OS_WIKI_BASE + name

    sig      = _build_signature(name, ret, params)
    new_body = _build_body(name, ret, params, github_desc, delay, energy, threat, wiki)

    desc_safe = github_desc.replace('"', '\\"').replace("\n", " ")[:300]
    sig_safe  = sig.replace('"', '\\"')

    if out_path.exists() and FORCE:
        # ── Selective update: preserve manual edits ─────────────────────────
        existing_text = out_path.read_text(encoding="utf-8", errors="replace")
        fields, existing_body = _parse_fm(existing_text)

        # Only clobber description if it's still a placeholder
        existing_desc = fields.get("description", "")
        if _PLACEHOLDER_RE.match(existing_desc):
            fields["description"] = desc_safe

        # Always update these from source
        fields.update({
            "signature":    sig_safe,
            "return_type":  ret,
            "threat_level": threat,
            "energy_cost":  energy,
            "sleep_time":   delay,
            "wiki_url":     wiki,
            "source":       "opensim/opensim GitHub (IOSSL_Api.cs)",
            "last_updated": TODAY,
        })
        # Ensure required fields exist for new-style files
        fields.setdefault("name",          name)
        fields.setdefault("category",      "function")
        fields.setdefault("type",          "function")
        fields.setdefault("language",      "OSSL")
        fields.setdefault("first_fetched", TODAY)

        merged_body = _merge_body(existing_body, "\n" + new_body)
        final_text  = _rebuild_fm(fields) + merged_body

        if not DRY_RUN:
            out_path.write_text(final_text, encoding="utf-8")
        return True

    elif not out_path.exists():
        # ── Fresh write ─────────────────────────────────────────────────────
        front = (
            f'---\n'
            f'name: "{name}"\n'
            f'category: "function"\n'
            f'type: "function"\n'
            f'language: "OSSL"\n'
            f'description: "{desc_safe}"\n'
            f'signature: "{sig_safe}"\n'
            f'return_type: "{ret}"\n'
            f'threat_level: "{threat}"\n'
            f'energy_cost: "{energy}"\n'
            f'sleep_time: "{delay}"\n'
            f'wiki_url: "{wiki}"\n'
            f'source: "opensim/opensim GitHub (IOSSL_Api.cs)"\n'
            f'first_fetched: "{TODAY}"\n'
            f'last_updated: "{TODAY}"\n'
            f'---\n'
        )
        if not DRY_RUN:
            out_path.write_text(front + "\n" + new_body, encoding="utf-8")
        return True

    # File exists, no --force
    return False


# ── Main ────────────────────────────────────────────────────────────────────────

print("Fetching OSSL docs from opensim/opensim GitHub repository...", flush=True)
print(f"  Interface:      {IFACE_URL}", flush=True)
print(f"  Implementation: {IMPL_URL}", flush=True)
print(flush=True)

iface_src = fetch_text(IFACE_URL, label="IOSSL_Api.cs")
if not iface_src:
    print("ERROR: Failed to fetch IOSSL_Api.cs — aborting.", flush=True)
    sys.exit(1)

impl_src = fetch_text(IMPL_URL, label="OSSL_Api.cs")
if not impl_src:
    print("WARNING: Failed to fetch OSSL_Api.cs — threat levels will be missing.", flush=True)

print(f"  Parsing interface file ...", flush=True)
iface_funcs = parse_interface(iface_src)
print(f"  Found {len(iface_funcs)} OSSL functions in IOSSL_Api.cs", flush=True)

threats = {}
if impl_src:
    print(f"  Parsing implementation file for threat levels ...", flush=True)
    threats = parse_threat_levels(impl_src)
    print(f"  Found {len(threats)} threat level declarations", flush=True)

print(f"  Loading local kwdb.xml ...", flush=True)
kwdb = load_kwdb(KWDB_PATH)
print(f"  {len(kwdb)} OSSL entries in kwdb" if kwdb else "  kwdb.xml not found — skipping", flush=True)

print(f"  Loading local makopo tooltipdata.json ...", flush=True)
makopo = load_makopo(MAKOPO_PATH)
print(f"  {len(makopo)} OSSL entries in makopo" if makopo else "  makopo not found — skipping", flush=True)

print(flush=True)

written = 0
skipped = 0

total_funcs = len(iface_funcs)
for i, (name, iface) in enumerate(sorted(iface_funcs.items()), 1):
    saved = save_doc(name, iface, threats, kwdb, makopo)
    if saved:
        written += 1
        if DRY_RUN:
            print(f"  [dry] would write: {name}.md", flush=True)
    else:
        skipped += 1
    print(f"  Writing docs: {i}/{total_funcs} ({name})...                    ", end="\r", flush=True)
print(flush=True)

print(flush=True)
if DRY_RUN:
    print(f"[DRY RUN] Would write {written} files, skip {skipped} existing.", flush=True)
else:
    print(f"Done: {written} files written, {skipped} skipped (already exist).", flush=True)

if written > 0 and not DRY_RUN:
    manifest = {}
    if MANIFEST_PATH.exists():
        try:
            manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        except Exception:
            pass
    manifest.setdefault("sections", {})["ossl"] = True
    manifest["last_updated"] = TODAY
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print("Cache manifest updated — sections.ossl = true", flush=True)

    try:
        with open(CHANGELOG, "a", encoding="utf-8") as f:
            f.write(
                f"\n## {TODAY} — OSSL docs from GitHub source\n"
                f"- Source: opensim/opensim IOSSL_Api.cs ({len(iface_funcs)} functions)\n"
                f"- Threat levels from OSSL_Api.cs ({len(threats)} entries)\n"
                f"- Cross-referenced kwdb ({len(kwdb)} entries) + makopo ({len(makopo)} entries)\n"
                f"- Generated {written} OSSL .md files in lsl-docs/ossl/\n"
                f"- Skipped {skipped} existing\n"
            )
    except Exception:
        pass
