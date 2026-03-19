#!/usr/bin/env python3
# Skill: generate-ossl-from-kwdb
# Version: 0.1.0.0
# Purpose: Generate OSSL function docs from locally cached kwdb.xml and makopo tooltipdata.json
# Usage: python3 generate-ossl-from-kwdb.py [--force] [--dry-run]
# Created: 2026-03-10
# Last modified: 2026-03-10

"""
Generates OSSL function documentation from two locally-cached sources — no web requests:

  1. ~/.lsl-cache/lsl-docs/vscode-extension-data/kwdb/kwdb.xml
     → authoritative function list, parameter types/names, return types

  2. ~/.lsl-cache/lsl-docs/vscode-extension-data/makopo/tooltipdata.json
     → human-readable descriptions, forced delay, energy cost, wiki URLs

  Cross-references both sources to produce complete YAML-fronted .md files
  in ~/.lsl-cache/lsl-docs/ossl/, one per OSSL function.

  Updates cache-manifest.json sections.ossl = true on completion.
"""

import io
import hashlib
import json
import os
import re
import sys
from datetime import date
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# ── Config ────────────────────────────────────────────────────────────────────

_env_base     = os.environ.get("LSL_CACHE_BASE", "").strip()
CACHE_ROOT    = Path(_env_base) if _env_base else Path(__file__).resolve().parents[1]
DOCS_DIR      = CACHE_ROOT / "lsl-docs"
OSSL_DIR      = DOCS_DIR / "ossl"
MANIFEST_PATH = CACHE_ROOT / "cache-manifest.json"
CHANGELOG     = DOCS_DIR / "CHANGELOG.md"
TODAY         = date.today().isoformat()

KWDB_PATH    = DOCS_DIR / "vscode-extension-data" / "kwdb" / "kwdb.xml"
MAKOPO_PATH  = DOCS_DIR / "vscode-extension-data" / "makopo" / "tooltipdata.json"

FORCE   = "--force"   in sys.argv
DRY_RUN = "--dry-run" in sys.argv

OS_WIKI_BASE = "https://opensimulator.org/wiki/"

OSSL_DIR.mkdir(parents=True, exist_ok=True)


# ── Parse kwdb.xml ────────────────────────────────────────────────────────────

def strip_html(html: str) -> str:
    text = re.sub(r"<[^>]+>", "", html)
    text = text.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
    text = text.replace("&quot;", '"').replace("&#160;", " ").replace("&nbsp;", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def parse_kwdb(path: Path) -> dict:
    """
    Parse kwdb.xml for OSSL functions.
    Returns dict: name -> {return_type, params: [(type, name), ...], description, grid}
    """
    text = path.read_text(encoding="utf-8", errors="replace")
    funcs = {}

    for m in re.finditer(r"<function([^>]*)>(.*?)</function>", text, re.DOTALL):
        attrs = m.group(1)
        body  = m.group(2)

        name_m = re.search(r'name="(os[A-Z]\w*|OSSL\w*)"', attrs)
        if not name_m:
            continue
        name = name_m.group(1)

        type_m  = re.search(r'\btype="([^"]+)"', attrs)
        grid_m  = re.search(r'\bgrid="([^"]+)"', attrs)
        ret     = type_m.group(1) if type_m else "void"
        grid    = grid_m.group(1) if grid_m else ""

        params  = re.findall(r'<param\s+type="([^"]+)"\s+name="([^"]+)"', body)

        desc_m  = re.search(r'<description[^>]*>(.*?)</description>', body, re.DOTALL)
        desc    = strip_html(desc_m.group(1)).strip() if desc_m else ""
        if "TODO" in desc or not desc:
            desc = ""

        funcs[name] = {
            "return_type": ret,
            "params":      params,   # [(type, name), ...]
            "description": desc,
            "grid":        grid,
        }

    return funcs


# ── Parse makopo tooltipdata.json ─────────────────────────────────────────────

_DELAY_RE   = re.compile(r"([\d.]+)\s*Forced Delay",   re.IGNORECASE)
_ENERGY_RE  = re.compile(r"([\d.]+)\s*Energy",          re.IGNORECASE)
_SIG_RE     = re.compile(
    r'<a[^>]*href="([^"]*)"[^>]*>[^<]+</a>\s*\(([^)]*)\)',
    re.DOTALL,
)
_RETTYPE_RE = re.compile(r"Function:\s*(\w+)\s+<a", re.IGNORECASE)


def parse_makopo(path: Path) -> dict:
    """
    Parse makopo tooltipdata.json for OSSL functions.
    Returns dict: name -> {description, delay, energy, wiki_url, signature}
    """
    data = json.loads(path.read_text(encoding="utf-8", errors="replace"))
    result = {}
    for key, html in data.items():
        if not (key.startswith("os") and key[2:3].isupper()):
            continue

        delay_m  = _DELAY_RE.search(html)
        energy_m = _ENERGY_RE.search(html)
        delay    = delay_m.group(1)  if delay_m  else ""
        energy   = energy_m.group(1) if energy_m else ""

        # Extract wiki URL from <a href=...>
        url_m   = re.search(r'href="([^"]*opensimulator\.org/wiki/[^"]*)"', html)
        wiki_url = url_m.group(1) if url_m else OS_WIKI_BASE + key

        # Clean description — strip HTML, remove the Forced Delay / Energy line
        plain = strip_html(html)
        plain = re.sub(r"Function:\s*\w+\s+\w+\(.*?\)\s*;?\s*", "", plain)
        plain = re.sub(r"[\d.]+\s*Forced Delay[^,\n]*,?\s*", "", plain)
        plain = re.sub(r"[\d.]+\s*Energy[^,\n]*", "", plain)
        plain = re.sub(r"\s+", " ", plain).strip().strip(";, ")
        if len(plain) < 5:
            plain = ""

        result[key] = {
            "description": plain,
            "delay":       delay,
            "energy":      energy,
            "wiki_url":    wiki_url,
        }
    return result


# ── Doc generation ────────────────────────────────────────────────────────────

def build_signature(name: str, ret: str, params: list) -> str:
    """Build a human-readable function signature string."""
    param_str = ", ".join(f"{t} {n}" for t, n in params)
    return f"{ret} {name}({param_str})"


def build_body(name: str, ret: str, params: list, desc: str,
               delay: str, energy: str, wiki_url: str) -> str:
    """Build the markdown body for a function doc."""
    lines = []

    if desc:
        lines.append(desc)
        lines.append("")

    lines.append("## Syntax")
    lines.append("")
    lines.append("```lsl")
    lines.append(build_signature(name, ret, params))
    lines.append("```")
    lines.append("")

    if params:
        lines.append("## Parameters")
        lines.append("")
        lines.append("| Type | Name |")
        lines.append("|------|------|")
        for t, n in params:
            lines.append(f"| `{t}` | `{n}` |")
        lines.append("")

    lines.append("## Return Value")
    lines.append("")
    lines.append(f"`{ret}`")
    lines.append("")

    meta = []
    if delay:
        meta.append(f"**Forced Delay:** {delay} seconds")
    if energy:
        meta.append(f"**Energy:** {energy}")

    if meta:
        lines.append("## Timing and Energy")
        lines.append("")
        for item in meta:
            lines.append(f"- {item}")
        lines.append("")

    lines.append("## Notes")
    lines.append("")
    lines.append(f"- OSSL function — requires appropriate threat level in the region's OpenSim configuration.")
    lines.append(f"- See: [{wiki_url}]({wiki_url})")
    lines.append("")

    return "\n".join(lines)


def append_chunk_if_changed(path: Path, chunk_label: str, chunk_content: str) -> bool:
    chunk_hash = hashlib.sha1(chunk_content.encode("utf-8")).hexdigest()[:12]
    marker = f"<!-- cache-chunk:{chunk_label}:{chunk_hash} -->"

    if path.exists():
        existing = path.read_text(encoding="utf-8")
        if marker in existing:
            return False
        with open(path, "a", encoding="utf-8") as fh:
            fh.write(
                f"\n\n{marker}\n"
                f"### Cache Delta — {TODAY} ({chunk_label})\n\n"
                f"{chunk_content.rstrip()}\n"
            )
        return True

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(chunk_content.rstrip() + "\n", encoding="utf-8")
    return True


def save_doc(name: str, kwdb_data: dict, makopo_data: dict) -> bool:
    """Generate and save a doc file. Existing files append chunk delta when --force is used."""
    out_path = OSSL_DIR / f"{name}.md"
    if out_path.exists() and not FORCE:
        return False

    ret    = kwdb_data.get("return_type", "void")
    params = kwdb_data.get("params", [])
    desc   = kwdb_data.get("description", "") or makopo_data.get("description", "")
    delay  = makopo_data.get("delay", "")
    energy = makopo_data.get("energy", "")
    wiki   = makopo_data.get("wiki_url", OS_WIKI_BASE + name)

    if not desc:
        desc = f"OSSL function: {name}."

    signature = build_signature(name, ret, params)
    body      = build_body(name, ret, params, desc, delay, energy, wiki)

    desc_safe = desc.replace('"', '\\"')
    sig_safe  = signature.replace('"', '\\"')

    front = f"""---
name: "{name}"
category: "function"
type: "function"
language: "OSSL"
description: "{desc_safe}"
signature: "{sig_safe}"
wiki_url: "{wiki}"
return_type: "{ret}"
energy_cost: "{energy}"
sleep_time: "{delay}"
first_fetched: "{TODAY}"
last_updated: "{TODAY}"
---
"""
    if not DRY_RUN:
        full_doc = front + "\n" + body
        if out_path.exists() and FORCE:
            delta = (
                "```yaml\n"
                f"{front.strip()}\n"
                "```\n\n"
                f"{body}"
            )
            return append_chunk_if_changed(out_path, "regen", delta)
        return append_chunk_if_changed(out_path, "initial", full_doc)
    return True


# ── Main ──────────────────────────────────────────────────────────────────────

print("Generating OSSL docs from local cache (kwdb.xml + makopo)...", flush=True)

if not KWDB_PATH.exists():
    print(f"ERROR: kwdb.xml not found at {KWDB_PATH}")
    sys.exit(1)

if not MAKOPO_PATH.exists():
    print(f"ERROR: tooltipdata.json not found at {MAKOPO_PATH}")
    sys.exit(1)

print(f"  Reading kwdb.xml ...", flush=True)
kwdb = parse_kwdb(KWDB_PATH)
print(f"  Found {len(kwdb)} OSSL functions in kwdb.xml", flush=True)

print(f"  Reading makopo tooltipdata.json ...", flush=True)
makopo = parse_makopo(MAKOPO_PATH)
print(f"  Found {len(makopo)} OSSL entries in makopo", flush=True)

# Merge: kwdb is authoritative for signatures; makopo adds descriptions/metadata
all_names = sorted(set(kwdb) | set(makopo))
print(f"  Total unique OSSL functions (combined): {len(all_names)}", flush=True)
print(flush=True)

written  = 0
skipped  = 0

for name in all_names:
    kd = kwdb.get(name, {})
    md = makopo.get(name, {})
    saved = save_doc(name, kd, md)
    if saved:
        written += 1
        if DRY_RUN:
            print(f"  [dry] would write: {name}.md", flush=True)
    else:
        skipped += 1

print(flush=True)
if DRY_RUN:
    print(f"[DRY RUN] Would write {written} files, skip {skipped} existing")
else:
    print(f"Done: {written} files written, {skipped} skipped (already exist)")

if written > 0 and not DRY_RUN:
    # Update manifest
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
                f"\n## {TODAY} — OSSL docs generated from local cache\n"
                f"- Sources: kwdb.xml ({len(kwdb)} functions), "
                f"makopo ({len(makopo)} entries)\n"
                f"- Generated {written} OSSL .md files in lsl-docs/ossl/\n"
                f"- Skipped {skipped} existing\n"
            )
    except Exception:
        pass
