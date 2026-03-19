#!/usr/bin/env python3
# Skill: lsl-lint-compat
# Version: 0.1.0.0
# Purpose: Built-in LSLint-style checks for SLCode (no external lslint dependency)
# Usage: Imported by search-cache.py via run_checks(source, mode)
# Created: 2026-03-15
# Last modified: 2026-03-15

from __future__ import annotations

import re
from pathlib import Path


EVENT_RE = re.compile(r"^\s*([A-Za-z_]\w*)\s*\([^;{}]*\)\s*\{\s*$")
STATE_RE = re.compile(r"^\s*state\s+([A-Za-z_]\w*)\s*\{\s*$")
DEFAULT_RE = re.compile(r"^\s*default\s*\{\s*$")
LINE_MAX = 120


def load_known_functions() -> set[str]:
    """Optional compatibility hook expected by search-cache preload logic."""
    return set()


def _detect_missing_default(lines: list[str]) -> list[tuple[str, str, int, str]]:
    for i, line in enumerate(lines, 1):
        if DEFAULT_RE.match(line):
            return []
    return [("ERROR", "LINT004", 1, "Script is missing a default state block")]


def _line_style_checks(lines: list[str]) -> list[tuple[str, str, int, str]]:
    issues: list[tuple[str, str, int, str]] = []
    for i, line in enumerate(lines, 1):
        if "\t" in line:
            issues.append(("WARN", "LINT001", i,
                "Tab character found; prefer spaces for stable formatting"))
        if line.rstrip("\n").rstrip("\r").endswith(" "):
            issues.append(("WARN", "LINT002", i,
                "Trailing whitespace"))
        if len(line.rstrip("\n\r")) > LINE_MAX:
            issues.append(("WARN", "LINT003", i,
                f"Line length exceeds {LINE_MAX} characters"))
    return issues


def _state_and_event_checks(lines: list[str]) -> list[tuple[str, str, int, str]]:
    issues: list[tuple[str, str, int, str]] = []
    state_stack: list[str] = []
    brace_depth = 0
    state_events: dict[str, dict[str, int]] = {}
    state_first_line: dict[str, int] = {}

    for i, raw in enumerate(lines, 1):
        line = raw.strip()
        if not line or line.startswith("//"):
            brace_depth += raw.count("{") - raw.count("}")
            if brace_depth < 0:
                brace_depth = 0
            continue

        m_default = DEFAULT_RE.match(raw)
        m_state = STATE_RE.match(raw)
        if m_default:
            state_name = "default"
            if state_name in state_first_line:
                issues.append(("ERROR", "LINT005", i,
                    "Duplicate state 'default'"))
            else:
                state_first_line[state_name] = i
            state_stack.append(state_name)
            state_events.setdefault(state_name, {})
        elif m_state:
            state_name = m_state.group(1)
            if state_name in state_first_line:
                issues.append(("ERROR", "LINT005", i,
                    f"Duplicate state '{state_name}'"))
            else:
                state_first_line[state_name] = i
            state_stack.append(state_name)
            state_events.setdefault(state_name, {})
        else:
            if state_stack:
                em = EVENT_RE.match(raw)
                if em:
                    event_name = em.group(1)
                    current_state = state_stack[-1]
                    first = state_events[current_state].get(event_name)
                    if first:
                        issues.append(("ERROR", "LINT006", i,
                            f"Duplicate event handler '{event_name}' in state '{current_state}' (first at line {first})"))
                    else:
                        state_events[current_state][event_name] = i

        opens = raw.count("{")
        closes = raw.count("}")
        brace_depth += opens - closes
        if closes > opens and state_stack:
            pop_count = min(len(state_stack), closes - opens)
            for _ in range(pop_count):
                state_stack.pop()
        if brace_depth < 0:
            brace_depth = 0

    return issues


def _runtime_risk_checks(lines: list[str]) -> list[tuple[str, str, int, str]]:
    issues: list[tuple[str, str, int, str]] = []
    say_re = re.compile(r"\b(llSay|llShout|llRegionSay)\s*\(\s*(-?\d+)")
    sleep_re = re.compile(r"\bllSleep\s*\(")

    for i, raw in enumerate(lines, 1):
        line = raw.strip()
        if not line or line.startswith("//"):
            continue

        m_say = say_re.search(raw)
        if m_say:
            fn = m_say.group(1)
            ch = int(m_say.group(2))
            if ch > 0:
                issues.append(("WARN", "LINT007", i,
                    f"{fn} uses positive chat channel {ch}; prefer negative/private channels"))

        if sleep_re.search(raw):
            issues.append(("WARN", "LINT008", i,
                "llSleep can stall script responsiveness; prefer timer/state design when possible"))

    return issues


def check_file(path: str | Path, *_args, **_kwargs) -> list[tuple[str, str, int, str]]:
    """Return list of issues as (severity, code, line, message)."""
    p = Path(path)
    src = p.read_text(encoding="utf-8", errors="replace")
    lines = src.splitlines()

    issues: list[tuple[str, str, int, str]] = []
    issues += _line_style_checks(lines)
    issues += _detect_missing_default(lines)
    issues += _state_and_event_checks(lines)
    issues += _runtime_risk_checks(lines)

    dedup = []
    seen = set()
    for sev, code, line, msg in issues:
        key = (code, line, msg)
        if key in seen:
            continue
        seen.add(key)
        dedup.append((sev, code, line, msg))
    return dedup
