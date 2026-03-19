#!/usr/bin/env bash
# Skill: update-extension-data
# Version: 0.1.0.0
# Purpose: Fetch latest files from all extension data sources, archive changed versions,
#          recopy snippets, re-run snippet analysis, update cache-manifest.json
# Usage: bash ~/.lsl-cache/skills/update-extension-data.sh
# Created: 2026-03-09
# Last modified: 2026-03-09

set -euo pipefail

CACHE_BASE="${LSL_CACHE_BASE:-$HOME/.lsl-cache}"
CACHE_ROOT="$CACHE_BASE"
EXT_DIR="$CACHE_ROOT/lsl-docs/vscode-extension-data"
MANIFEST="$CACHE_ROOT/cache-manifest.json"
TODAY=$(date +%Y-%m-%d)

echo "update-extension-data v0.1.0.0 — $TODAY"
echo

fetch_and_archive() {
    local url="$1"
    local dest="$2"
    local tmp; tmp=$(mktemp)
    mkdir -p "$(dirname "$dest")"

    if curl -fsSL "$url" -o "$tmp" 2>/dev/null; then
        if [ -f "$dest" ] && ! diff -q "$dest" "$tmp" > /dev/null 2>&1; then
            # Content changed — archive old version
            cp "$dest" "${dest}.${TODAY}"
            echo "  Archived: ${dest##*/} → ${dest##*/}.${TODAY}"
        fi
        mv "$tmp" "$dest"
        echo "  Fetched: $dest"
    else
        rm -f "$tmp"
        echo "  WARN: Failed to fetch $url"
    fi
}

fetch_any_and_archive() {
    local dest="$1"
    shift
    local url
    for url in "$@"; do
        local tmp; tmp=$(mktemp)
        mkdir -p "$(dirname "$dest")"
        if curl -fsSL "$url" -o "$tmp" 2>/dev/null; then
            if [ -f "$dest" ] && ! diff -q "$dest" "$tmp" > /dev/null 2>&1; then
                cp "$dest" "${dest}.${TODAY}"
                echo "  Archived: ${dest##*/} → ${dest##*/}.${TODAY}"
            fi
            mv "$tmp" "$dest"
            echo "  Fetched: $dest"
            echo "    via: $url"
            return 0
        fi
        rm -f "$tmp"
    done
    echo "  WARN: Failed to fetch any candidate for ${dest##*/}"
    return 1
}

echo "── Source 1: jyaoma/vscode-lsl ──────────────────────────────────"
BASE="https://raw.githubusercontent.com/jyaoma/vscode-lsl/lsp"
fetch_any_and_archive "$EXT_DIR/jyaoma/functions.json" \
    "$BASE/functions.json" \
    "$BASE/language/functions.json"
fetch_any_and_archive "$EXT_DIR/jyaoma/events.json" \
    "$BASE/events.json" \
    "$BASE/language/events.json"
fetch_any_and_archive "$EXT_DIR/jyaoma/constants.json" \
    "$BASE/constants.json" \
    "$BASE/language/constants.json"
fetch_any_and_archive "$EXT_DIR/jyaoma/snippets.json" \
    "$BASE/snippets.json" \
    "$BASE/snippets/snippets.json" \
    "https://raw.githubusercontent.com/jyaoma/vscode-lsl/master/snippets/snippets.json"

echo
echo "── Source 2: Sei-Lisa/kwdb ──────────────────────────────────────"
fetch_any_and_archive "$EXT_DIR/kwdb/kwdb.xml" \
    "https://raw.githubusercontent.com/Sei-Lisa/kwdb/master/database/kwdb.xml" \
    "https://raw.githubusercontent.com/Sei-Lisa/kwdb/master/kwdb.xml"

echo
echo "── Source 3: Sei-Lisa/LSL-PyOptimizer ──────────────────────────"
BASE="https://raw.githubusercontent.com/Sei-Lisa/LSL-PyOptimizer/master"
fetch_and_archive "$BASE/fndata.txt"   "$EXT_DIR/pyoptimizer/fndata.txt"
fetch_and_archive "$BASE/builtins.txt" "$EXT_DIR/pyoptimizer/builtins.txt"

echo
echo "── Source 4: Makopo/sublime-text-tooltip-lsl ────────────────────"
fetch_and_archive \
    "https://raw.githubusercontent.com/Makopo/sublime-text-tooltip-lsl/master/tooltipdata.json" \
    "$EXT_DIR/makopo/tooltipdata.json"

echo
echo "── Source 5: buildersbrewery/linden-scripting-language ─────────"
BASE="https://raw.githubusercontent.com/buildersbrewery/linden-scripting-language/master"
fetch_and_archive "$BASE/vscode/.vscode/extensions/LSL/syntaxes/LSL.tmLanguage.json" \
    "$EXT_DIR/buildersbrewery/LSL.tmLanguage.json"
fetch_and_archive "$BASE/vscode/.vscode/extensions/LSL/snippets/lsl.json" \
    "$EXT_DIR/buildersbrewery/lsl.json"

echo
echo "── Re-running snippet analysis ──────────────────────────────────"
if command -v python3 &>/dev/null; then
    if ! python3 "$CACHE_ROOT/skills/analyse-snippets.py"; then
        echo "  WARN: snippet analysis failed — continuing update."
    fi
else
    echo "  WARN: python3 not found — skipping snippet analysis. Run manually."
fi

echo
echo "── Updating cache manifest ──────────────────────────────────────"
if command -v python3 &>/dev/null; then
    MANIFEST_PY="$MANIFEST"
    if command -v cygpath &>/dev/null; then
        MANIFEST_PY="$(cygpath -w "$MANIFEST")"
    fi
    if ! python3 - <<EOF
import json, pathlib
p = pathlib.Path(r"""$MANIFEST_PY""")
if p.exists():
    raw = p.read_text(encoding="utf-8").strip()
    try:
        m = json.loads(raw) if raw else {}
    except Exception:
        m = {}
else:
    m = {}
m["last_updated"] = "$TODAY"
sources = m.setdefault("extension_sources", {})
for s in ["jyaoma", "kwdb", "pyoptimizer", "makopo", "buildersbrewery"]:
    sources[s] = "$TODAY"
p.write_text(json.dumps(m, indent=2), encoding="utf-8")
print("  Manifest updated.")
EOF
    then
        echo "  WARN: manifest update failed — continuing update."
    fi
fi

echo
echo "Done. Run 'update docs' to also refresh wiki documentation."
