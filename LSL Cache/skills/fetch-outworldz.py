#!/usr/bin/env python3
# Skill: fetch-outworldz
# Version: 0.3.0.0
# Purpose: Fetch all LSL scripts from outworldz.com/lib/ into lsl-docs/examples/
# Usage: python3 fetch-outworldz.py [--force] [--limit N] [--dry-run]
#                                   [--token=GHPAT] [--save-token] [--clear-token]
# Created: 2026-03-17
# Last modified: 2026-03-17

"""
outworldz.com/lib/ is a git-served mirror of github.com/Outworldz/LSL-Scripts.

Strategy:
  1. Use the GitHub tree API to get ALL file paths in one request.
  2. Filter to .lsl / .sl / .txt files.
  3. Download each from raw.githubusercontent.com.
  4. Save with YAML front matter to lsl-docs/examples/.

This approach makes ~1 API call to discover files instead of 3000+ HTTP
crawl requests, cutting total run time from ~20 min to ~2-3 min.

Source credit URL: https://outworldz.com/lib/<path> (the served web mirror).
"""

import hashlib
import io
import json
import os
import re
import ssl
import sys
import time
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# ── Config ────────────────────────────────────────────────────────────────────

_env_base  = os.environ.get("LSL_CACHE_BASE", "").strip()
CACHE_ROOT = Path(_env_base) if _env_base else Path(__file__).resolve().parents[1]
DOCS_DIR   = CACHE_ROOT / "lsl-docs"
OUT_DIR    = DOCS_DIR / "examples"
CHANGELOG  = DOCS_DIR / "CHANGELOG.md"
MANIFEST   = CACHE_ROOT / "cache-manifest.json"
TODAY      = date.today().isoformat()

FORCE       = "--force"       in sys.argv
DRY_RUN     = "--dry-run"     in sys.argv
SAVE_TOKEN  = "--save-token"  in sys.argv
CLEAR_TOKEN = "--clear-token" in sys.argv
LIMIT       = None
_CLI_TOKEN  = None
for a in sys.argv[1:]:
    if a.startswith("--limit="):
        LIMIT = int(a.split("=", 1)[1])
    elif a.startswith("--token="):
        _CLI_TOKEN = a.split("=", 1)[1].strip()

GH_OWNER  = "Outworldz"
GH_REPO   = "LSL-Scripts"
WEB_BASE  = "https://outworldz.com/lib/"
RAW_BASE  = f"https://raw.githubusercontent.com/{GH_OWNER}/{GH_REPO}"
API_BASE  = f"https://api.github.com/repos/{GH_OWNER}/{GH_REPO}"

SOURCE_NAME = "Outworldz Script Library"
RATE_DELAY  = 0.25   # seconds between download requests

LSL_EXTS = {".lsl", ".sl", ".lslp", ".lslm"}
TXT_EXT  = ".txt"

# Token config file — stored separately from cache-manifest so it's never
# accidentally committed or logged.
_TOKEN_FILE = CACHE_ROOT / ".gh-token"

OUT_DIR.mkdir(parents=True, exist_ok=True)

# ── GitHub token management ───────────────────────────────────────────────────

def _load_token() -> str:
    """
    Token priority (highest to lowest):
      1. --token=XXX on the command line
      2. GITHUB_TOKEN environment variable
      3. ~/.lsl-cache/.gh-token saved by --save-token
    Returns empty string if none found.
    """
    if _CLI_TOKEN:
        return _CLI_TOKEN
    env = os.environ.get("GITHUB_TOKEN", "").strip()
    if env:
        return env
    if _TOKEN_FILE.exists():
        try:
            return _TOKEN_FILE.read_text(encoding="utf-8").strip()
        except Exception:
            pass
    return ""


def _save_token(token: str):
    """Write token to .gh-token (chmod 600 on non-Windows)."""
    _TOKEN_FILE.write_text(token + "\n", encoding="utf-8")
    try:
        import stat
        _TOKEN_FILE.chmod(stat.S_IRUSR | stat.S_IWUSR)  # 0o600
    except Exception:
        pass


def _clear_token():
    if _TOKEN_FILE.exists():
        _TOKEN_FILE.unlink()
        print("Saved token cleared.", flush=True)
    else:
        print("No saved token found.", flush=True)


# ── HTTP ──────────────────────────────────────────────────────────────────────

_SSL_CTX = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
_SSL_CTX.check_hostname = False
_SSL_CTX.verify_mode    = ssl.CERT_NONE

GH_TOKEN = _load_token()

_HEADERS = {
    "Accept":     "text/html,text/plain,*/*",
    "User-Agent": "SLCode/1.0 LSL-cache-builder",
}
_GH_HEADERS = {
    "Accept":     "application/vnd.github+json",
    "User-Agent": "SLCode/1.0 LSL-cache-builder",
}
if GH_TOKEN:
    _GH_HEADERS["Authorization"] = f"Bearer {GH_TOKEN}"


def _get(url: str, headers: dict, timeout: int = 30) -> bytes | None:
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=_SSL_CTX) as r:
            return r.read()
    except Exception as e:
        print(f"  [fetch error] {url}: {e}", flush=True)
        return None


def fetch_text(url: str, timeout: int = 20) -> str:
    data = _get(url, _HEADERS, timeout)
    if data is None:
        return ""
    try:
        return data.decode("utf-8", errors="replace")
    except Exception:
        return ""


def fetch_json(url: str) -> dict | list | None:
    data = _get(url, _GH_HEADERS)
    if data is None:
        return None
    try:
        return json.loads(data)
    except Exception:
        return None


# ── GitHub tree API ───────────────────────────────────────────────────────────

def get_default_branch() -> str:
    data = fetch_json(f"{API_BASE}")
    if isinstance(data, dict):
        return data.get("default_branch", "main")
    return "main"


def get_all_lsl_paths(branch: str) -> list[tuple[str, str]]:
    """
    Returns list of (git_path, sha) for every LSL/txt file in the repo.
    Uses the recursive tree API — one request for the entire repo.
    Falls back to paginated iteration if the tree is truncated.
    """
    url  = f"{API_BASE}/git/trees/{branch}?recursive=1"
    data = fetch_json(url)

    if not isinstance(data, dict):
        return []

    entries = data.get("tree", [])
    if data.get("truncated"):
        print("  [warn] GitHub tree truncated — falling back to top-level walk", flush=True)
        entries = _walk_tree(branch)

    results = []
    for entry in entries:
        if entry.get("type") != "blob":
            continue
        path = entry.get("path", "")
        ext  = Path(path).suffix.lower()
        if ext in LSL_EXTS or ext == TXT_EXT:
            results.append((path, entry.get("sha", "")))

    return results


def _walk_tree(branch: str) -> list[dict]:
    """Fallback: walk top-level dirs one by one if recursive tree was truncated."""
    entries = []
    top = fetch_json(f"{API_BASE}/git/trees/{branch}")
    if not isinstance(top, dict):
        return entries
    for item in top.get("tree", []):
        if item.get("type") == "tree":
            sub = fetch_json(f"{API_BASE}/git/trees/{item['sha']}?recursive=1")
            if isinstance(sub, dict):
                for e in sub.get("tree", []):
                    e["path"] = item["path"] + "/" + e["path"]
                    entries.append(e)
        else:
            entries.append(item)
        time.sleep(0.2)
    return entries


# ── LSL keyword check (for .txt files) ───────────────────────────────────────

_LSL_KW = re.compile(
    r'\b(default\s*\{|state_entry\s*\(|llSay\s*\(|llOwnerSay\s*\(|'
    r'llSetText\s*\(|llListen\s*\(|integer\s+\w|string\s+\w|vector\s+\w)',
    re.DOTALL,
)


def _is_lsl(path: str, content: str) -> bool:
    ext = Path(path).suffix.lower()
    if ext in LSL_EXTS:
        return True
    if ext == TXT_EXT:
        return bool(_LSL_KW.search(content))
    return False


# ── Deduplication ─────────────────────────────────────────────────────────────

def _norm(name: str) -> str:
    n = name.lower()
    n = re.sub(r'[\s\-_]+', '', n)
    n = re.sub(r'\.(lsl|sl|lslp|lslm|txt)$', '', n)
    return n


def _md5(content: str) -> str:
    return hashlib.md5(
        re.sub(r'\s+', ' ', content).strip().encode("utf-8", errors="replace")
    ).hexdigest()


def _load_existing() -> tuple[set[str], set[str]]:
    names: set[str]  = set()
    hashes: set[str] = set()
    for p in OUT_DIR.glob("*.md"):
        names.add(_norm(p.stem))
        try:
            txt   = p.read_text(encoding="utf-8", errors="replace")
            parts = re.split(r'^---\s*$', txt, maxsplit=2, flags=re.MULTILINE)
            body  = parts[-1] if len(parts) >= 2 else txt
            hashes.add(_md5(body))
        except Exception:
            pass
    return names, hashes


# ── Description extractor ─────────────────────────────────────────────────────

def _extract_desc(content: str) -> str:
    bm = re.match(r'\s*/\*(.*?)\*/', content, re.DOTALL)
    if bm:
        lines = [l.strip().lstrip('*').strip() for l in bm.group(1).splitlines()]
        prose = ' '.join(l for l in lines if l and not l.startswith('@'))
        if len(prose) > 10:
            return prose[:300]
    acc = []
    for line in content.splitlines():
        s = line.strip()
        if s.startswith("//"):
            acc.append(s[2:].strip())
        elif s == "" and acc:
            break
        elif s and not s.startswith("//"):
            break
    if acc:
        prose = ' '.join(acc)
        if len(prose) > 10:
            return prose[:300]
    return ""


# ── File writer ───────────────────────────────────────────────────────────────

def _qs(s: str) -> str:
    return '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'


def _save(git_path: str, raw_url: str, web_url: str,
          content: str, existing_names: set, existing_hashes: set) -> bool:
    stem = Path(git_path).stem
    norm = _norm(stem)

    if not FORCE and norm in existing_names:
        return False

    h = _md5(content)
    if not FORCE and h in existing_hashes:
        return False

    safe = re.sub(r'[<>:"/\\|?*]', '_', stem)
    safe = re.sub(r'\s+', '_', safe.strip())[:100]
    path = OUT_DIR / f"{safe}.md"

    counter = 0
    while path.exists() and not FORCE:
        counter += 1
        path = OUT_DIR / f"{safe}_{counter}.md"

    desc = _extract_desc(content)
    front = (
        f'---\n'
        f'name: {_qs(safe)}\n'
        f'category: "examples"\n'
        f'type: "example"\n'
        f'language: "LSL"\n'
        f'description: {_qs(desc)}\n'
        f'source_url: {_qs(web_url)}\n'
        f'source_name: {_qs(SOURCE_NAME)}\n'
        f'first_fetched: {_qs(TODAY)}\n'
        f'last_updated: {_qs(TODAY)}\n'
        f'---\n\n'
        f'```lsl\n{content.rstrip()}\n```\n'
    )

    if not DRY_RUN:
        path.write_text(front, encoding="utf-8")

    existing_names.add(norm)
    existing_hashes.add(h)
    return True


# ── Manifest / changelog ──────────────────────────────────────────────────────

def _update_manifest(saved: int):
    manifest: dict = {}
    if MANIFEST.exists():
        try:
            manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        except Exception:
            pass
    manifest.setdefault("extra_library_sources", {})["outworldz-web"] = TODAY
    manifest["last_updated"] = TODAY
    if not DRY_RUN:
        MANIFEST.write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def _append_changelog(saved: int, skipped: int, errors: int):
    entry = (
        f"\n## {TODAY} — Outworldz fetch\n"
        f"- outworldz ({GH_OWNER}/{GH_REPO}): saved {saved}, skipped {skipped}, errors {errors}\n"
    )
    try:
        existing = CHANGELOG.read_text(encoding="utf-8") if CHANGELOG.exists() else ""
        if not DRY_RUN:
            CHANGELOG.write_text(existing + entry, encoding="utf-8")
    except Exception:
        pass


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    # ── Token-only operations ──────────────────────────────────────────────
    if CLEAR_TOKEN:
        _clear_token()
        sys.exit(0)

    if SAVE_TOKEN:
        token = _CLI_TOKEN or os.environ.get("GITHUB_TOKEN", "").strip()
        if not token:
            print(
                "ERROR: --save-token requires a token.\n"
                "  Supply it with --token=ghp_... or set GITHUB_TOKEN in your environment.",
                flush=True,
            )
            sys.exit(1)
        _save_token(token)
        print(f"Token saved to {_TOKEN_FILE}", flush=True)
        print("It will be used automatically on future runs.", flush=True)
        # Fall through to run normally with the token just saved.

    print(f"fetch-outworldz v0.3.0.0  [{TODAY}]", flush=True)
    print(f"Repo     : {GH_OWNER}/{GH_REPO}", flush=True)
    print(f"Output   : {OUT_DIR}", flush=True)

    if GH_TOKEN:
        source = (
            "CLI --token"     if _CLI_TOKEN else
            "GITHUB_TOKEN env" if os.environ.get("GITHUB_TOKEN") else
            f"{_TOKEN_FILE.name} (saved)"
        )
        masked = GH_TOKEN[:4] + "…" + GH_TOKEN[-4:] if len(GH_TOKEN) > 8 else "***"
        print(f"Auth     : {masked}  ({source})  — 5 000 req/hr", flush=True)
    else:
        print(
            "Auth     : none (60 req/hr — run with --token=ghp_... to authenticate)\n"
            "           Get a token at: https://github.com/settings/tokens\n"
            "           No scopes needed for public repos.  Save for reuse: --save-token",
            flush=True,
        )

    if FORCE:   print("Mode     : --force (ignoring duplicates)", flush=True)
    if DRY_RUN: print("Mode     : --dry-run (nothing written)", flush=True)
    if LIMIT:   print(f"Limit    : {LIMIT} files", flush=True)
    print(flush=True)

    existing_names, existing_hashes = _load_existing()
    print(f"Existing examples: {len(existing_names)} (dedup index loaded)\n", flush=True)

    # ── Step 1: discover all files via GitHub tree API ─────────────────────
    print("Step 1: resolving default branch …", flush=True)
    branch = get_default_branch()
    print(f"  branch: {branch}", flush=True)

    print(f"Step 2: fetching file tree from GitHub API …", flush=True)
    all_paths = get_all_lsl_paths(branch)
    print(f"  {len(all_paths)} candidate file(s) found\n", flush=True)

    if not all_paths:
        print("ERROR: No files found in GitHub tree. Check repo name or network.", flush=True)
        sys.exit(1)

    # ── Step 3: download and save ──────────────────────────────────────────
    print(f"Step 3: downloading and saving …\n", flush=True)

    saved = skipped = errors = 0

    for git_path, _sha in all_paths:
        if LIMIT and (saved + skipped) >= LIMIT:
            print(f"  Limit of {LIMIT} reached — stopping.", flush=True)
            break

        # Build URLs
        encoded   = urllib.parse.quote(git_path)
        raw_url   = f"{RAW_BASE}/{branch}/{encoded}"
        web_url   = f"{WEB_BASE}{encoded}"   # outworldz.com mirror URL for attribution

        # Quick name-based pre-check before downloading
        stem = Path(git_path).stem
        norm = _norm(stem)
        if not FORCE and norm in existing_names:
            skipped += 1
            continue

        time.sleep(RATE_DELAY)
        content = fetch_text(raw_url)
        if not content:
            errors += 1
            print(f"  ERROR: {git_path}", flush=True)
            continue

        if not _is_lsl(git_path, content):
            skipped += 1
            continue

        if _save(git_path, raw_url, web_url, content, existing_names, existing_hashes):
            saved += 1
            print(f"  saved : {git_path}", flush=True)
        else:
            skipped += 1

    # ── Summary ────────────────────────────────────────────────────────────
    print(f"\n{'='*50}", flush=True)
    print(f"Saved  : {saved}", flush=True)
    print(f"Skipped: {skipped}", flush=True)
    print(f"Errors : {errors}", flush=True)

    if saved > 0 and not DRY_RUN:
        _update_manifest(saved)
        _append_changelog(saved, skipped, errors)
        print("Manifest and changelog updated.", flush=True)


if __name__ == "__main__":
    main()
