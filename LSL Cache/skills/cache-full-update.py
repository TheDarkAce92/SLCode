#!/usr/bin/env python3
# Skill: cache-full-update
# Version: 0.1.0.0
# Purpose: Orchestrate a full local cache rebuild (no web requests)
# Usage: python3 cache-full-update.py [--skip-repair] [--skip-docs] [--skip-patterns]
# Created: 2026-03-10
# Last modified: 2026-03-10

"""
Runs all local cache update steps in the correct order:
  1. generate-docs-from-cache.py  -- synthesise missing function/event doc files
  2. lsl-cache-repair.py          -- fill empty front matter fields
  3. analyse-snippets.py          -- rebuild pattern library from extension data

No web requests are made. Use fetch-ossl-docs.py / fetch-slua-docs.py /
scrape-wiki-pages.py for web content updates.

Each step streams its own output with a clear header.
"""

import io
import os
import subprocess
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

_frozen = getattr(sys, "frozen", False)
SKILLS  = Path(__file__).resolve().parent


def _skill_cmd(name: str, *args) -> list:
    """Build the right command to invoke a skill whether frozen or not."""
    if _frozen:
        return [sys.executable, "run-skill", name] + list(args)
    return [sys.executable, str(SKILLS / f"{name}.py")] + list(args)

SKIP_REPAIR   = "--skip-repair"   in sys.argv
SKIP_DOCS     = "--skip-docs"     in sys.argv
SKIP_PATTERNS = "--skip-patterns" in sys.argv


def run_step(label: str, cmd: list) -> int:
    """Run a subprocess step, streaming output with a header. Returns exit code."""
    print(f"\n{'='*60}")
    print(f"  STEP: {label}")
    print(f"{'='*60}", flush=True)
    try:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        for line in proc.stdout:
            print(line, end="", flush=True)
        proc.wait()
        status = "OK" if proc.returncode == 0 else f"FAILED (exit {proc.returncode})"
        print(f"\n  [{label}] {status}", flush=True)
        return proc.returncode
    except FileNotFoundError as e:
        print(f"  [error] Could not run step: {e}", flush=True)
        return 1


steps = []

if not SKIP_DOCS:
    steps.append((
        "Generate docs from cache",
        _skill_cmd("generate-docs-from-cache", "--type", "all"),
    ))

if not SKIP_REPAIR:
    steps.append((
        "Repair front matter",
        _skill_cmd("lsl-cache-repair", "--category", "all"),
    ))

if not SKIP_PATTERNS:
    steps.append((
        "Analyse snippets / rebuild pattern library",
        _skill_cmd("analyse-snippets"),
    ))

print(f"Cache Full Update — {len(steps)} step(s) queued")

results = {}
for label, cmd in steps:
    rc = run_step(label, cmd)
    results[label] = rc

print(f"\n{'='*60}")
print("  FULL UPDATE SUMMARY")
print(f"{'='*60}")
all_ok = True
for label, rc in results.items():
    status = "OK" if rc == 0 else f"FAILED ({rc})"
    print(f"  {'OK' if rc==0 else 'FAIL'}  {label}")
    if rc != 0:
        all_ok = False

print()
if all_ok:
    print("  All steps completed successfully.")
else:
    print("  One or more steps failed — check output above.")
    sys.exit(1)
