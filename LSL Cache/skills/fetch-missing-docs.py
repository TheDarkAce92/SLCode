#!/usr/bin/env python3
# Skill: fetch-missing-docs
# Version: 0.1.0.0
# Purpose: Batch-fetch missing LSL function/event docs from the SL wiki using the MediaWiki API
# Usage: python3 skills/fetch-missing-docs.py [--dry-run] [--type functions|events|all]
# Created: 2026-03-10
# Last modified: 2026-03-10

"""
Uses the MediaWiki API (50-page batches) to fetch wikitext for all LSL functions and events
not yet present in the local cache. Converts wikitext to Markdown and saves with YAML front matter.

MediaWiki API: https://wiki.secondlife.com/api.php?action=query&prop=revisions&rvprop=content&format=json&titles=T1|T2|...
"""

import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

# ── Config ──────────────────────────────────────────────────────────────────

_env_base    = os.environ.get("LSL_CACHE_BASE", "").strip()
CACHE_ROOT   = Path(_env_base) if _env_base else Path(__file__).resolve().parents[1]
DOCS_DIR     = CACHE_ROOT / "lsl-docs"
FN_DIR       = DOCS_DIR / "functions"
EV_DIR       = DOCS_DIR / "events"
MANIFEST     = CACHE_ROOT / "cache-manifest.json"
CHANGELOG    = DOCS_DIR / "CHANGELOG.md"
README       = DOCS_DIR / "README.md"
EXT_DIR      = DOCS_DIR / "vscode-extension-data"

WIKI_API     = "https://wiki.secondlife.com/api.php"
BATCH_SIZE   = 50     # MediaWiki API limit per request
RATE_DELAY   = 0.4    # seconds between batch requests (be polite)
TODAY        = date.today().isoformat()

DRY_RUN      = "--dry-run" in sys.argv
FETCH_TYPE   = "all"
for arg in sys.argv[1:]:
    if arg.startswith("--type="):
        FETCH_TYPE = arg.split("=")[1]

# ── Helpers ──────────────────────────────────────────────────────────────────

def slug(name: str) -> str:
    return re.sub(r"[^a-z0-9_]", "", name.lower().replace(" ", "_"))


def get_existing(directory: Path) -> set:
    if not directory.exists():
        return set()
    return {f.stem for f in directory.glob("*.md")}


def get_jyaoma_list(filename: str) -> list:
    path = EXT_DIR / "jyaoma" / filename
    if not path.exists():
        return []
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict):
        return list(data.keys())
    return [item.get("name", "") for item in data if isinstance(item, dict)]


def get_pyoptimizer_function_list() -> list[str]:
    path = EXT_DIR / "pyoptimizer" / "fndata.txt"
    if not path.exists():
        return []
    names = []
    sig_re = re.compile(r"^\w+\s+(ll\w+)\s*\(")
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        m = sig_re.match(line.strip())
        if m:
            names.append(m.group(1))
    return names


# ── MediaWiki API fetch ───────────────────────────────────────────────────────

def fetch_wikitext_batch(titles: list[str]) -> dict[str, str]:
    """Fetch wikitext for up to 50 titles in one API call. Returns {title: wikitext}."""
    params = urllib.parse.urlencode({
        "action":   "query",
        "prop":     "revisions",
        "rvprop":   "content",
        "rvslots":  "main",
        "format":   "json",
        "titles":   "|".join(titles),
    })
    url = f"{WIKI_API}?{params}"
    req = urllib.request.Request(url, headers={"User-Agent": "LSL-Cache-Bot/1.0 (local tool)"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"    ERROR fetching batch: {e}")
        return {}

    result = {}
    pages = data.get("query", {}).get("pages", {})
    for page_id, page in pages.items():
        if page_id == "-1":
            # Page doesn't exist
            title = page.get("title", "")
            result[title] = None
            continue
        title = page.get("title", "")
        revs = page.get("revisions", [])
        if revs:
            slots = revs[0].get("slots", {})
            content = slots.get("main", {}).get("*", "") or revs[0].get("*", "")
            result[title] = content
    return result


# ── Wikitext → Markdown ───────────────────────────────────────────────────────

def wikitext_to_markdown(text: str) -> str:
    """Convert MediaWiki markup to approximate Markdown. Not perfect but good enough."""
    # Remove template calls we don't need
    text = re.sub(r"\{\{LSL_Function[^}]*\}\}", "", text, flags=re.DOTALL)
    text = re.sub(r"\{\{LSL_Event[^}]*\}\}", "", text, flags=re.DOTALL)

    # LSL code blocks
    text = re.sub(r"<lsl>(.*?)</lsl>", lambda m: "```lsl\n" + m.group(1).strip() + "\n```", text, flags=re.DOTALL)
    text = re.sub(r"<source\s+lang=\"lsl2\"[^>]*>(.*?)</source>", lambda m: "```lsl\n" + m.group(1).strip() + "\n```", text, flags=re.DOTALL)
    text = re.sub(r"<syntaxhighlight\s+lang=\"lsl2\"[^>]*>(.*?)</syntaxhighlight>", lambda m: "```lsl\n" + m.group(1).strip() + "\n```", text, flags=re.DOTALL)

    # Generic code / pre
    text = re.sub(r"<code>(.*?)</code>", r"`\1`", text, flags=re.DOTALL)
    text = re.sub(r"<pre>(.*?)</pre>", lambda m: "```\n" + m.group(1).strip() + "\n```", text, flags=re.DOTALL)

    # Headings
    text = re.sub(r"^====\s*(.*?)\s*====", r"#### \1", text, flags=re.MULTILINE)
    text = re.sub(r"^===\s*(.*?)\s*===",  r"### \1",  text, flags=re.MULTILINE)
    text = re.sub(r"^==\s*(.*?)\s*==",   r"## \1",   text, flags=re.MULTILINE)

    # Bold / italic
    text = re.sub(r"'''(.*?)'''", r"**\1**", text)
    text = re.sub(r"''(.*?)''",   r"*\1*",   text)

    # Links: [[Page|Label]] → Label, [[Page]] → Page
    text = re.sub(r"\[\[([^|\]]+)\|([^\]]+)\]\]", r"\2", text)
    text = re.sub(r"\[\[([^\]]+)\]\]", r"\1", text)

    # External links: [URL Label] → [Label](URL)
    text = re.sub(r"\[(\S+)\s+([^\]]+)\]", r"[\2](\1)", text)

    # Tables (simplify to text)
    text = re.sub(r"^\{\|.*?^\|\}", "", text, flags=re.MULTILINE | re.DOTALL)

    # Templates {{name|...}} — strip most, preserve content of some
    text = re.sub(r"\{\{[Nn]ote\|(.*?)\}\}", r"> **Note:** \1", text, flags=re.DOTALL)
    text = re.sub(r"\{\{[Ww]arning\|(.*?)\}\}", r"> ⚠️ **Warning:** \1", text, flags=re.DOTALL)
    text = re.sub(r"\{\{[Dd]eprecated[^}]*\}\}", "> ⚠️ **Deprecated.** See the wiki for the recommended alternative.", text)
    text = re.sub(r"\{\{[^}]+\}\}", "", text)  # strip remaining templates

    # HTML tags
    text = re.sub(r"<[^>]+>", "", text)

    # Lists: * and # → - and 1.
    text = re.sub(r"^\*\s*", "- ", text, flags=re.MULTILINE)
    text = re.sub(r"^#\s*",  "1. ", text, flags=re.MULTILINE)

    # Collapse 3+ blank lines to 2
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


# ── Front matter extraction ───────────────────────────────────────────────────

KNOWN_SLEEP = {
    "llSleep": "1.0", "llDialog": "1.0", "llTextBox": "1.0",
    "llRequestAgentData": "0.1", "llRequestInventoryData": "0.1",
    "llHTTPRequest": "0.0", "llEmail": "20.0", "llInstantMessage": "2.0",
    "llRezObject": "0.1", "llSensor": "0.0", "llGiveMoney": "0.0",
    "llGiveInventory": "2.0", "llGiveInventoryList": "3.0",
    "llLoadURL": "0.1", "llMapDestination": "1.0", "llParcelMediaCommandList": "2.0",
}

def extract_function_meta(name: str, wikitext: str) -> dict:
    """Extract signature, return type, description, sleep time from wikitext."""
    meta = {
        "name":        name,
        "category":    "function",
        "type":        "function",
        "language":    "LSL",
        "wiki_url":    f"https://wiki.secondlife.com/wiki/{urllib.parse.quote(name)}",
        "first_fetched": TODAY,
        "last_updated":  TODAY,
        "description": "",
        "signature":   "",
        "return_type": "",
        "sleep_time":  KNOWN_SLEEP.get(name, ""),
        "energy_cost": "",
        "deprecated":  "false",
    }

    # Return type and signature from first function definition line
    sig_m = re.search(r"(\w+)\s+" + re.escape(name) + r"\s*\([^)]*\)", wikitext)
    if sig_m:
        meta["return_type"] = sig_m.group(1)
        meta["signature"]   = sig_m.group(0).strip()

    # Description: first plain-text paragraph after any templates
    desc_m = re.search(r"\n\n([A-Z][^{\n][^\n]{10,})\n", wikitext)
    if desc_m:
        raw = desc_m.group(1).strip()
        # Strip wikitext markup from description
        raw = re.sub(r"\[\[([^|\]]+)\|([^\]]+)\]\]", r"\2", raw)
        raw = re.sub(r"\[\[([^\]]+)\]\]", r"\1", raw)
        raw = re.sub(r"'''?([^']+)'''?", r"\1", raw)
        raw = re.sub(r"\{\{[^}]+\}\}", "", raw)
        meta["description"] = raw[:300].strip()

    # Sleep time from {{Delay}} or explicit mention
    delay_m = re.search(r"\{\{[Dd]elay\|([0-9.]+)\}\}", wikitext)
    if delay_m:
        meta["sleep_time"] = delay_m.group(1)
    elif re.search(r"[Ff]orced\s+delay[:\s]+([0-9.]+)\s*sec", wikitext):
        m = re.search(r"[Ff]orced\s+delay[:\s]+([0-9.]+)\s*sec", wikitext)
        meta["sleep_time"] = m.group(1)

    # Energy
    energy_m = re.search(r"[Ee]nergy[:\s]+([0-9.]+)", wikitext)
    if energy_m:
        meta["energy_cost"] = energy_m.group(1)

    # Deprecated
    if re.search(r"\{\{[Dd]eprecated", wikitext, re.IGNORECASE):
        meta["deprecated"] = "true"

    return meta


def extract_event_meta(name: str, wikitext: str) -> dict:
    meta = {
        "name":        name,
        "category":    "event",
        "type":        "event",
        "language":    "LSL",
        "wiki_url":    f"https://wiki.secondlife.com/wiki/{urllib.parse.quote(name)}",
        "first_fetched": TODAY,
        "last_updated":  TODAY,
        "description": "",
        "signature":   "",
        "deprecated":  "false",
    }

    sig_m = re.search(re.escape(name) + r"\s*\([^)]*\)", wikitext)
    if sig_m:
        meta["signature"] = sig_m.group(0).strip()

    desc_m = re.search(r"\n\n([A-Z][^{\n][^\n]{10,})\n", wikitext)
    if desc_m:
        raw = desc_m.group(1)
        raw = re.sub(r"\[\[([^|\]]+)\|([^\]]+)\]\]", r"\2", raw)
        raw = re.sub(r"\[\[([^\]]+)\]\]", r"\1", raw)
        raw = re.sub(r"'''?([^']+)'''?", r"\1", raw)
        raw = re.sub(r"\{\{[^}]+\}\}", "", raw)
        meta["description"] = raw[:300].strip()

    return meta


def write_doc(path: Path, meta: dict, body: str):
    """Write a doc file with YAML front matter. Merge if file exists."""
    if path.exists():
        # Append-only merge: add dated update block
        existing = path.read_text(encoding="utf-8")
        update_block = f"\n\n---\n### Update — {TODAY}\n_Re-fetched. Content below may differ from original._\n\n{body}\n---\n"
        path.write_text(existing + update_block, encoding="utf-8")
        return

    fm_lines = ["---"]
    for k, v in meta.items():
        if v:
            fm_lines.append(f'{k}: "{v}"')
    fm_lines.append("---")
    fm = "\n".join(fm_lines)

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"{fm}\n\n{body}\n", encoding="utf-8")


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    print(f"fetch-missing-docs v0.1.0.0 — {TODAY}")
    print(f"Cache root: {CACHE_ROOT}")
    if DRY_RUN:
        print("  DRY RUN — no files will be written\n")
    print()

    # Determine what to fetch
    tasks = []  # list of (name, wiki_title, out_dir, meta_fn)

    if FETCH_TYPE in ("all", "functions"):
        existing_fn  = get_existing(FN_DIR)
        all_functions = sorted(set(get_jyaoma_list("functions.json")) | set(get_pyoptimizer_function_list()))
        missing_fn   = [n for n in all_functions if n not in existing_fn]
        print(f"Functions: {len(existing_fn)} documented, {len(all_functions)} known, {len(missing_fn)} to fetch")
        tasks += [(n, n, FN_DIR, "function") for n in missing_fn]

    if FETCH_TYPE in ("all", "events"):
        existing_ev  = get_existing(EV_DIR)
        all_events   = get_jyaoma_list("events.json")
        missing_ev   = [n for n in all_events if n not in existing_ev]
        print(f"Events:    {len(existing_ev)} documented, {len(all_events)} known, {len(missing_ev)} to fetch")
        tasks += [(n, n, EV_DIR, "event") for n in missing_ev]

    if not tasks:
        print("Nothing to fetch.")
        return

    total = len(tasks)
    print(f"\nTotal to fetch: {total}")
    print(f"Batches of {BATCH_SIZE}: {-(-total // BATCH_SIZE)} requests\n")

    if DRY_RUN:
        for name, _, _, t in tasks[:20]:
            print(f"  Would fetch [{t}]: {name}")
        if total > 20:
            print(f"  ... and {total-20} more")
        return

    # Batch fetch
    fetched_ok  = 0
    not_found   = []
    errors      = []
    changelog_entries = []

    for batch_start in range(0, total, BATCH_SIZE):
        batch = tasks[batch_start:batch_start + BATCH_SIZE]
        titles = [t[1] for t in batch]
        print(f"  Batch {batch_start // BATCH_SIZE + 1}/{-(-total // BATCH_SIZE)}: fetching {len(titles)} pages…", end=" ", flush=True)

        wikitext_map = fetch_wikitext_batch(titles)
        time.sleep(RATE_DELAY)

        batch_ok = 0
        for name, wiki_title, out_dir, doc_type in batch:
            wt = wikitext_map.get(wiki_title)
            if wt is None:
                not_found.append(name)
                continue
            if not wt.strip():
                not_found.append(name)
                continue

            body = wikitext_to_markdown(wt)
            if doc_type == "function":
                meta = extract_function_meta(name, wt)
            else:
                meta = extract_event_meta(name, wt)

            out_path = out_dir / f"{name}.md"
            write_doc(out_path, meta, body)
            fetched_ok += 1
            batch_ok   += 1
            changelog_entries.append(f"- Fetched {out_dir.name}/{name}.md [{doc_type}]")

        print(f"{batch_ok} OK")

    # ── Update cache README ──────────────────────────────────────────────────
    fn_count = len(list(FN_DIR.glob("*.md")))
    ev_count = len(list(EV_DIR.glob("*.md")))
    readme_text = README.read_text(encoding="utf-8")
    readme_text = re.sub(r"_Total documents: \d+_", f"_Total documents: {fn_count + ev_count + 7 + 3 + 5}_", readme_text)
    readme_text = re.sub(r"\| Functions \| \d+ \|", f"| Functions | {fn_count} |", readme_text)
    readme_text = re.sub(r"\| Events \| \d+ \|", f"| Events | {ev_count} |", readme_text)
    readme_text = re.sub(r"\| \*\*Total\*\* \| \*\*\d+\*\* \|", f"| **Total** | **{fn_count + ev_count + 7 + 3 + 5}** |", readme_text)
    README.write_text(readme_text, encoding="utf-8")

    # ── Update CHANGELOG ────────────────────────────────────────────────────
    cl_text = CHANGELOG.read_text(encoding="utf-8")
    entry = f"\n## {TODAY} — Batch gap-fill\n"
    entry += f"- Fetched {fetched_ok} new docs ({fn_count} total functions, {ev_count} total events)\n"
    if not_found:
        entry += f"- Not found on wiki ({len(not_found)}): {', '.join(not_found[:20])}"
        if len(not_found) > 20:
            entry += f" ... and {len(not_found)-20} more"
        entry += "\n"
    CHANGELOG.write_text(cl_text + entry, encoding="utf-8")

    # ── Update manifest ──────────────────────────────────────────────────────
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    manifest["doc_counts"]["functions"] = fn_count
    manifest["doc_counts"]["events"]    = ev_count
    manifest["last_updated"]            = TODAY
    MANIFEST.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    # ── Summary ─────────────────────────────────────────────────────────────
    print()
    print(f"── Results ──────────────────────────────────────────────────")
    print(f"  Fetched:   {fetched_ok}")
    print(f"  Not found: {len(not_found)}")
    if not_found:
        print(f"  Missing:   {', '.join(not_found[:10])}" + ("..." if len(not_found) > 10 else ""))
    print(f"  Functions on disk now: {fn_count}")
    print(f"  Events on disk now:    {ev_count}")
    print()


if __name__ == "__main__":
    main()
