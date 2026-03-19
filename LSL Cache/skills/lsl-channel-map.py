# Skill: lsl-channel-map
# Version: 0.1.0.0
# Purpose: Map all communication channels used in an LSL script
# Usage: python3 lsl-channel-map.py <script.lsl>
# Created: 2026-03-10
# Last modified: 2026-03-10

"""
Scans LSL source for all communication-related function calls and maps them
to their channels. Useful for identifying channel conflicts, PUBLIC_CHANNEL
usage, and listener cleanup issues.
"""

import re
import sys
from pathlib import Path

# LSL communication functions and the 0-based index of their channel argument.
# None means the function has no channel argument.
CHANNEL_FUNCS = {
    "llListen":       0,
    "llSay":          0,
    "llWhisper":      0,
    "llShout":        0,
    "llRegionSay":    0,
    "llRegionSayTo":  1,   # (key target, integer channel, string msg)
    "llDialog":       2,   # (key avatar, string msg, list buttons, integer channel) — actually index 3
}

# llDialog channel is the 4th argument (index 3)
CHANNEL_FUNCS["llDialog"] = 3

WELL_KNOWN = {
    0:  "PUBLIC_CHANNEL",
    -1: "DEBUG_CHANNEL",
}


def strip_comments(source: str) -> list:
    result   = []
    in_block = False
    for i, line in enumerate(source.splitlines(), 1):
        s = line
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


def extract_nth_arg(after_paren: str, n: int) -> str:
    """Extract the nth (0-based) comma-separated argument from a function call body."""
    depth   = 0
    current = []
    arg_idx = 0
    for ch in after_paren:
        if ch in "({[":
            depth += 1
            current.append(ch)
        elif ch in ")}]":
            if depth == 0:
                break
            depth -= 1
            current.append(ch)
        elif ch == ',' and depth == 0:
            if arg_idx == n:
                return "".join(current).strip()
            arg_idx += 1
            current = []
        else:
            current.append(ch)
    if arg_idx == n:
        return "".join(current).strip()
    return ""


def resolve_channel(raw: str):
    """Try to resolve a channel expression to an integer. Returns (int|None, label_str)."""
    raw = raw.strip()
    aliases = {
        "PUBLIC_CHANNEL": 0,
        "DEBUG_CHANNEL":  -1,
    }
    if raw in aliases:
        return aliases[raw], raw
    m = re.match(r'^(0x[0-9a-fA-F]+)$', raw)
    if m:
        return int(raw, 16), raw
    m = re.match(r'^-?\d+$', raw)
    if m:
        return int(raw), raw
    return None, raw


def channel_map_file(filepath: str) -> dict:
    """Map all communication channels in LSL file at `filepath`."""
    try:
        source = Path(filepath).read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        return {"error": str(e)}
    return channel_map_source(source)


def channel_map_source(source: str) -> dict:
    lines = strip_comments(source)
    calls      = []
    by_channel = {}

    func_pattern = re.compile(
        r'\b(' + '|'.join(re.escape(f) for f in CHANNEL_FUNCS) + r')\s*\('
    )

    for lineno, line in lines:
        for m in func_pattern.finditer(line):
            func_name = m.group(1)
            chan_pos  = CHANNEL_FUNCS[func_name]
            after     = line[m.end():]
            raw       = extract_nth_arg(after, chan_pos)
            val, label = resolve_channel(raw)

            well_known = WELL_KNOWN.get(val, "")
            if well_known and label != well_known:
                label = f"{raw} ({well_known})"
            elif not label:
                label = raw

            entry = {
                "func":        func_name,
                "line":        lineno,
                "channel":     val,
                "channel_raw": raw,
                "label":       label,
                "note":        well_known or ("dynamic" if val is None else ""),
            }
            calls.append(entry)
            if val is not None:
                by_channel.setdefault(val, []).append(entry)

    unique_resolved = sorted(by_channel.keys())

    warnings = []
    if 0 in by_channel:
        output_funcs = [e["func"] for e in by_channel[0]
                        if e["func"] not in ("llListen",)]
        if output_funcs:
            warnings.append(
                f"PUBLIC_CHANNEL (0) used for output in: "
                f"{', '.join(sorted(set(output_funcs)))} — consider a private channel."
            )
    listens = [c for c in calls if c["func"] == "llListen"]
    if len(listens) > 4:
        warnings.append(
            f"{len(listens)} llListen calls — remember max 64 active listeners per script."
        )

    return {
        "calls":           calls,
        "by_channel":      {str(k): v for k, v in by_channel.items()},
        "unique_channels": unique_resolved,
        "warnings":        warnings,
        "total_calls":     len(calls),
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 lsl-channel-map.py <script.lsl>")
        sys.exit(1)
    result = channel_map_file(sys.argv[1])
    if "error" in result:
        print(f"Error: {result['error']}")
        sys.exit(1)
    print(f"Channel map: {result['total_calls']} calls, {len(result['unique_channels'])} unique channels")
    for ch in result["unique_channels"]:
        label   = WELL_KNOWN.get(ch, f"ch {ch}")
        entries = result["by_channel"][str(ch)]
        funcs   = ", ".join(f"{e['func']}:{e['line']}" for e in entries)
        print(f"  [{ch:>12}] {label:<22} {funcs}")
    if result["warnings"]:
        print("\nWarnings:")
        for w in result["warnings"]:
            print(f"  WARNING: {w}")
