#!/usr/bin/env python3
# Skill: fetch-slua-docs
# Version: 0.1.0.1
# Purpose: Download Second Life SLua scripting documentation to the LSL cache
# Usage: python3 fetch-slua-docs.py [--force]
# Created: 2026-03-10
# Last modified: 2026-03-17

"""
Fetches SLua documentation from the SL wiki:
  - Dynamically discovers SLua pages via the MediaWiki API (category members,
    search, and seed crawl fallback)
  - Any linked SLua sub-pages and function pages found on discovered pages

Saves docs to ~/.lsl-cache/lsl-docs/slua/ and updates cache-manifest.json.

Note: The primary SLua API reference at create.secondlife.com/script/ is a
JavaScript SPA and cannot be scraped without a browser. The wiki pages are
the best available structured source via plain HTTP.
"""

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
DOCS_DIR      = CACHE_ROOT / "lsl-docs"
SLUA_DIR      = DOCS_DIR / "slua"
MANIFEST_PATH = CACHE_ROOT / "cache-manifest.json"
CHANGELOG     = DOCS_DIR / "CHANGELOG.md"
TODAY         = date.today().isoformat()
RATE_DELAY    = 0.5

FORCE = "--force" in sys.argv

SL_WIKI = "https://wiki.secondlife.com"

SLUA_DIR.mkdir(parents=True, exist_ok=True)

# ── SSL context ───────────────────────────────────────────────────────────────
# Use a no-verify context for all requests to handle certificate issues

_SSL_CTX = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
_SSL_CTX.check_hostname = False
_SSL_CTX.verify_mode = ssl.CERT_NONE


# ── HTTP helpers ──────────────────────────────────────────────────────────────

HEADERS = {
    "Accept":          "text/html,application/xhtml+xml",
    "Accept-Language": "en-US,en;q=0.9",
    "User-Agent":      "Mozilla/5.0 (Windows NT 10.0; Win64; x64) SLCode/1.0 LSL-cache-builder",
}


def fetch_url(url: str) -> str:
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=20, context=_SSL_CTX) as resp:
            raw = resp.read()
            enc = resp.headers.get_content_charset("utf-8")
            return raw.decode(enc, errors="replace")
    except Exception as e:
        print(f"  [fetch error] {url}: {e}", flush=True)
        return ""


# ── Dynamic page discovery ────────────────────────────────────────────────────

def _is_slua_relevant(title_or_url: str) -> bool:
    """Return True if the title or URL suggests SLua/Luau content."""
    lower = title_or_url.lower()
    return "slua" in lower or "luau" in lower


def _api_category_members(category: str) -> list:
    """Query MediaWiki API for category members. Returns list of (title, wiki_url)."""
    for api_url in (f"{SL_WIKI}/w/api.php", f"{SL_WIKI}/api.php"):
        results = []
        cmcontinue = None
        if not fetch_url(f"{api_url}?action=query&meta=siteinfo&format=json"):
            continue  # this path doesn't exist
        break
    else:
        return []
    while True:
        params = {
            "action": "query",
            "list": "categorymembers",
            "cmtitle": f"Category:{category}",
            "cmlimit": "500",
            "format": "json",
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
                encoded = urllib.parse.quote(title.replace(" ", "_"))
                wiki_url = f"{SL_WIKI}/wiki/{encoded}"
                results.append((title, wiki_url))
        cont = data.get("continue", {})
        cmcontinue = cont.get("cmcontinue")
        if not cmcontinue:
            break
    return results


def _api_search(query: str) -> list:
    """Query MediaWiki search API. Returns list of (title, wiki_url)."""
    results = []
    api_url = next(
        (u for u in (f"{SL_WIKI}/w/api.php", f"{SL_WIKI}/api.php")
         if fetch_url(f"{u}?action=query&meta=siteinfo&format=json")),
        f"{SL_WIKI}/w/api.php"
    )
    params = {
        "action": "query",
        "list": "search",
        "srsearch": query,
        "srlimit": "100",
        "format": "json",
        "srnamespace": "0",
    }
    query_str = urllib.parse.urlencode(params)
    url = f"{api_url}?{query_str}"
    time.sleep(RATE_DELAY)
    raw = fetch_url(url)
    if not raw:
        return results
    try:
        data = json.loads(raw)
    except Exception:
        return results
    for item in data.get("query", {}).get("search", []):
        title = item.get("title", "")
        if title:
            encoded = urllib.parse.quote(title.replace(" ", "_"))
            wiki_url = f"{SL_WIKI}/wiki/{encoded}"
            results.append((title, wiki_url))
    return results


def _seed_crawl() -> list:
    """Crawl seed pages and follow SLua/Luau links. Returns list of (title, wiki_url)."""
    seeds = [
        f"{SL_WIKI}/wiki/SLua",
        f"{SL_WIKI}/wiki/Category:SLua",
    ]
    results = []
    seen_urls = set()
    for seed_url in seeds:
        time.sleep(RATE_DELAY)
        html = fetch_url(seed_url)
        if not html:
            continue
        for m in re.finditer(r'<a[^>]*href="(/wiki/[^"#]*)"[^>]*>([^<]*)</a>', html):
            path  = m.group(1)
            title = m.group(2).strip()
            wiki_url = SL_WIKI + path
            if wiki_url in seen_urls:
                continue
            if _is_slua_relevant(path) or _is_slua_relevant(title):
                seen_urls.add(wiki_url)
                results.append((title or path.split("/")[-1], wiki_url))
    return results


def discover_pages() -> list:
    """
    Build the list of SLua pages to fetch using dynamic discovery:
      1. MediaWiki API — category members (primary)
      2. MediaWiki API — search (secondary)
      3. Seed crawl (fallback)
    Returns deduplicated list of (title, wiki_url).
    """
    SLUA_CATEGORIES = ["SLua", "SLua_Functions", "SLua_Scripting", "Luau"]

    print("Discovering SLua pages via MediaWiki API (category members)...", flush=True)
    found = []
    for cat in SLUA_CATEGORIES:
        members = _api_category_members(cat)
        if members:
            print(f"  Category:{cat} → {len(members)} page(s)", flush=True)
        found.extend(members)

    if not found:
        print("  No category members found. Trying API search...", flush=True)
        found = _api_search("SLua")
        print(f"  Search returned {len(found)} result(s)", flush=True)

    if not found:
        print("  API search returned nothing. Falling back to seed crawl...", flush=True)
        found = _seed_crawl()
        print(f"  Seed crawl found {len(found)} link(s)", flush=True)

    # Deduplicate by URL, preserving order
    seen  = set()
    dedup = []
    for title, url in found:
        if url not in seen:
            seen.add(url)
            dedup.append((title, url))

    print(f"Total unique SLua pages discovered: {len(dedup)}", flush=True)
    return dedup


# ── HTML → Markdown ───────────────────────────────────────────────────────────

def strip_tags(html: str) -> str:
    text = re.sub(r"<[^>]+>", "", html)
    return re.sub(r"\s+", " ", text).strip()


def unescape(text: str) -> str:
    text = text.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
    text = text.replace("&quot;", '"').replace("&#160;", " ").replace("&nbsp;", " ")
    text = text.replace("&mdash;", "—").replace("&ndash;", "–")
    text = re.sub(r"&#(\d+);", lambda m: chr(int(m.group(1))), text)
    return text


def html_to_markdown(html: str) -> str:
    # Code blocks
    html = re.sub(
        r'<div[^>]*class="[^"]*mw-highlight[^"]*"[^>]*>\s*<pre[^>]*>(.*?)</pre>\s*</div>',
        lambda m: f"\n\n```lua\n{unescape(re.sub(r'<[^>]+>','',m.group(1))).rstrip()}\n```\n\n",
        html, flags=re.DOTALL
    )
    html = re.sub(
        r"<pre[^>]*>(.*?)</pre>",
        lambda m: f"\n\n```lua\n{unescape(re.sub(r'<[^>]+>','',m.group(1))).rstrip()}\n```\n\n",
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
    html = re.sub(
        r'<a[^>]*href="(/wiki/[^"#]*)"[^>]*>(.*?)</a>',
        lambda m: f"[{strip_tags(m.group(2))}]({SL_WIKI}{unescape(m.group(1))})",
        html, flags=re.DOTALL
    )
    html = re.sub(r'<a[^>]*href="(https?://[^"]*)"[^>]*>(.*?)</a>',
                  lambda m: f"[{strip_tags(m.group(2))}]({m.group(1)})", html, flags=re.DOTALL)

    # Bold / italic
    html = re.sub(r"<b[^>]*>(.*?)</b>",
                  lambda m: f"**{strip_tags(m.group(1))}**", html, flags=re.DOTALL)
    html = re.sub(r"<i[^>]*>(.*?)</i>",
                  lambda m: f"*{strip_tags(m.group(1))}*", html, flags=re.DOTALL)

    # Paragraphs
    html = re.sub(r"<br\s*/?>", "\n", html)
    html = re.sub(r"<p[^>]*>(.*?)</p>",
                  lambda m: f"\n\n{strip_tags(m.group(1))}\n\n", html, flags=re.DOTALL)

    html = re.sub(r"<[^>]+>", "", html)
    html = unescape(html)
    html = re.sub(r"\n{3,}", "\n\n", html)
    return html.strip()


# ── Page processing ───────────────────────────────────────────────────────────

def extract_content(html: str) -> str:
    """Extract the main content area from a wiki page."""
    cm = re.search(
        r'<div[^>]*id="mw-content-text"[^>]*>(.*?)<div[^>]*class="[^"]*printfooter',
        html, re.DOTALL
    )
    return cm.group(1) if cm else html


def extract_title(html: str) -> str:
    """Extract page title."""
    m = re.search(r'<h1[^>]*id="firstHeading"[^>]*>(.*?)</h1>', html, re.DOTALL)
    return strip_tags(m.group(1)).strip() if m else ""


def extract_description(content_html: str) -> str:
    """Extract first prose paragraph."""
    for pm in re.finditer(r'<p[^>]*>(.*?)</p>', content_html, re.DOTALL):
        text = unescape(strip_tags(pm.group(1))).strip()
        if len(text) > 20 and not text.startswith('{') and not text.startswith('|'):
            return text[:300]
    return ""


def get_slua_links(content_html: str) -> list:
    """Find internal wiki links to SLua-related pages."""
    links = []
    for m in re.finditer(r'<a[^>]*href="(/wiki/[^"#]*)"[^>]*>([^<]+)</a>',
                         content_html, re.DOTALL):
        path  = m.group(1)
        title = m.group(2).strip()
        url   = SL_WIKI + path
        if url not in [u for _, u in links]:
            # Broaden filter: accept any link where path OR title contains slua/luau
            if _is_slua_relevant(path) or _is_slua_relevant(title):
                links.append((title, url))
    return links


def save_page(title: str, wiki_url: str, content_html: str, is_function: bool = False):
    """Save a SLua wiki page as a markdown doc."""
    safe_name = re.sub(r'[^\w\-.]', '_', title.replace('/', '-').replace(' ', '_'))
    out_path  = SLUA_DIR / f"{safe_name}.md"

    if out_path.exists() and not FORCE:
        return False

    desc   = extract_description(content_html)
    body   = html_to_markdown(content_html)
    category = "function" if is_function else "reference"
    lang     = "SLua"

    desc_safe = desc.replace('"', '\\"')
    sig_m     = re.search(r'<(?:code|pre)[^>]*>(.*?)</(?:code|pre)>', content_html, re.DOTALL)
    signature = strip_tags(sig_m.group(1)).strip() if sig_m and title in strip_tags(sig_m.group(1)) else ""

    front = f"""---
name: "{title}"
category: "{category}"
type: "{category}"
language: "{lang}"
description: "{desc_safe}"
signature: "{signature.replace('"', '\\"')}"
wiki_url: "{wiki_url}"
first_fetched: "{TODAY}"
last_updated: "{TODAY}"
---
"""
    out_path.write_text(front + "\n" + body, encoding="utf-8")
    return True


# ── Main ──────────────────────────────────────────────────────────────────────

fetched  = 0
skipped  = 0
errors   = 0
visited  = set()

# Build page list dynamically
to_fetch = [(title, url) for title, url in discover_pages()]

print(f"\nFetching {len(to_fetch)} SLua page(s) from SL wiki...", flush=True)

while to_fetch:
    title, url = to_fetch.pop(0)
    if url in visited:
        continue
    visited.add(url)

    print(f"  Fetching: {url}", end="", flush=True)
    time.sleep(RATE_DELAY)

    html = fetch_url(url)
    if not html:
        errors += 1
        print(" — error", flush=True)
        continue

    # Use pre-discovered title; fall back to extracting from page HTML
    page_title = title if title else extract_title(html)
    content    = extract_content(html)

    if not page_title:
        print(" — no title, skipping", flush=True)
        continue

    # Determine if this is a function page (title contains () or is under SLua/)
    is_func = bool(re.search(r'\(.*\)', page_title)) or "/SLua/" in url

    saved = save_page(page_title, url, content, is_function=is_func)
    if saved:
        fetched += 1
        print(f" — saved: {page_title}", flush=True)
    else:
        skipped += 1
        print(f" — skipped (exists): {page_title}", flush=True)

    # Find and queue additional linked SLua pages from this page
    # Filter: only add links where title or URL contains slua/luau (case-insensitive)
    for link_name, link_url in get_slua_links(content):
        if link_url not in visited and (link_name, link_url) not in to_fetch:
            to_fetch.append((link_name, link_url))

print(f"\nDone: {fetched} pages saved, {skipped} skipped, {errors} errors", flush=True)
if fetched == 0 and errors > 0 and len(visited) == errors:
    print()
    print("NOTE: All SLua wiki URLs returned errors (likely 403/404).")
    print("SLua documentation may not yet be published on wiki.secondlife.com.")
    print("The primary SLua reference is at https://create.secondlife.com/script/")
    print("(a JavaScript SPA that requires a browser to render).")
    print("Re-run this tool later as the wiki pages become available.")

# Update manifest
if fetched > 0:
    manifest = {}
    if MANIFEST_PATH.exists():
        try:
            manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        except Exception:
            pass
    manifest.setdefault("sections", {})["slua"] = True
    manifest["last_updated"] = TODAY
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    try:
        with open(CHANGELOG, "a", encoding="utf-8") as f:
            f.write(f"\n## {TODAY} — SLua docs fetch\n"
                    f"- Fetched {fetched} SLua pages, skipped {skipped} existing\n"
                    f"- Saved to lsl-docs/slua/\n")
    except Exception:
        pass

    print(f"Cache manifest updated — sections.slua = true", flush=True)
