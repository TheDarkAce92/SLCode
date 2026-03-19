#!/usr/bin/env python3
# Skill: fetch-ossl-docs
# Version: 0.1.0.2
# Purpose: Download OpenSimulator OSSL function documentation to the LSL cache
# Usage: python3 fetch-ossl-docs.py [--limit N] [--force]
# Created: 2026-03-10
# Last modified: 2026-03-19
# DEPRECATED: opensimulator.org/wiki is unreliable (frequent 404s).
#             Use fetch-ossl-from-github.py instead — it sources directly from
#             the opensim/opensim GitHub repo and does not contact opensimulator.org.

"""
Fetches the OSSL function list from opensimulator.org/wiki/Category:OSSL_Functions,
then fetches each individual function page and saves it as a .md file with full
YAML front matter to ~/.lsl-cache/lsl-docs/ossl/.

Discovery uses the MediaWiki API as the primary method, with paginated HTML
scraping as a fallback.

Updates cache-manifest.json on completion.
"""

import io
import json
import os
import re
import ssl
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# ── Config ────────────────────────────────────────────────────────────────────

_env_base = os.environ.get("LSL_CACHE_BASE", "").strip()
CACHE_ROOT = Path(_env_base) if _env_base else Path(__file__).resolve().parents[1]
DOCS_DIR      = CACHE_ROOT / "lsl-docs"
OSSL_DIR      = DOCS_DIR / "ossl"
MANIFEST_PATH = CACHE_ROOT / "cache-manifest.json"
CHANGELOG     = DOCS_DIR / "CHANGELOG.md"
TODAY         = date.today().isoformat()
RATE_DELAY    = 0.8   # seconds between requests — be polite to opensimulator.org

OSIM_BASE     = "http://opensimulator.org"
BASE_URL      = f"{OSIM_BASE}/wiki/"
# All category/index pages that contain OSSL function links
SEED_URLS     = [
    f"{OSIM_BASE}/wiki/Category:OSSL",
    f"{OSIM_BASE}/wiki/Category:Scripting",
    f"{OSIM_BASE}/wiki/OSSL_Script_Library",
]
CATEGORY_URL  = SEED_URLS[0]   # kept for legacy fallback reference

FORCE = "--force" in sys.argv
LIMIT = None
for a in sys.argv[1:]:
    if a.startswith("--limit="):
        LIMIT = int(a.split("=", 1)[1])

OSSL_DIR.mkdir(parents=True, exist_ok=True)


# ── HTTP helpers ──────────────────────────────────────────────────────────────

HEADERS = {
    "Accept":          "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "User-Agent":      "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

# opensimulator.org uses older TLS configuration — use a permissive context
_SSL_CTX = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
_SSL_CTX.check_hostname = False
_SSL_CTX.verify_mode    = ssl.CERT_NONE


def fetch_url(url: str) -> str:
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=25, context=_SSL_CTX) as resp:
            raw = resp.read()
            enc = resp.headers.get_content_charset("utf-8")
            return raw.decode(enc, errors="replace")
    except Exception as e:
        print(f"  [fetch error] {url}: {e}", flush=True)
        return ""


# ── HTML → Markdown (MediaWiki) ───────────────────────────────────────────────

def strip_tags(html: str) -> str:
    text = re.sub(r"<[^>]+>", "", html)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def unescape(text: str) -> str:
    text = text.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
    text = text.replace("&quot;", '"').replace("&#160;", " ").replace("&nbsp;", " ")
    text = text.replace("&mdash;", "—").replace("&ndash;", "–").replace("&bull;", "•")
    text = re.sub(r"&#(\d+);", lambda m: chr(int(m.group(1))), text)
    return text


def html_to_markdown(html: str) -> str:
    # Code blocks
    html = re.sub(
        r'<div[^>]*class="[^"]*mw-highlight[^"]*"[^>]*>\s*<pre[^>]*>(.*?)</pre>\s*</div>',
        lambda m: f"\n\n```lsl\n{unescape(re.sub(r'<[^>]+>','',m.group(1))).rstrip()}\n```\n\n",
        html, flags=re.DOTALL
    )
    html = re.sub(
        r"<pre[^>]*>(.*?)</pre>",
        lambda m: f"\n\n```lsl\n{unescape(re.sub(r'<[^>]+>','',m.group(1))).rstrip()}\n```\n\n",
        html, flags=re.DOTALL
    )
    html = re.sub(r"<code[^>]*>(.*?)</code>",
                  lambda m: f"`{strip_tags(m.group(1))}`", html, flags=re.DOTALL)

    # Headings
    for lvl in (4, 3, 2):
        html = re.sub(
            fr"<h{lvl}[^>]*>.*?class=\"mw-headline\"[^>]*>(.*?)</span>.*?</h{lvl}>",
            lambda m, l=lvl: f"\n\n{'#'*l} {strip_tags(m.group(1))}\n\n",
            html, flags=re.DOTALL
        )
        html = re.sub(
            fr"<h{lvl}[^>]*>(.*?)</h{lvl}>",
            lambda m, l=lvl: f"\n\n{'#'*l} {strip_tags(m.group(1))}\n\n",
            html, flags=re.DOTALL
        )

    # Lists
    LEAF = re.compile(r"<(ul|ol)[^>]*>((?:(?!<(?:ul|ol)\b).)*?)</(ul|ol)>", re.DOTALL)
    def conv_list(m):
        tag   = m.group(1)
        inner = m.group(2)
        bullet = "1. " if tag == "ol" else "- "
        items = re.findall(r"<li[^>]*>(.*?)</li>", inner, re.DOTALL)
        lines = []
        for item in items:
            t = html_to_markdown(item).strip()
            t = re.sub(r"\n(- |[0-9]+\. )", r"\n  \1", t)
            lines.append(f"{bullet}{t}")
        return "\n" + "\n".join(lines) + "\n"
    for _ in range(6):
        new = LEAF.sub(conv_list, html)
        if new == html:
            break
        html = new

    # Links
    html = re.sub(r'<a[^>]*href="([^"]*)"[^>]*>(.*?)</a>',
                  lambda m: f"[{strip_tags(m.group(2))}]({unescape(m.group(1))})",
                  html, flags=re.DOTALL)

    # Bold / italic
    html = re.sub(r"<b[^>]*>(.*?)</b>", lambda m: f"**{strip_tags(m.group(1))}**",
                  html, flags=re.DOTALL)
    html = re.sub(r"<i[^>]*>(.*?)</i>", lambda m: f"*{strip_tags(m.group(1))}*",
                  html, flags=re.DOTALL)

    # Paragraphs / breaks
    html = re.sub(r"<br\s*/?>", "\n", html)
    html = re.sub(r"<p[^>]*>(.*?)</p>", lambda m: f"\n\n{strip_tags(m.group(1))}\n\n",
                  html, flags=re.DOTALL)

    # Strip remaining tags
    html = re.sub(r"<[^>]+>", "", html)
    html = unescape(html)

    # Normalise whitespace
    html = re.sub(r"\n{3,}", "\n\n", html)
    return html.strip()


# ── Page parsers ──────────────────────────────────────────────────────────────

def discover_via_api() -> list:
    """
    Use the MediaWiki API to get all members of Category:OSSL_Functions.
    Tries /api.php and /w/api.php path variants.
    Returns list of (name, wiki_url) tuples.
    """
    api_paths = [
        f"{OSIM_BASE}/w/api.php",
        f"{OSIM_BASE}/api.php",
        f"{OSIM_BASE}/mediawiki/api.php",
    ]
    results = []
    OSSL_CATEGORIES = ["OSSL", "Scripting", "OSSL_Functions"]
    for api_url in api_paths:
        batch = []
        for cat in OSSL_CATEGORIES:
            cmcontinue = None
            while True:
                params = {
                    "action":      "query",
                    "list":        "categorymembers",
                    "cmtitle":     f"Category:{cat}",
                    "cmlimit":     "500",
                    "format":      "json",
                    "cmnamespace": "0",
                }
                if cmcontinue:
                    params["cmcontinue"] = cmcontinue
                query_str = urllib.parse.urlencode(params)
                url = f"{api_url}?{query_str}"
                time.sleep(RATE_DELAY)
                raw = fetch_url(url)
                if not raw:
                    break
                try:
                    data = json.loads(raw)
                except Exception:
                    break
                members = data.get("query", {}).get("categorymembers", [])
                for m in members:
                    title = m.get("title", "")
                    if title:
                        encoded  = urllib.parse.quote(title.replace(" ", "_"))
                        wiki_url = f"{OSIM_BASE}/wiki/{encoded}"
                        name     = title.split(":")[-1] if ":" in title else title
                        batch.append((name, wiki_url))
                cont = data.get("continue", {})
                cmcontinue = cont.get("cmcontinue")
                if not cmcontinue:
                    break
        if batch:
            results = batch
            print(f"  API ({api_url}): found {len(results)} entries across categories", flush=True)
            break
        else:
            print(f"  API ({api_url}): no results", flush=True)

    return results


def get_function_list() -> list:
    """
    Build the list of OSSL functions to fetch.
    Primary: MediaWiki API.
    Fallback: paginated HTML scraping of the category page.
    Returns list of (name, wiki_url) tuples.
    """
    print(f"Fetching OSSL function list...", flush=True)

    # Primary: MediaWiki API
    api_results = discover_via_api()
    if api_results:
        # Deduplicate by name
        seen  = set()
        dedup = []
        for item in api_results:
            if item[0] not in seen:
                seen.add(item[0])
                dedup.append(item)
        print(f"  Found {len(dedup)} OSSL functions (via API)", flush=True)
        return dedup

    # Fallback: paginated HTML scraping of all seed URLs
    print(f"  API returned nothing — falling back to HTML scrape", flush=True)
    funcs     = []
    seen_urls = set()

    visited_pages = set()

    def _scrape_page_for_ossl_links(start_url: str):
        next_url = start_url
        while next_url:
            if next_url in visited_pages:
                break
            visited_pages.add(next_url)
            time.sleep(RATE_DELAY)
            html = fetch_url(next_url)
            if not html:
                break
            # Collect any internal wiki links — filter by name below
            for m in re.finditer(r'<a[^>]*href="(/wiki/[^"#]+)"[^>]*>([^<]+)</a>', html):
                path, name = m.group(1), m.group(2).strip()
                full_url = OSIM_BASE + path
                if full_url in seen_urls:
                    continue
                # Accept os* functions, OSSL_ prefixed, and "Script_Library" style pages
                if (name.startswith("os") or name.startswith("OSSL")
                        or "Script" in name or "script" in name):
                    seen_urls.add(full_url)
                    funcs.append((name, full_url))
            # Pagination
            next_m = re.search(
                r'<a href="([^"]*(?:pagefrom|from)[^"]*)"[^>]*>[^<]*next[^<]*</a>',
                html, re.IGNORECASE
            )
            if next_m:
                next_path = unescape(next_m.group(1))
                next_url = (next_path if next_path.startswith("http")
                            else OSIM_BASE + ("" if next_path.startswith("/") else "/") + next_path)
                print(f"  Following next page: {next_url}", flush=True)
            else:
                next_url = None

    for seed in SEED_URLS:
        print(f"  Scraping: {seed}", flush=True)
        _scrape_page_for_ossl_links(seed)

    # Deduplicate preserving order
    seen  = set()
    dedup = []
    for item in funcs:
        if item[0] not in seen:
            seen.add(item[0])
            dedup.append(item)

    print(f"  Found {len(dedup)} OSSL functions (via HTML scrape)", flush=True)
    return dedup


def parse_function_page(html: str, name: str, wiki_url: str) -> dict:
    """Extract structured data from an OSSL function wiki page."""
    # Content area
    cm = re.search(r'<div[^>]*id="mw-content-text"[^>]*>(.*?)<div[^>]*class="[^"]*printfooter',
                   html, re.DOTALL)
    content = cm.group(1) if cm else html

    # Description — first <p> in content
    desc = ""
    for pm in re.finditer(r'<p[^>]*>(.*?)</p>', content, re.DOTALL):
        text = strip_tags(pm.group(1)).strip()
        text = unescape(text)
        if len(text) > 20 and not text.startswith('{'):
            desc = text[:300]
            break

    # Signature — look for <code> or <pre> near "Syntax" heading
    signature = ""
    syn_m = re.search(r'(?:Syntax|Signature).*?<(?:code|pre)[^>]*>(.*?)</(?:code|pre)>',
                      content, re.DOTALL | re.IGNORECASE)
    if syn_m:
        signature = strip_tags(syn_m.group(1)).strip()
    if not signature:
        # Try pattern: common OSSL signature in first code block
        code_m = re.search(r'<(?:code|pre)[^>]*>(.*?)</(?:code|pre)>', content, re.DOTALL)
        if code_m:
            candidate = strip_tags(code_m.group(1)).strip()
            if name in candidate:
                signature = candidate

    # Delay / threat level (OpenSim specific)
    threat_level = ""
    tl_m = re.search(r'(?:Threat Level|ThreatLevel)[^:]*:\s*([A-Za-z]+)', content, re.IGNORECASE)
    if tl_m:
        threat_level = tl_m.group(1).strip()

    # Body markdown
    body_md = html_to_markdown(content)

    return {
        "description":  desc,
        "signature":    signature,
        "threat_level": threat_level,
        "body":         body_md,
    }


def save_doc(name: str, wiki_url: str, data: dict) -> bool:
    """Save a function doc to ossl/. Returns True if written, False if skipped."""
    out_path = OSSL_DIR / f"{name}.md"

    if out_path.exists() and not FORCE:
        return False  # skip existing

    desc = data["description"].replace('"', '\\"')
    sig  = data["signature"].replace('"', '\\"')

    front_matter = f"""---
name: "{name}"
category: "function"
type: "function"
language: "OSSL"
description: "{desc}"
signature: "{sig}"
wiki_url: "{wiki_url}"
threat_level: "{data['threat_level']}"
first_fetched: "{TODAY}"
last_updated: "{TODAY}"
---
"""
    content = front_matter + "\n" + data["body"]
    out_path.write_text(content, encoding="utf-8")
    return True


def append_changelog(count: int, skipped: int):
    entry = (f"\n## {TODAY} — OSSL docs fetch\n"
             f"- Fetched {count} OSSL function docs, skipped {skipped} existing\n"
             f"- Saved to lsl-docs/ossl/\n")
    try:
        with open(CHANGELOG, "a", encoding="utf-8") as f:
            f.write(entry)
    except Exception:
        pass


def update_manifest():
    manifest = {}
    if MANIFEST_PATH.exists():
        try:
            manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        except Exception:
            pass
    manifest.setdefault("sections", {})["ossl"] = True
    manifest["last_updated"] = TODAY
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2), encoding="utf-8")


# ── Fallback: kwdb-based local generation ─────────────────────────────────────

GITHUB_SKILL = Path(__file__).parent / "fetch-ossl-from-github.py"
KWDB_SKILL   = Path(__file__).parent / "generate-ossl-from-kwdb.py"

def _run_fallback(reason: str) -> None:
    """Try GitHub source first, then kwdb, when the wiki is unreachable."""
    print(f"\n[fetch-ossl] {reason}", flush=True)

    if GITHUB_SKILL.exists():
        print("[fetch-ossl] Falling back to GitHub source (IOSSL_Api.cs)...\n", flush=True)
        cmd = [sys.executable, str(GITHUB_SKILL)]
        if FORCE:
            cmd.append("--force")
        result = subprocess.run(cmd)
        sys.exit(result.returncode)

    if KWDB_SKILL.exists():
        print("[fetch-ossl] GitHub skill not found — falling back to local kwdb...\n", flush=True)
        cmd = [sys.executable, str(KWDB_SKILL)]
        if FORCE:
            cmd.append("--force")
        result = subprocess.run(cmd)
        sys.exit(result.returncode)

    print("ERROR: No fallback skill found.", flush=True)
    sys.exit(1)


# ── Main ──────────────────────────────────────────────────────────────────────

funcs = get_function_list()
if not funcs:
    _run_fallback("opensimulator.org returned no functions (wiki unreachable or empty).")

if LIMIT:
    funcs = funcs[:LIMIT]
    print(f"Limiting to {LIMIT} functions.", flush=True)

fetched = 0
skipped = 0
errors  = 0

for i, (name, wiki_url) in enumerate(funcs, 1):
    out_path = OSSL_DIR / f"{name}.md"
    if out_path.exists() and not FORCE:
        skipped += 1
        continue

    print(f"  [{i}/{len(funcs)}] {name}", end="", flush=True)
    time.sleep(RATE_DELAY)

    html = fetch_url(wiki_url)
    if not html:
        print(" — fetch error", flush=True)
        errors += 1
        continue

    data = parse_function_page(html, name, wiki_url)
    saved = save_doc(name, wiki_url, data)

    if saved:
        fetched += 1
        print(f" — OK", flush=True)
    else:
        skipped += 1
        print(f" — skipped (exists)", flush=True)

print(f"\nDone: {fetched} fetched, {skipped} skipped, {errors} errors", flush=True)

# If the wiki was reachable but almost everything failed, fall back to kwdb.
# Threshold: >80% errors with fewer than 5 successes means the wiki is broken.
if errors > 0 and fetched < 5 and errors / max(fetched + errors, 1) > 0.8:
    _run_fallback(
        f"Wiki fetch produced {fetched} successes and {errors} errors — "
        "wiki appears unreliable."
    )

if fetched > 0:
    append_changelog(fetched, skipped)
    update_manifest()
    print(f"Cache manifest updated — sections.ossl = true", flush=True)
