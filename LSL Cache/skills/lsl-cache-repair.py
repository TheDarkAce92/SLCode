#!/usr/bin/env python3
# Skill: lsl-cache-repair
# Version: 0.1.0.0
# Purpose: Auto-repair common front matter issues in LSL cache documentation files
# Usage: python3 lsl-cache-repair.py [--dry-run] [--category all|functions|events|constants|examples|tutorials]
# Created: 2026-03-10
# Last modified: 2026-03-10

"""
Scans all doc files in ~/.lsl-cache/lsl-docs/ and repairs common front matter issues:
  - Empty/missing description  → extracted from doc body, or derived from name
  - Missing type               → inferred from directory (functions/ → "function")
  - Missing language           → defaults to "LSL"
  - Missing wiki_url           → constructed from function/event name
  - Missing first_fetched      → set to today

Merge-not-delete policy: never removes existing content; only fills in empty/absent fields.
"""

import io
import hashlib
import os
import re
import sys
import urllib.parse
from datetime import date
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# ── Config ────────────────────────────────────────────────────────────────────

_env_base  = os.environ.get("LSL_CACHE_BASE", "").strip()
CACHE_ROOT = Path(_env_base) if _env_base else Path(__file__).resolve().parents[1]
DOCS_DIR   = CACHE_ROOT / "lsl-docs"
TODAY      = date.today().isoformat()
DRY_RUN    = "--dry-run" in sys.argv

CATEGORY = "all"
for a in sys.argv[1:]:
    if a.startswith("--category="):
        CATEGORY = a.split("=", 1)[1]

CATEGORY_MAP = {
    "functions": ("function",  DOCS_DIR / "functions"),
    "events":    ("event",     DOCS_DIR / "events"),
    "constants": ("constant",  DOCS_DIR / "constants"),
    "tutorials": ("tutorial",  DOCS_DIR / "tutorials"),
    "examples":  ("example",   DOCS_DIR / "examples"),
}

SL_WIKI_BASE  = "https://wiki.secondlife.com/wiki/"
OS_WIKI_BASE  = "https://opensimulator.org/wiki/"


# ── Front matter helpers ──────────────────────────────────────────────────────

def parse_front_matter(text: str):
    """Return (fields_dict, body_str, has_fm_bool)."""
    m = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)', text, re.DOTALL)
    if not m:
        return {}, text, False
    raw, body = m.group(1), m.group(2)
    fields = {}
    for line in raw.splitlines():
        kv = re.match(r'^(\w[\w_]*):\s*(.*)', line)
        if kv:
            fields[kv.group(1)] = kv.group(2).strip().strip("\"'")
    return fields, body, True


def extract_description(body: str, name: str, doc_type: str) -> str:
    """Extract first substantial prose paragraph from body."""
    SKIP_PREFIXES = ('#', '```', '|', '-', '*', '<!--', '>', '_Source',
                     '!', '[', '{{', '}}')
    for para in body.split('\n\n'):
        s = para.strip()
        if not s:
            continue
        if any(s.startswith(p) for p in SKIP_PREFIXES):
            continue
        if re.match(r'^(#+\s|---)', s):
            continue
        # Strip markdown formatting
        text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', s)
        text = re.sub(r'\*+([^*]+)\*+', r'\1', text)
        text = re.sub(r'`([^`]+)`', r'\1', text)
        text = re.sub(r'\s+', ' ', text).strip()
        if len(text) > 20:
            if len(text) > 200:
                text = text[:197] + '...'
            return text
    return f"LSL {doc_type}: {name}."


def build_wiki_url(name: str, doc_type: str, folder_name: str) -> str:
    """Construct the most likely wiki URL for a given doc."""
    if folder_name == "ossl":
        return OS_WIKI_BASE + urllib.parse.quote(name)
    return SL_WIKI_BASE + urllib.parse.quote(name)


def apply_repairs(text: str, updates: dict) -> tuple:
    """
    Apply field updates to front matter. Only fills empty/absent fields.
    Returns (new_text, n_changes).
    """
    m = re.match(r'^(---\s*\n)(.*?)(\n---\s*\n)(.*)', text, re.DOTALL)
    if not m:
        return text, 0
    fm_open, raw_fm, fm_close, body = m.groups()

    lines       = raw_fm.splitlines()
    new_lines   = []
    handled     = set()
    changes     = 0

    for line in lines:
        kv = re.match(r'^(\w[\w_]*):\s*(.*)', line)
        if kv:
            field = kv.group(1)
            val   = kv.group(2).strip().strip("\"'")
            handled.add(field)
            # Only overwrite if field is empty
            if field in updates and not val:
                new_val = updates[field].replace('"', '\\"')
                new_lines.append(f'{field}: "{new_val}"')
                changes += 1
                continue
        new_lines.append(line)

    # Append any fields that were entirely absent
    for field, val in updates.items():
        if field not in handled:
            val_safe = val.replace('"', '\\"')
            new_lines.append(f'{field}: "{val_safe}"')
            changes += 1

    # Bump last_updated if we changed anything
    if changes:
        updated = []
        found_lu = False
        for line in new_lines:
            if line.startswith('last_updated:'):
                updated.append(f'last_updated: "{TODAY}"')
                found_lu = True
            else:
                updated.append(line)
        if not found_lu:
            updated.append(f'last_updated: "{TODAY}"')
        new_lines = updated

    new_fm = '\n'.join(new_lines)
    return fm_open + new_fm + fm_close + body, changes


def append_repair_delta(path: Path, updates: dict):
    """Append a repair delta block if this exact update chunk has not been recorded yet."""
    update_lines = [f"{k}: {v}" for k, v in sorted(updates.items())]
    payload = "\n".join(update_lines)
    chunk_hash = hashlib.sha1(payload.encode("utf-8")).hexdigest()[:12]
    marker = f"<!-- cache-repair:{chunk_hash} -->"

    existing = path.read_text(encoding="utf-8", errors="replace")
    if marker in existing:
        return False

    block = (
        f"\n\n{marker}\n"
        f"### Cache Repair Delta — {TODAY}\n\n"
        "```yaml\n"
        f"{payload}\n"
        "```\n"
    )
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(block)
    return True


# ── Main ─────────────────────────────────────────────────────────────────────

def run():
    total_files    = 0
    total_modified = 0
    total_changes  = 0
    total_skipped  = 0

    cats = list(CATEGORY_MAP.items()) if CATEGORY == "all" else \
           [(CATEGORY, CATEGORY_MAP[CATEGORY])] if CATEGORY in CATEGORY_MAP else []

    if not cats:
        print(f"Unknown category: {CATEGORY}. Use: all, functions, events, constants, examples, tutorials")
        sys.exit(1)

    # Also scan ossl/ and slua/ if they exist
    for extra_dir_name, extra_type in (("ossl", "function"), ("slua", "function")):
        extra_dir = DOCS_DIR / extra_dir_name
        if extra_dir.exists() and (CATEGORY == "all" or CATEGORY == extra_dir_name):
            cats.append((extra_dir_name, (extra_type, extra_dir)))

    for cat_name, (doc_type, folder) in cats:
        if not folder.exists():
            print(f"[skip] {cat_name}/ not found")
            continue
        print(f"\nScanning {cat_name}/ ...", flush=True)
        md_files = sorted(folder.glob("*.md"))
        print(f"  {len(md_files)} files", flush=True)

        for md_path in md_files:
            total_files += 1
            try:
                text = md_path.read_text(encoding="utf-8", errors="replace")
            except Exception as e:
                print(f"  [error] {md_path.name}: {e}")
                continue

            fields, body, has_fm = parse_front_matter(text)
            if not has_fm:
                total_skipped += 1
                continue

            name    = fields.get("name", md_path.stem)
            updates = {}

            # description
            desc = fields.get("description", "")
            if not desc:
                updates["description"] = extract_description(body, name, doc_type)

            # type
            if not fields.get("type"):
                updates["type"] = doc_type

            # language
            if not fields.get("language"):
                lang = "SLua" if cat_name == "slua" else "LSL"
                if cat_name == "ossl":
                    lang = "OSSL"
                updates["language"] = lang

            # wiki_url (skip tutorials, examples, patterns)
            if not fields.get("wiki_url") and cat_name not in ("tutorials", "examples"):
                updates["wiki_url"] = build_wiki_url(name, doc_type, cat_name)

            # first_fetched
            if not fields.get("first_fetched"):
                updates["first_fetched"] = TODAY

            if not updates:
                continue

            _new_text, n = apply_repairs(text, updates)
            if n:
                total_modified += 1
                total_changes  += n
                changed = ", ".join(updates.keys())
                print(f"  {'[dry] ' if DRY_RUN else ''}  {md_path.name}: {changed}", flush=True)
                if not DRY_RUN:
                    append_repair_delta(md_path, updates)

    print(f"\n{'[DRY RUN] ' if DRY_RUN else ''}Repair complete")
    print(f"  Files scanned:   {total_files}")
    print(f"  Files modified:  {total_modified}")
    print(f"  Field updates:   {total_changes}")
    print(f"  Skipped (no FM): {total_skipped}")
    if DRY_RUN:
        print("\n  Re-run without --dry-run to apply changes.")


if __name__ == "__main__":
    run()
