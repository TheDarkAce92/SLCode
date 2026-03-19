# Skill: analyse-snippets
# Version: 0.1.0.2
# Purpose: Analyse all extension snippets and produce standalone pattern library
# Usage: python3 skills/analyse-snippets.py
# Created: 2026-03-09
# Last modified: 2026-03-09

"""
Analyses snippets.json and lsl.json files from all vscode-extension-data sources.
Classifies each snippet as idiom / pattern / anti-pattern / function-usage.
Generates .md files to lsl-docs/patterns/ and updates function doc front matter.
"""

import json
import hashlib
import os
import re
import sys
from datetime import date
from pathlib import Path

# Ensure UTF-8 output on Windows (avoids cp1252 encode errors with box-drawing chars)
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ── Configuration ──────────────────────────────────────────────────────────

_env_base  = os.environ.get("LSL_CACHE_BASE", "").strip()
CACHE_ROOT = Path(_env_base) if _env_base else Path(__file__).resolve().parents[1]
EXT_DATA_DIR = CACHE_ROOT / "lsl-docs" / "vscode-extension-data"
PATTERNS_DIR = CACHE_ROOT / "lsl-docs" / "patterns"
FUNCTIONS_DIR = CACHE_ROOT / "lsl-docs" / "functions"
MANIFEST_PATH = CACHE_ROOT / "cache-manifest.json"
MANIFEST_DELTA_LOG = CACHE_ROOT / "cache-manifest-deltas.log"
TODAY = date.today().isoformat()

# Genuine LSL anti-patterns: functions whose PRIMARY use in a short snippet
# is considered harmful. Must be a named function that is broadly discouraged,
# not merely expensive or context-dependent.
ANTI_PATTERN_MARKERS = {
    "llSleep",    # blocks the entire script thread — always an anti-pattern in isolation
    "llResetScript",  # losing state silently; prefer explicit state transitions
}

# Functions with known sleep times (used to flag sleep-heavy snippets)
SLEEP_FUNCTIONS = {
    "llSleep", "llDialog", "llTextBox", "llRequestAgentData",
    "llRequestInventoryData", "llHTTPRequest", "llEmail",
    "llInstantMessage", "llRezObject", "llSensor",
}

# Single-token bodies: just a constant name or simple keyword — skip these entirely.
# buildersbrewery lsl.json has ~1100 of these (ACTIVE, AGENT_FLYING, etc.)
_SINGLE_TOKEN_RE = re.compile(r"^\s*\$?[A-Z_][A-Z0-9_]*\s*$")

# ── Helpers ────────────────────────────────────────────────────────────────

def load_json_file(path: Path) -> dict | list | None:
    try:
        with open(path, encoding="utf-8") as f:
            text = f.read()
        # Try standard JSON first
        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            # Fall back to JSONC: strip // line comments (e.g. buildersbrewery lsl.json)
            stripped = re.sub(r"//[^\n]*", "", text)
            data = json.loads(stripped)
        # buildersbrewery nests snippets under a top-level "lsl" key
        if isinstance(data, dict) and list(data.keys()) == ["lsl"]:
            data = data["lsl"]
        return data
    except Exception as e:
        print(f"  WARN: Could not load {path}: {e}")
        return None


def slug(name: str) -> str:
    """Convert snippet name to a filesystem-safe slug."""
    s = name.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def is_completion_token(body: str) -> bool:
    """Return True if the body is just a constant/token name — not a meaningful snippet.
    buildersbrewery lsl.json has ~1100 of these (ACTIVE, AGENT_FLYING, ATTACH_BACK, etc.).
    These are completion tokens, not patterns, idioms, or anti-patterns."""
    stripped = body.strip()
    # Single-word ALL_CAPS token (constant), or simple keyword/type
    if _SINGLE_TOKEN_RE.match(stripped):
        return True
    # Multi-word but still just tab-completion: no braces, semicolons, or ll* calls
    if "\n" not in stripped and ";" not in stripped and "{" not in stripped and "ll" not in stripped:
        return True
    return False


def classify_snippet(name: str, prefix: str, body: str) -> str:
    """Classify a snippet as idiom / pattern / anti-pattern / function-usage.
    Returns None for completion tokens that should be skipped entirely."""
    lines = [l for l in body.splitlines() if l.strip()]
    num_lines = len(lines)

    # Anti-pattern: the snippet's PRIMARY purpose is a known anti-pattern function,
    # used in isolation (not buried in a larger useful snippet).
    for marker in ANTI_PATTERN_MARKERS:
        if re.search(r"\b" + re.escape(marker) + r"\s*\(", body) and num_lines < 5:
            return "anti-pattern"

    # Function-usage: prefix matches an LSL ll* function name AND body has substance
    if re.match(r"ll[A-Z]\w+", prefix) and num_lines >= 1:
        return "function-usage"

    # Pattern: multi-block structure (has state/event/braces nesting, or >= 8 lines)
    if num_lines >= 8 or re.search(r"\bstate\b\s+\w|\bdefault\b\s*\{|\}\s*\n\s*\w+\s*\{", body):
        return "pattern"

    # Idiom: short but meaningful multi-token code snippet (has ll* call, semicolons, or operators)
    has_ll_call  = bool(re.search(r"\bll[A-Z]\w+\s*\(", body))
    has_operator = bool(re.search(r"[;=+\-*/<>!&|]", body))
    if has_ll_call or (has_operator and num_lines >= 1):
        return "idiom"

    # Anything else is a completion token — skip
    return None


def extract_functions_used(body: str) -> list[str]:
    """Extract ll* function calls from snippet body."""
    return sorted(set(re.findall(r"\bll[A-Z]\w+\b", body)))


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


def write_pattern_file(category: str, name: str, prefix: str, body: str,
                        sources: list[str], functions_used: list[str]) -> Path:
    """Write a pattern .md file and return its path."""
    out_dir = PATTERNS_DIR / (category + "s" if not category.endswith("s") else category)
    # Map category names to directory names
    dir_map = {
        "idiom": "idioms",
        "pattern": "patterns",
        "anti-pattern": "anti-patterns",
        "function-usage": "function-usage",
    }
    out_dir = PATTERNS_DIR / dir_map.get(category, category)
    out_dir.mkdir(parents=True, exist_ok=True)

    filename = slug(name) + ".md"
    out_path = out_dir / filename

    tags = []
    if functions_used:
        tags = functions_used[:3]  # use top 3 functions as tags

    content = f"""---
name: "{name}"
category: {category}
tags: {json.dumps(tags)}
functions_used: {json.dumps(functions_used)}
sources: {json.dumps(sources)}
memory_impact: unknown
complexity: beginner
extracted: "{TODAY}"
last_reviewed: "{TODAY}"
---

# {name}

Extracted from: {", ".join(sources)}

## Code

```lsl
{body}
```

## When to Use

- _(Add usage notes here)_

## Gotchas

- _(Add caveats here)_

## See Also

- `/lsl-docs/patterns/README.md`
"""
    if out_path.exists():
        append_chunk_if_changed(out_path, "pattern-refresh", content)
    else:
        out_path.write_text(content, encoding="utf-8")
    return out_path


def update_function_doc_front_matter(func_name: str, pattern_slug: str):
    """Append a pattern-reference delta block to the function doc (no in-place edits)."""
    doc_path = FUNCTIONS_DIR / f"{func_name}.md"
    if not doc_path.exists():
        return

    delta = (
        f"Pattern reference candidate: `{pattern_slug}`\n\n"
        "```yaml\n"
        f"patterns: [\"{pattern_slug}\"]\n"
        "```"
    )
    append_chunk_if_changed(doc_path, f"pattern-ref-{pattern_slug}", delta)


# ── Main ───────────────────────────────────────────────────────────────────

def main():
    print(f"analyse-snippets v0.1.0.2 — {TODAY}")
    print(f"Cache root: {CACHE_ROOT}")
    print()

    # Collect all snippet files
    snippet_files: list[tuple[Path, str]] = []
    for source_dir in EXT_DATA_DIR.iterdir():
        if not source_dir.is_dir():
            continue
        source_name = source_dir.name
        for fname in ["snippets.json", "lsl.json", "oldSnippets.json"]:
            fpath = source_dir / fname
            if fpath.exists():
                snippet_files.append((fpath, source_name))

    if not snippet_files:
        print("No snippet files found. Run initialisation first.")
        sys.exit(1)

    print(f"Found {len(snippet_files)} snippet file(s):")
    for fp, src in snippet_files:
        print(f"  {src}/{fp.name}")
    print()

    # Deduplicate and classify
    seen: dict[str, dict] = {}  # key = slug(name), value = entry dict

    for fpath, source_name in snippet_files:
        data = load_json_file(fpath)
        if not data:
            continue
        if isinstance(data, list):
            items = {item.get("name", item.get("prefix", str(i))): item for i, item in enumerate(data)}
        else:
            items = data  # VS Code snippets format: dict of {name: {prefix, body, description}}

        for entry_name, entry in items.items():
            if isinstance(entry, dict):
                prefix = entry.get("prefix", entry_name)
                if isinstance(prefix, list):
                    prefix = prefix[0] if prefix else entry_name
                body_raw = entry.get("body", "")
                if isinstance(body_raw, list):
                    body = "\n".join(body_raw)
                else:
                    body = str(body_raw)
            else:
                continue

            # Skip pure completion tokens (constants with no code content)
            if is_completion_token(body):
                continue

            key = slug(entry_name)
            if key in seen:
                seen[key]["sources"].append(f"{source_name}/{fpath.name}")
            else:
                seen[key] = {
                    "name": entry_name,
                    "prefix": prefix,
                    "body": body,
                    "sources": [f"{source_name}/{fpath.name}"],
                }

    print(f"Unique snippets found: {len(seen)}")
    print()

    # Classify and write
    counts = {"idiom": 0, "pattern": 0, "anti-pattern": 0, "function-usage": 0}
    pattern_map: dict[str, list[str]] = {}  # func_name → list of pattern slugs

    skipped = 0
    for key, entry in seen.items():
        category = classify_snippet(entry["name"], entry["prefix"], entry["body"])
        if category is None:
            skipped += 1
            continue
        functions_used = extract_functions_used(entry["body"])

        write_pattern_file(
            category=category,
            name=entry["name"],
            prefix=entry["prefix"],
            body=entry["body"],
            sources=entry["sources"],
            functions_used=functions_used,
        )

        counts[category] += 1

        for func in functions_used:
            pattern_map.setdefault(func, []).append(key)

    print(f"  Skipped (completion tokens): {skipped}")

    # Update function doc front matter
    updated_docs = 0
    for func_name, pattern_slugs in pattern_map.items():
        for ps in pattern_slugs:
            update_function_doc_front_matter(func_name, ps)
        updated_docs += 1

    # Write patterns README
    readme_lines = [
        "# LSL Pattern Library\n",
        f"_Last analysis: {TODAY}_\n\n",
        f"## Summary\n\n",
        f"| Category | Count |\n|----------|-------|\n",
    ]
    for cat, count in counts.items():
        readme_lines.append(f"| {cat} | {count} |\n")
    readme_lines.append(f"\n**Total:** {sum(counts.values())} patterns\n\n")
    readme_lines.append("## Pattern Index\n\n")
    readme_lines.append("| Name | Category | Functions Used | File |\n")
    readme_lines.append("|------|----------|----------------|------|\n")

    dir_map = {
        "idiom": "idioms",
        "pattern": "patterns",
        "anti-pattern": "anti-patterns",
        "function-usage": "function-usage",
    }

    for key, entry in seen.items():
        category = classify_snippet(entry["name"], entry["prefix"], entry["body"])
        if category is None:
            continue
        functions_used = extract_functions_used(entry["body"])
        funcs_str = ", ".join(functions_used[:3]) + ("..." if len(functions_used) > 3 else "")
        subdir = dir_map.get(category, category)
        readme_lines.append(f"| {entry['name']} | {category} | {funcs_str} | `{subdir}/{key}.md` |\n")

    append_chunk_if_changed(PATTERNS_DIR / "README.md", "pattern-index", "".join(readme_lines))

    # Record manifest-style update as append-only delta (do not rewrite JSON manifest)
    manifest_delta = f"{TODAY}\tpatterns_last_run\t{TODAY}\n"
    append_chunk_if_changed(MANIFEST_DELTA_LOG, "patterns-last-run", manifest_delta)

    # Summary
    print("── Results ──────────────────────────────────────────────────")
    print(f"  Idioms:          {counts['idiom']}")
    print(f"  Patterns:        {counts['pattern']}")
    print(f"  Anti-patterns:   {counts['anti-pattern']}")
    print(f"  Function-usage:  {counts['function-usage']}")
    print(f"  Total:           {sum(counts.values())}")
    print(f"  Function docs updated with pattern refs: {updated_docs}")
    print(f"  patterns/README.md written.")
    print()


if __name__ == "__main__":
    main()
