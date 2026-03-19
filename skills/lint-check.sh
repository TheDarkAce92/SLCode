#!/usr/bin/env bash
# Skill: lint-check
# Version: 0.1.0.0
# Purpose: Run LSLint across all project scripts in /src/
# Usage: bash skills/lint-check.sh [optional: path/to/script.lsl]
# Created: 2026-03-09
# Last modified: 2026-03-09

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
SRC_DIR="$PROJECT_ROOT/src"

if command -v lslint &>/dev/null; then
    USE_EXTERNAL=1
else
    USE_EXTERNAL=0
fi

run_builtin_lint() {
    local target_file="$1"
    local py="${PROJECT_ROOT}/.venv/Scripts/python.exe"
    if [ ! -x "$py" ]; then
        py="python3"
    fi

    "$py" - <<'PY' "$PROJECT_ROOT" "$target_file"
import importlib.util
import os
import sys
from pathlib import Path

project_root = Path(sys.argv[1])
target = Path(sys.argv[2])
lint_path = project_root / "LSL Cache" / "skills" / "lsl-lint-compat.py"
if not lint_path.exists():
    print(f"ERROR: built-in lint checker not found at {lint_path}")
    sys.exit(1)

spec = importlib.util.spec_from_file_location("lsl_lint_compat", str(lint_path))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
issues = mod.check_file(str(target))

if not issues:
    print("No lint issues.")
    sys.exit(0)

for sev, code, line, msg in issues:
    print(f"[{sev}] {code} L{line}: {msg}")
PY
}

if [ -n "$1" ]; then
    # Lint a specific file
    echo "Linting: $1"
    if [ "$USE_EXTERNAL" -eq 1 ]; then
        lslint "$1"
    else
        echo "lslint not found; using built-in lint-compat checker"
        run_builtin_lint "$1"
    fi
else
    # Lint all .lsl files in /src/
    FOUND=0
    while IFS= read -r -d '' file; do
        echo "── $file"
        if [ "$USE_EXTERNAL" -eq 1 ]; then
            lslint "$file"
        else
            run_builtin_lint "$file"
        fi
        FOUND=$((FOUND + 1))
    done < <(find "$SRC_DIR" -name "*.lsl" -print0 2>/dev/null)

    if [ "$FOUND" -eq 0 ]; then
        echo "No .lsl files found in $SRC_DIR"
    else
        if [ "$USE_EXTERNAL" -eq 1 ]; then
            echo "Linted $FOUND script(s) with lslint."
        else
            echo "Linted $FOUND script(s) with built-in lint-compat checker."
        fi
    fi
fi
