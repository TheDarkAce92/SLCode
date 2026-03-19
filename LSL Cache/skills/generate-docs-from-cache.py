#!/usr/bin/env python3
# Skill: generate-docs-from-cache
# Version: 0.1.0.0
# Purpose: Generate missing LSL function/event docs from jyaoma + pyoptimizer + makopo cache data
# Usage: python3 skills/generate-docs-from-cache.py [--type functions|events|all] [--force]
# Created: 2026-03-10
# Last modified: 2026-03-10

"""
Synthesises .md files for every LSL function and event not yet in the cache,
using structured data already fetched from jyaoma, pyoptimizer, and makopo.
No web requests. Produces richer docs than raw HTML scraping.
"""

import io
import hashlib
import json
import os
import re
import sys
from datetime import date
from html.parser import HTMLParser
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# ── Config ───────────────────────────────────────────────────────────────────

_env_base  = os.environ.get("LSL_CACHE_BASE", "").strip()
CACHE_ROOT = Path(_env_base) if _env_base else Path(__file__).resolve().parents[1]
DOCS_DIR   = CACHE_ROOT / "lsl-docs"
FN_DIR     = DOCS_DIR / "functions"
EV_DIR     = DOCS_DIR / "events"
EXT_DIR    = DOCS_DIR / "vscode-extension-data"
MANIFEST   = CACHE_ROOT / "cache-manifest.json"
CHANGELOG  = DOCS_DIR / "CHANGELOG.md"
README_MD  = DOCS_DIR / "README.md"
TODAY      = date.today().isoformat()

FORCE      = "--force" in sys.argv
FETCH_TYPE = "all"
for a in sys.argv[1:]:
    if a.startswith("--type="):
        FETCH_TYPE = a.split("=", 1)[1]


# ── Load source data ──────────────────────────────────────────────────────────

def load_json(path: Path) -> dict | list:
    if not path.exists():
        return {}
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_pyoptimizer_sigs(path: Path) -> dict:
    """Parse pyoptimizer fndata.txt for full function signatures → {name: sig}."""
    sigs = {}
    if not path.exists():
        return sigs
    sig_re = re.compile(r"^(\w+)\s+(ll\w+)\s*\(([^)]*)\)")
    with open(path, encoding="utf-8") as f:
        for line in f:
            m = sig_re.match(line.strip())
            if m:
                ret, fname, params = m.group(1), m.group(2), m.group(3)
                sigs[fname] = f"{ret} {fname}({params})"
    return sigs


def signature_to_params(sig: str) -> list[dict]:
    params = []
    m = re.match(r"^\w+\s+\w+\((.*)\)$", sig.strip())
    if not m:
        return params
    raw_params = m.group(1).strip()
    if not raw_params:
        return params
    for raw in raw_params.split(","):
        parts = raw.strip().split()
        if len(parts) >= 2:
            params.append({
                "type": parts[0],
                "name": parts[1],
                "description": "",
            })
    return params


def count_visible_docs(path: Path) -> int:
    return sum(
        1
        for item in path.rglob("*.md")
        if not any(part.startswith('.') for part in item.relative_to(path).parts)
    )


def count_reference_docs() -> int:
    return sum(1 for item in DOCS_DIR.glob("*.md") if item.name not in {"README.md", "CHANGELOG.md"})


def load_makopo(path: Path) -> dict:
    """Parse makopo tooltipdata.json → {name: {description, delay, energy, url}}."""
    if not path.exists():
        return {}
    with open(path, encoding="utf-8") as f:
        raw = json.load(f)
    result = {}
    for name, html in raw.items():
        info = parse_makopo_html(name, html)
        result[name] = info
    return result


class _StripHTML(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []
    def handle_data(self, d):
        self.parts.append(d)
    def get(self):
        return "".join(self.parts)


def strip_html(s: str) -> str:
    p = _StripHTML()
    p.feed(s)
    return p.get().strip()


def parse_makopo_html(name: str, html: str) -> dict:
    """Extract structured data from makopo's HTML tooltip string."""
    info = {"description": "", "delay": "", "energy": "", "url": ""}
    # URL
    url_m = re.search(r'href="([^"]+)"', html)
    if url_m:
        info["url"] = url_m.group(1)
    # Strip HTML for text
    text = strip_html(html)
    # Delay and energy
    delay_m  = re.search(r"([0-9.]+)\s*Forced Delay", text)
    energy_m = re.search(r"([0-9.]+)\s*Energy",       text)
    if delay_m:  info["delay"]  = delay_m.group(1)
    if energy_m: info["energy"] = energy_m.group(1)
    # Description: everything after the signature line up to the stats
    desc_m = re.search(r"\);\s*(.+?)(?:\n|$)", text, re.DOTALL)
    if desc_m:
        raw = desc_m.group(1).strip()
        raw = re.sub(r"\s+", " ", raw)
        raw = re.sub(r"[0-9.]+ Forced Delay.*", "", raw).strip()
        info["description"] = raw[:400]
    return info


# ── Doc generators ────────────────────────────────────────────────────────────

def make_function_doc(name: str, jdata: dict, sig: str, makopo: dict) -> tuple[dict, str]:
    """Return (front_matter_dict, markdown_body)."""
    mk = makopo.get(name, {})

    # Front matter
    wiki_url  = jdata.get("wiki") or mk.get("url") or f"https://wiki.secondlife.com/wiki/{name}"
    sleep_raw = jdata.get("sleep", 0)
    sleep_str = str(float(sleep_raw)) if sleep_raw else ""
    energy_raw = jdata.get("energy", 0)
    energy_str = str(float(energy_raw)) if energy_raw else mk.get("energy", "")
    desc = jdata.get("description", "") or mk.get("description", "")

    # Return type from signature
    ret_type = ""
    if sig:
        ret_m = re.match(r"^(\w+)\s+", sig)
        if ret_m:
            ret_type = ret_m.group(1)

    flags = []
    if jdata.get("experimental"): flags.append("experimental")
    if jdata.get("godMode"):      flags.append("god-mode")
    if jdata.get("experience"):   flags.append("experience-api")
    if jdata.get("broken"):       flags.append("broken")

    fm = {
        "name":          name,
        "category":      "function",
        "type":          "function",
        "language":      "LSL",
        "description":   desc[:300].replace('"', "'") if desc else "",
        "signature":     sig or "",
        "return_type":   ret_type,
        "sleep_time":    sleep_str if sleep_str and sleep_str != "0.0" else "",
        "energy_cost":   energy_str if energy_str and energy_str != "0.0" else "",
        "wiki_url":      wiki_url,
        "deprecated":    "true" if jdata.get("deprecated") else "false",
        "first_fetched": TODAY,
        "last_updated":  TODAY,
    }
    if flags:
        fm["flags"] = ", ".join(flags)

    # Markdown body
    params = jdata.get("parameters", []) or signature_to_params(sig)
    body_lines = []

    # Description
    if desc:
        body_lines.append(f"{desc}\n")

    # Signature block
    if sig:
        body_lines.append(f"\n## Signature\n\n```lsl\n{sig};\n```\n")

    # Parameters table
    if params:
        body_lines.append("\n## Parameters\n")
        body_lines.append("\n| Type | Name | Description |")
        body_lines.append("|------|------|-------------|")
        for p in params:
            ptype = p.get("type", "")
            pname = p.get("name", "")
            pdesc = p.get("description", "")
            st    = p.get("subtype")
            if st and st != ptype:
                ptype = f"{ptype} ({st})"
            body_lines.append(f"| `{ptype}` | `{pname}` | {pdesc} |")
        body_lines.append("")

    # Returns
    if ret_type and ret_type != "void":
        body_lines.append(f"\n## Return Value\n\nReturns `{ret_type}`.\n")

    # Caveats / flags
    caveats = []
    if sleep_str and sleep_str != "0.0":
        caveats.append(f"Forced delay: **{sleep_str} seconds** — the script sleeps after each call.")
    if energy_str and energy_str != "0.0":
        caveats.append(f"Energy cost: **{energy_str}**.")
    if jdata.get("experience"):
        caveats.append("Requires an active **Experience** (Experience API function).")
    if jdata.get("godMode"):
        caveats.append("Available to **god-mode** (Linden Lab internal) only.")
    if jdata.get("experimental"):
        caveats.append("**Experimental** — behaviour may change.")
    if jdata.get("broken"):
        caveats.append("⚠️ **Marked as broken** in LSL tooling data — verify current behaviour on the SL wiki.")

    if caveats:
        body_lines.append("\n## Caveats\n")
        for c in caveats:
            body_lines.append(f"- {c}")
        body_lines.append("")

    body_lines.append(f"\n## See Also\n\n- [SL Wiki]({wiki_url})\n")

    return fm, "\n".join(body_lines)


def make_event_doc(name: str, jdata: dict) -> tuple[dict, str]:
    """Return (front_matter_dict, markdown_body) for an event."""
    wiki_url = f"https://wiki.secondlife.com/wiki/{name}"
    desc     = jdata.get("description", "")
    params   = jdata.get("parameters", [])

    # Build signature
    param_sig = ", ".join(
        f"{p.get('type','')} {p.get('name','')}" for p in params
    )
    sig = f"{name}({param_sig})"

    fm = {
        "name":          name,
        "category":      "event",
        "type":          "event",
        "language":      "LSL",
        "description":   desc[:300].replace('"', "'") if desc else "",
        "signature":     sig,
        "wiki_url":      wiki_url,
        "first_fetched": TODAY,
        "last_updated":  TODAY,
    }

    body_lines = []
    if desc:
        body_lines.append(f"{desc}\n")

    body_lines.append(f"\n## Signature\n\n```lsl\n{sig}\n{{\n    // your code here\n}}\n```\n")

    if params:
        body_lines.append("\n## Parameters\n")
        body_lines.append("\n| Type | Name | Description |")
        body_lines.append("|------|------|-------------|")
        for p in params:
            ptype = p.get("type", "")
            pname = p.get("name", "")
            pdesc = p.get("description", "")
            st    = p.get("subtype")
            if st and st != ptype:
                ptype = f"{ptype} ({st})"
            body_lines.append(f"| `{ptype}` | `{pname}` | {pdesc} |")
        body_lines.append("")

    body_lines.append(f"\n## See Also\n\n- [SL Wiki]({wiki_url})\n")

    return fm, "\n".join(body_lines)


def render_front_matter(fm: dict) -> str:
    lines = ["---"]
    for k, v in fm.items():
        v_s = str(v).replace("\\", "\\\\")
        if any(c in v_s for c in ['"', '\n', ':']):
            lines.append(f"{k}: '{v_s}'")
        else:
            lines.append(f'{k}: "{v_s}"')
    lines.append("---")
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


def write_doc(path: Path, fm: dict, body: str):
    """Write YAML front matter + body. For existing files, append chunk delta on FORCE only."""
    fm_text = render_front_matter(fm)
    full_doc = f"{fm_text}\n\n{body}\n"

    if path.exists() and not FORCE:
        return False

    if path.exists() and FORCE:
        delta = (
            "```yaml\n"
            f"{fm_text}\n"
            "```\n\n"
            f"{body}"
        )
        return append_chunk_if_changed(path, "regen", delta)

    return append_chunk_if_changed(path, "initial", full_doc)


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print(f"generate-docs-from-cache v0.1.0.0 — {TODAY}")
    print(f"Cache: {CACHE_ROOT}")
    print()

    # Load source data
    print("Loading source data…")
    jyaoma_fn = load_json(EXT_DIR / "jyaoma" / "functions.json")
    jyaoma_ev = load_json(EXT_DIR / "jyaoma" / "events.json")
    pyopt_sig = load_pyoptimizer_sigs(EXT_DIR / "pyoptimizer" / "fndata.txt")
    makopo    = load_makopo(EXT_DIR / "makopo" / "tooltipdata.json")
    print(f"  jyaoma functions: {len(jyaoma_fn)}")
    print(f"  jyaoma events:    {len(jyaoma_ev)}")
    print(f"  pyoptimizer sigs: {len(pyopt_sig)}")
    print(f"  makopo entries:   {len(makopo)}")
    print()

    existing_fn = {f.stem for f in FN_DIR.glob("*.md")} if FN_DIR.exists() else set()
    existing_ev = {f.stem for f in EV_DIR.glob("*.md")} if EV_DIR.exists() else set()

    generated_fn = 0
    generated_ev = 0
    skipped      = 0

    function_names = sorted(set(jyaoma_fn.keys()) | set(pyopt_sig.keys()))

    # Functions
    if FETCH_TYPE in ("all", "functions"):
        missing = [n for n in function_names if n not in existing_fn] if not FORCE else function_names
        print(f"Functions: {len(existing_fn)} existing, {len(missing)} to generate")
        for name in missing:
            jdata = jyaoma_fn.get(name, {})
            sig   = pyopt_sig.get(name, "")
            fm, body = make_function_doc(name, jdata, sig, makopo)
            if write_doc(FN_DIR / f"{name}.md", fm, body):
                generated_fn += 1
            else:
                skipped += 1
        print(f"  Generated: {generated_fn}")

    # Events
    if FETCH_TYPE in ("all", "events"):
        missing = [n for n in jyaoma_ev if n not in existing_ev] if not FORCE else list(jyaoma_ev.keys())
        print(f"Events:    {len(existing_ev)} existing, {len(missing)} to generate")
        for name in sorted(missing):
            jdata = jyaoma_ev.get(name, {})
            fm, body = make_event_doc(name, jdata)
            if write_doc(EV_DIR / f"{name}.md", fm, body):
                generated_ev += 1
            else:
                skipped += 1
        print(f"  Generated: {generated_ev}")

    total_generated = generated_fn + generated_ev

    # Update README counts
    fn_total = count_visible_docs(FN_DIR)
    ev_total = count_visible_docs(EV_DIR)
    doc_total = fn_total + ev_total + count_visible_docs(DOCS_DIR / "constants") + count_visible_docs(DOCS_DIR / "tutorials") + count_reference_docs()
    if README_MD.exists():
        readme = README_MD.read_text(encoding="utf-8")
        readme = re.sub(r"_Total documents: \d+_",              f"_Total documents: {doc_total}_",   readme)
        readme = re.sub(r"\| Functions \| \d+ \|",              f"| Functions | {fn_total} |",        readme)
        readme = re.sub(r"\| Events \| \d+ \|",                 f"| Events | {ev_total} |",           readme)
        readme = re.sub(r"\| \*\*Total\*\* \| \*\*\d+\*\* \|", f"| **Total** | **{doc_total}** |",  readme)
        README_MD.write_text(readme, encoding="utf-8")

    # Update CHANGELOG
    cl = CHANGELOG.read_text(encoding="utf-8") if CHANGELOG.exists() else "# LSL Docs Changelog\n"
    entry  = f"\n## {TODAY} — Synthesised gap-fill from cache data\n"
    entry += f"- Generated {generated_fn} function docs from jyaoma + pyoptimizer + makopo\n"
    entry += f"- Generated {generated_ev} event docs from jyaoma\n"
    entry += f"- Total functions on disk: {fn_total}, events: {ev_total}\n"
    CHANGELOG.write_text(cl + entry, encoding="utf-8")

    # Update manifest
    if MANIFEST.exists():
        raw_manifest = MANIFEST.read_text(encoding="utf-8").strip()
        try:
            manifest = json.loads(raw_manifest) if raw_manifest else {}
        except Exception:
            manifest = {}
    else:
        manifest = {}
    doc_counts = manifest.setdefault("doc_counts", {})
    doc_counts["functions"] = fn_total
    doc_counts["events"]    = ev_total
    manifest["last_updated"] = TODAY
    MANIFEST.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print()
    print(f"Done. Generated {total_generated} docs ({skipped} skipped — already exist).")
    print(f"Functions on disk: {fn_total} / {len(function_names)}")
    print(f"Events on disk:    {ev_total} / {len(jyaoma_ev)}")
    print(f"Total doc count:   {doc_total}")


if __name__ == "__main__":
    main()
