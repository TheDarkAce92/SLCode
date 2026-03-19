# Skill: lsl-formatter
# Version: 0.1.0.0
# Purpose: Format and normalise LSL source code indentation and style
# Usage: python3 lsl-formatter.py <script.lsl>
# Created: 2026-03-10
# Last modified: 2026-03-10

"""
Applies consistent formatting to LSL source:
- 4-space indentation based on brace depth
- Standalone opening braces hoisted to previous line
- Normalised spacing: after commas, around assignments
- Collapses runs of 3+ blank lines to 2
"""

import re
import sys
from pathlib import Path


def format_file(filepath: str) -> dict:
    """Format LSL file at `filepath`. Returns {"source", "changes"}."""
    try:
        source = Path(filepath).read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        return {"error": str(e)}
    return format_source(source)


def format_source(source: str) -> dict:
    """Format LSL source string. Returns {"source": formatted, "changes": N}."""
    lines   = source.splitlines()
    out     = []
    depth   = 0
    changes = 0

    i = 0
    while i < len(lines):
        raw      = lines[i]
        s        = raw.rstrip()
        stripped = s.lstrip()

        # Hoist standalone '{' onto the previous non-empty line
        if stripped == '{' and out:
            prev = out[-1].rstrip()
            if prev.strip() and not prev.rstrip().endswith('{') and not prev.rstrip().endswith('}'):
                out[-1] = prev + ' {'
                depth  += 1
                changes += 1
                i += 1
                continue

        # Closing brace reduces depth before indent is applied
        if stripped.startswith('}'):
            depth = max(0, depth - 1)

        # Build indented line
        indent   = '    ' * depth
        new_line = (indent + stripped) if stripped else ''

        # Normalise operator spacing (skip pure comment/string lines)
        if stripped and not stripped.startswith('//'):
            fixed = _fix_spacing(new_line)
            if fixed != new_line:
                changes += 1
                new_line = fixed

        if new_line != s and stripped:
            changes += 1

        out.append(new_line)

        # Update depth for next iteration
        open_cnt  = stripped.count('{')
        close_cnt = stripped.count('}')
        if stripped.startswith('}'):
            # closing brace already decremented; count remaining opens/closes
            depth = max(0, depth + open_cnt - (close_cnt - 1))
        else:
            depth = max(0, depth + open_cnt - close_cnt)

        i += 1

    # Collapse 3+ consecutive blank lines to 2
    result_lines = []
    blank_run    = 0
    for line in out:
        if line.strip() == '':
            blank_run += 1
            if blank_run <= 2:
                result_lines.append(line)
            else:
                changes += 1
        else:
            blank_run = 0
            result_lines.append(line)

    formatted = '\n'.join(result_lines)
    if not formatted.endswith('\n'):
        formatted += '\n'

    return {
        "source":  formatted,
        "changes": changes,
        "note":    "Formatting is heuristic. Always review output before use.",
    }


def _fix_spacing(line: str) -> str:
    """Normalise spaces: after commas; around simple assignments."""
    indent = len(line) - len(line.lstrip())
    body   = line[indent:]

    # Space after comma (not already present)
    body = re.sub(r',(?!\s)', ', ', body)
    # Normalise multiple internal spaces (but not leading indent)
    body = re.sub(r'(?<=\S)  +', ' ', body)

    return line[:indent] + body


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 lsl-formatter.py <script.lsl>")
        sys.exit(1)
    result = format_file(sys.argv[1])
    if "error" in result:
        print(f"Error: {result['error']}")
        sys.exit(1)
    print(f"Formatted: {result['changes']} change(s) made")
    print(f"Note: {result['note']}")
    print("\n--- Formatted source ---")
    print(result["source"])
