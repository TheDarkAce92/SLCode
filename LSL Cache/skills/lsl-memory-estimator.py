# Skill: lsl-memory-estimator
# Version: 0.1.0.0
# Purpose: Estimate memory footprint of an LSL script
# Usage: python3 lsl-memory-estimator.py <script.lsl>
# Created: 2026-03-10
# Last modified: 2026-03-10

"""
Estimates memory usage of an LSL script.
- Globals/local variable count by type
- Rough heap estimate in bytes
- Warning flags near LSL limits
"""

import re
import sys
from pathlib import Path

# LSL type memory sizes (approximate, Mono runtime)
TYPE_SIZES = {
    "integer":  4,
    "float":    4,
    "key":      36,
    "vector":   12,
    "rotation": 16,
    "string":   56,    # overhead; content adds ~1B/char
    "list":     64,    # overhead; each entry ~32B average
}

LSL_HEAP_LIMIT    = 256 * 1024
LSL_WARN_THRESHOLD = 0.8


def strip_comments(source: str) -> list:
    """Return list of (lineno, stripped_line) with comments removed."""
    result   = []
    in_block = False
    for i, raw in enumerate(source.splitlines(), 1):
        s = raw
        if in_block:
            end = s.find("*/")
            if end == -1:
                result.append((i, ""))
                continue
            s = s[end + 2:]
            in_block = False
        s = re.sub(r'//.*', '', s)
        while True:
            m = re.search(r'/\*.*?\*/', s)
            if not m:
                break
            s = s[:m.start()] + s[m.end():]
        bc = s.find("/*")
        if bc != -1:
            s = s[:bc]
            in_block = True
        result.append((i, s))
    return result


def estimate_file(filepath: str) -> dict:
    """Estimate memory footprint of LSL file at `filepath`."""
    try:
        source = Path(filepath).read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        return {"error": str(e)}
    return estimate_source(source)


def estimate_source(source: str) -> dict:
    """Estimate memory footprint from raw LSL source string."""
    cleaned_lines = strip_comments(source)

    items = []
    depth = 0

    for lineno, line in cleaned_lines:
        stripped = line.strip()

        # Adjust depth: closing braces reduce depth BEFORE we apply to scope
        if stripped.startswith('}'):
            depth = max(0, depth - 1)

        scope = "global" if depth == 0 else "local"

        # Match variable declarations
        for typ in TYPE_SIZES:
            m = re.match(r'\b(' + typ + r')\s+([a-zA-Z_]\w*)\s*[=;(]', stripped)
            if m:
                # Make sure it's a declaration, not a cast or parameter
                var_name = m.group(2)
                sz   = TYPE_SIZES[typ]
                note = ""
                if typ == "string":
                    str_m = re.search(r'"([^"]*)"', line)
                    if str_m:
                        sz  += len(str_m.group(1))
                        snip = str_m.group(1)[:20]
                        note = f'init string ~{sz}B'
                elif typ == "list":
                    ls_m = re.search(r'\[([^\]]*)\]', line)
                    if ls_m:
                        n_items = len([x for x in ls_m.group(1).split(',') if x.strip()])
                        sz   = 64 + n_items * 32
                        note = f"~{n_items} items"
                items.append({
                    "name":       var_name,
                    "type":       typ,
                    "scope":      scope,
                    "line":       lineno,
                    "size_bytes": sz,
                    "note":       note,
                })
                break

        # Update depth for next line
        open_cnt  = line.count('{')
        close_cnt = line.count('}')
        if stripped.startswith('}'):
            depth += open_cnt          # closing already handled above
        else:
            depth = max(0, depth + open_cnt - close_cnt)

    global_bytes = sum(it["size_bytes"] for it in items if it["scope"] == "global")
    local_bytes  = sum(it["size_bytes"] for it in items if it["scope"] == "local")

    # Rough bytecode estimate: ~8 bytes per non-blank line of code
    loc = len([l for _, l in cleaned_lines if l.strip()])
    bytecode_est = loc * 8

    total_est = global_bytes + local_bytes + bytecode_est
    pct       = total_est / LSL_HEAP_LIMIT * 100

    return {
        "items":         items,
        "globals_count": sum(1 for it in items if it["scope"] == "global"),
        "locals_count":  sum(1 for it in items if it["scope"] == "local"),
        "global_bytes":  global_bytes,
        "local_bytes":   local_bytes,
        "bytecode_est":  bytecode_est,
        "total_est":     total_est,
        "total_kb":      round(total_est / 1024, 1),
        "pct_heap":      round(pct, 1),
        "warning":       pct >= LSL_WARN_THRESHOLD * 100,
        "limit_kb":      256,
        "note":          "Estimates are approximate. Use llGetUsedMemory() in-world for accuracy.",
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 lsl-memory-estimator.py <script.lsl>")
        sys.exit(1)
    result = estimate_file(sys.argv[1])
    if "error" in result:
        print(f"Error: {result['error']}")
        sys.exit(1)
    print(f"Memory estimate: {result['total_kb']} KB / {result['limit_kb']} KB ({result['pct_heap']}%)")
    print(f"  Globals: {result['globals_count']} vars, {result['global_bytes']} bytes")
    print(f"  Locals:  {result['locals_count']} vars, {result['local_bytes']} bytes")
    print(f"  Bytecode est: {result['bytecode_est']} bytes")
    if result["warning"]:
        print("  WARNING: Approaching memory limit!")
    print(f"\n  Note: {result['note']}")
    for it in result["items"]:
        print(f"    L{it['line']:4d} [{it['scope']:6s}] {it['type']:8s} {it['name']:20s}  ~{it['size_bytes']}B  {it['note']}")
