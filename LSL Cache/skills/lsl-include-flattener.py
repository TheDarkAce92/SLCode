# Skill: lsl-include-flattener
# Version: 0.1.0.0
# Purpose: Flatten Firestorm preprocessor #include directives in LSL scripts
# Usage: python3 lsl-include-flattener.py <script.lsl>
# Created: 2026-03-10
# Last modified: 2026-03-10

"""
Resolves and inlines all #include "file.lsl" directives in a
Firestorm-preprocessor LSL script. Produces a single merged source string.
Handles recursive includes and detects circular dependencies.
"""

import re
import sys
from pathlib import Path


def flatten_file(filepath: str) -> dict:
    """Flatten all #include directives in LSL file at `filepath`."""
    p = Path(filepath)
    if not p.exists():
        return {"error": f"File not found: {filepath}"}
    try:
        source = p.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        return {"error": str(e)}
    return _flatten(source, p.parent, set(), [])


def flatten_source(source: str, base_dir: str = ".") -> dict:
    """Flatten a source string, resolving includes relative to base_dir."""
    return _flatten(source, Path(base_dir), set(), [])


def _flatten(source: str, base_dir: Path, seen: set, included: list) -> dict:
    """Recursive flatten with cycle detection."""
    result_lines = []
    warnings     = []

    for i, line in enumerate(source.splitlines(), 1):
        m = re.match(r'^\s*#\s*include\s+"([^"]+)"', line)
        if not m:
            result_lines.append(line)
            continue

        inc_rel  = m.group(1)
        inc_path = (base_dir / inc_rel).resolve()
        inc_str  = str(inc_path)

        if inc_str in seen:
            warnings.append(f"Circular include: {inc_rel} (line {i})")
            result_lines.append(f"// [circular include skipped: {inc_rel}]")
            continue

        if not inc_path.exists():
            warnings.append(f"Include not found: {inc_rel} (line {i})")
            result_lines.append(f"// [include not found: {inc_rel}]")
            continue

        try:
            inc_source = inc_path.read_text(encoding="utf-8", errors="replace")
        except Exception as e:
            warnings.append(f"Could not read {inc_rel}: {e}")
            result_lines.append(f"// [include read error: {inc_rel}]")
            continue

        seen.add(inc_str)
        included.append(str(inc_path))
        result_lines.append(f"// === begin include: {inc_rel} ===")
        sub = _flatten(inc_source, inc_path.parent, seen, included)
        result_lines.append(sub["source"])
        result_lines.append(f"// === end include: {inc_rel} ===")
        warnings.extend(sub.get("warnings", []))

    return {
        "source":         "\n".join(result_lines),
        "files_included": list(included),
        "warnings":       warnings,
        "include_count":  len(included),
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 lsl-include-flattener.py <script.lsl>")
        sys.exit(1)
    result = flatten_file(sys.argv[1])
    if "error" in result:
        print(f"Error: {result['error']}")
        sys.exit(1)
    print(f"Flattened: {result['include_count']} include(s) resolved")
    for f in result["files_included"]:
        print(f"  + {f}")
    if result["warnings"]:
        print("Warnings:")
        for w in result["warnings"]:
            print(f"  WARNING: {w}")
    print("\n--- Flattened source ---")
    print(result["source"])
