# Skill: lsl-sleep-profiler
# Version: 0.1.0.0
# Purpose: Profile forced sleep / delay functions in LSL scripts
# Usage: python3 lsl-sleep-profiler.py <script.lsl>
# Created: 2026-03-10
# Last modified: 2026-03-10

"""
Scans LSL source for forced-sleep function calls (functions with a mandatory
delay per pyoptimizer fndata.txt), reports total delay per event handler,
and flags performance issues.
"""

import os
import re
import sys
from pathlib import Path

_env_base  = os.environ.get("LSL_CACHE_BASE", "").strip()
CACHE_ROOT = Path(_env_base) if _env_base else Path(__file__).resolve().parents[1]
FNDATA_PATH = CACHE_ROOT / "lsl-docs" / "vscode-extension-data" / "pyoptimizer" / "fndata.txt"

LSL_EVENTS = {
    "state_entry", "state_exit", "touch_start", "touch", "touch_end",
    "collision_start", "collision", "collision_end", "land_collision_start",
    "land_collision", "land_collision_end", "timer", "listen", "sensor",
    "no_sensor", "control", "money", "email", "at_target", "not_at_target",
    "at_rot_target", "not_at_rot_target", "run_time_permissions",
    "changed", "attach", "dataserver", "moving_start", "moving_end",
    "link_message", "on_rez", "object_rez", "remote_data", "http_response",
    "http_request", "path_update", "transaction_result",
    "experience_permissions", "experience_permissions_denied", "game_control",
}


def load_sleep_data() -> dict:
    """Parse fndata.txt and return {function_name: sleep_seconds} for delayed funcs."""
    delays = {}
    if not FNDATA_PATH.exists():
        return delays
    try:
        text = FNDATA_PATH.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return delays
    current_func = None
    for line in text.splitlines():
        line = line.strip()
        m = re.match(r'^(?:\w+)\s+(\w+)\s*\(', line)
        if m and not line.startswith('-'):
            current_func = m.group(1)
        elif line.startswith('- delay') and current_func:
            dm = re.match(r'^- delay\s+([\d.]+)', line)
            if dm:
                delays[current_func] = float(dm.group(1))
    return delays


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


def get_event_ranges(cleaned_lines: list) -> list:
    """Return list of {name, start_line, end_line} for each event handler found."""
    events        = []
    depth         = 0
    current_event = None
    event_start   = None
    event_depth   = None

    for lineno, line in cleaned_lines:
        stripped = line.strip()

        if current_event is None:
            m = re.match(r'^(\w+)\s*\(', stripped)
            if m and m.group(1) in LSL_EVENTS:
                current_event = m.group(1)
                event_start   = lineno
                event_depth   = depth

        open_cnt  = line.count('{')
        close_cnt = line.count('}')
        depth = max(0, depth + open_cnt - close_cnt)

        if current_event is not None:
            if depth <= event_depth and (open_cnt > 0 or close_cnt > 0) and close_cnt > 0:
                events.append({
                    "name":       current_event,
                    "start_line": event_start,
                    "end_line":   lineno,
                })
                current_event = None
                event_start   = None
                event_depth   = None

    return events


def profile_file(filepath: str) -> dict:
    """Profile forced delays in LSL file at `filepath`."""
    try:
        source = Path(filepath).read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        return {"error": str(e)}
    return profile_source(source)


def profile_source(source: str) -> dict:
    sleep_data   = load_sleep_data()
    cleaned      = strip_comments(source)
    event_ranges = get_event_ranges(cleaned)

    all_calls    = []
    func_pattern = re.compile(r'\b(\w+)\s*\(')

    for lineno, line in cleaned:
        for m in func_pattern.finditer(line):
            fn = m.group(1)
            if fn not in sleep_data:
                continue
            duration = sleep_data[fn]
            # For llSleep specifically, try to read the argument
            if fn == "llSleep":
                after   = line[m.end():]
                raw_arg = ""
                dep     = 0
                for ch in after:
                    if ch == '(':
                        dep += 1
                    elif ch == ')':
                        if dep == 0:
                            break
                        dep -= 1
                    elif ch == ',' and dep == 0:
                        break
                    else:
                        raw_arg += ch
                try:
                    duration = float(raw_arg.strip())
                except (ValueError, AttributeError):
                    pass
            all_calls.append({
                "func":     fn,
                "line":     lineno,
                "delay":    duration,
                "in_event": None,
            })

    # Assign each call to its enclosing event handler
    for call in all_calls:
        for ev in event_ranges:
            if ev["start_line"] <= call["line"] <= ev["end_line"]:
                call["in_event"] = ev["name"]
                break

    # Group by event
    by_event = {}
    for call in all_calls:
        ev = call["in_event"] or "(global/unknown)"
        by_event.setdefault(ev, {"calls": [], "total_delay": 0.0})
        by_event[ev]["calls"].append(call)
        by_event[ev]["total_delay"] = round(by_event[ev]["total_delay"] + call["delay"], 3)

    # Warnings
    warnings = []
    if "timer" in by_event and by_event["timer"]["total_delay"] > 0:
        warnings.append(
            f"timer event has {by_event['timer']['total_delay']}s of forced delay "
            f"— timer callbacks should be fast; consider timer-driven state machines."
        )
    llsleep_calls = [c for c in all_calls if c["func"] == "llSleep"]
    if llsleep_calls:
        warnings.append(
            f"llSleep used {len(llsleep_calls)} time(s) — "
            f"consider timer events or state transitions instead."
        )

    total_delay = round(sum(c["delay"] for c in all_calls), 3)

    return {
        "calls":            all_calls,
        "by_event":         by_event,
        "total_delay":      total_delay,
        "warnings":         warnings,
        "functions_loaded": len(sleep_data),
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 lsl-sleep-profiler.py <script.lsl>")
        sys.exit(1)
    result = profile_file(sys.argv[1])
    if "error" in result:
        print(f"Error: {result['error']}")
        sys.exit(1)
    print(f"Sleep profile: {result['total_delay']}s total · {len(result['calls'])} delayed calls "
          f"· {result['functions_loaded']} functions with known delays")
    for ev, info in result["by_event"].items():
        print(f"\n  [{ev}]  total: {info['total_delay']}s")
        for c in info["calls"]:
            print(f"    L{c['line']:4d}  {c['func']}  {c['delay']}s")
    if result["warnings"]:
        print("\nWarnings:")
        for w in result["warnings"]:
            print(f"  WARNING: {w}")
