#!/usr/bin/env python3
# Skill: scrape-lsl-library
# Version: 0.1.2.0
# Purpose: Fetch LSL Script Library pages from wiki.secondlife.com/wiki/Category:LSL_Library
#          and pages linked from the main LSL_Library index page (e.g. FURWARE_text)
# Usage: python3 skills/scrape-lsl-library.py [--limit N] [--name PageName] [--resume]
# Created: 2026-03-10
# Last modified: 2026-03-11

"""
Fetches all pages in Category:LSL_Library, extracts descriptions and code blocks,
and saves each as a .md file in ~/.lsl-cache/lsl-docs/examples/.

Page structure of individual library scripts:
  <h1 id="firstHeading">    — script title
  <div id="mw-content-text"> — description paragraphs + code blocks
"""

import io
import hashlib
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# ── Config ───────────────────────────────────────────────────────────────────

_env_base   = os.environ.get("LSL_CACHE_BASE", "").strip()
CACHE_ROOT  = Path(_env_base) if _env_base else Path(__file__).resolve().parents[1]
DOCS_DIR    = CACHE_ROOT / "lsl-docs"
OUT_DIR     = DOCS_DIR / "examples"
CHANGELOG   = DOCS_DIR / "CHANGELOG.md"
TODAY       = date.today().isoformat()
RATE_DELAY  = 0.5
BASE_URL    = "https://wiki.secondlife.com"
CAT_URL     = f"{BASE_URL}/wiki/Category:LSL_Library"
INDEX_URL   = f"{BASE_URL}/wiki/LSL_Library"  # curated index page (not a category)

LIMIT         = None
TARGET        = None
SKIP_EXISTING = False

for a in sys.argv[1:]:
    if a.startswith("--limit="):   LIMIT = int(a.split("=", 1)[1])
    elif a.startswith("--name="):  TARGET = a.split("=", 1)[1]
    elif a == "--resume":          SKIP_EXISTING = True


# ── HTML utilities ─────────────────────────────────────────────────────────────

def fetch(url: str) -> str:
    req = urllib.request.Request(
        url, headers={"User-Agent": "LSL-Cache-Bot/1.0 (local doc tool)"}
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.read().decode("utf-8", errors="replace")
    except Exception as e:
        print(f"  FETCH ERROR {url}: {e}")
        return ""


def unescape(text: str) -> str:
    text = text.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
    text = text.replace("&quot;", '"').replace("&#160;", " ").replace("&nbsp;", " ")
    text = text.replace("&mdash;", "—").replace("&ndash;", "–").replace("&bull;", "•")
    text = text.replace("&#124;", "|").replace("&#39;", "'")
    text = re.sub(r"&#(\d+);", lambda m: chr(int(m.group(1))), text)
    return text


def strip_tags(html: str) -> str:
    text = re.sub(r"<[^>]+>", "", html)
    return re.sub(r"\s+", " ", text).strip()


def strip_nav_chrome(html: str) -> str:
    """Remove wiki navigation templates, personal author boxes, and portal bars."""
    # Strip noprint / navigation tables
    html = re.sub(r'<table[^>]*class="[^"]*(?:noprint|navbox|toc)[^"]*"[^>]*>.*?</table>', '', html, flags=re.DOTALL)
    # Strip the LSL Portal navbar (a table containing "LSL Portal" or "LSL_Portal")
    html = re.sub(r'<table[^>]*>(?:(?!</table>).)*?LSL[_ ]Portal(?:(?!</table>).)*?</table>', '', html, flags=re.DOTALL)
    # Strip leading tables that appear before the first paragraph (nav boxes, author boxes)
    # Keep removing leading <table>...</table> blocks until we hit a <p> or heading
    while True:
        m = re.match(r'\s*(<table[^>]*>.*?</table>)\s*', html, re.DOTALL)
        if not m:
            break
        # Only strip if the table comes before any <p> content
        table_end = m.end()
        first_p = html.find('<p')
        if first_p == -1 or table_end <= first_p:
            html = html[table_end:]
        else:
            break
    # Strip <div> author/notice boxes before first paragraph
    html = re.sub(r'^(\s*<div[^>]*class="[^"]*(?:notice|messagebox|ambox|mbox)[^"]*"[^>]*>.*?</div>\s*)+', '', html, flags=re.DOTALL)
    return html


def html_to_markdown(html: str) -> str:
    """Convert content HTML to Markdown. Reuses same approach as scrape-wiki-pages."""

    html = strip_nav_chrome(html)

    # Code blocks
    def replace_code_block(m):
        inner = m.group(1)
        code = re.sub(r"<span[^>]*>|</span>", "", inner)
        code = re.sub(r"<[^>]+>", "", code)
        return f"\n\n```lsl\n{unescape(code).rstrip()}\n```\n\n"

    html = re.sub(
        r'<div[^>]*class="[^"]*mw-highlight[^"]*"[^>]*>\s*<pre[^>]*>(.*?)</pre>\s*</div>',
        replace_code_block, html, flags=re.DOTALL
    )
    html = re.sub(
        r"<pre[^>]*>(.*?)</pre>",
        lambda m: f"\n\n```lsl\n{unescape(re.sub(r'<[^>]+>','',m.group(1))).rstrip()}\n```\n\n",
        html, flags=re.DOTALL
    )
    html = re.sub(r"<code[^>]*>(.*?)</code>",
                  lambda m: f"`{strip_tags(m.group(1))}`", html, flags=re.DOTALL)

    # Headings
    for level in (4, 3, 2):
        tag = f"h{level}"
        html = re.sub(
            fr"<{tag}[^>]*>.*?class=\"mw-headline\"[^>]*>(.*?)</span>.*?</{tag}>",
            lambda m, lvl=level: f"\n\n{'#'*lvl} {strip_tags(m.group(1))}\n\n",
            html, flags=re.DOTALL
        )
        html = re.sub(
            fr"<{tag}[^>]*>(.*?)</{tag}>",
            lambda m, lvl=level: f"\n\n{'#'*lvl} {strip_tags(m.group(1))}\n\n",
            html, flags=re.DOTALL
        )

    # Lists
    LEAF_LIST = re.compile(
        r"<(ul|ol)[^>]*>((?:(?!<(?:ul|ol)\b).)*?)</(ul|ol)>", re.DOTALL
    )

    def convert_list(m):
        tag = m.group(1)
        items_html = m.group(2)
        bullet = "1. " if tag == "ol" else "- "
        items = re.findall(r"<li[^>]*>(.*?)</li>", items_html, re.DOTALL)
        lines = []
        for item in items:
            text = html_to_markdown(item).strip()
            text = re.sub(r"\n(- |[0-9]+\. )", r"\n  \1", text)
            lines.append(f"{bullet}{text}")
        return "\n" + "\n".join(lines) + "\n"

    for _ in range(6):
        new = LEAF_LIST.sub(convert_list, html)
        if new == html:
            break
        html = new

    # Inline formatting — no DOTALL; multi-line spans are stripped not converted
    def convert_bold(m):
        inner = m.group(1)
        text = strip_tags(inner)
        if "\n" in text or len(text) > 300:
            return text  # misused block-level bold — just strip the tags
        return f"**{text}**"

    def convert_italic(m):
        inner = m.group(1)
        text = strip_tags(inner)
        if "\n" in text or len(text) > 200:
            return text
        return f"*{text}*"

    html = re.sub(r"<(?:b|strong)[^>]*>(.*?)</(?:b|strong)>", convert_bold, html, flags=re.DOTALL)
    html = re.sub(r"<(?:i|em)[^>]*>(.*?)</(?:i|em)>", convert_italic, html, flags=re.DOTALL)

    # Links — internal wiki links become plain text; external keep URL
    html = re.sub(
        r'<a[^>]+href="(/wiki/[^"]+)"[^>]*>(.*?)</a>',
        lambda m: strip_tags(m.group(2)), html, flags=re.DOTALL
    )
    html = re.sub(
        r'<a[^>]+href="(https?://[^"]+)"[^>]*>(.*?)</a>',
        lambda m: f"[{strip_tags(m.group(2))}]({m.group(1)})", html, flags=re.DOTALL
    )

    # Paragraphs / br
    html = re.sub(r"<p[^>]*>", "\n\n", html)
    html = re.sub(r"</p>", "", html)
    html = re.sub(r"<br\s*/?>", "  \n", html)
    html = re.sub(r"<sup[^>]*>.*?</sup>", "", html, flags=re.DOTALL)
    html = re.sub(r"<[a-zA-Z/!][^>]*>", "", html)

    text = unescape(html)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"(?<!`)`{2}(?!`)", "", text)
    return text.strip()


# ── Category crawler ──────────────────────────────────────────────────────────

_SKIP_PREFIXES = ("Category:", "User:", "User_talk:", "Talk:", "Special:",
                  "Help:", "File:", "Template:", "Wikipedia:")

def _extract_page_links(html: str) -> list[tuple[str, str]]:
    """Extract (title, url) pairs from a mw-pages div, handling nested divs."""
    # Grab from id="mw-pages" to the next top-level section boundary
    m = re.search(r'id="mw-pages"(.*?)(?=\s*<(?:div|h2)\s+id="|<div\s+class="printfooter)', html, re.DOTALL)
    block = m.group(1) if m else html

    results = []
    for lm in re.finditer(r'<a\s+href="(/wiki/([^"#]+))"[^>]*>([^<]+)</a>', block):
        href, slug, title = lm.group(1), lm.group(2), lm.group(3)
        slug_decoded = urllib.parse.unquote(slug)
        if any(slug_decoded.startswith(p) for p in _SKIP_PREFIXES):
            continue
        results.append((unescape(title.strip()), BASE_URL + href))
    return results


def get_category_links() -> list[tuple[str, str]]:
    """Return (title, url) pairs from Category:LSL_Library and its subcategories."""
    seen_pages    = set()
    seen_cats     = set()
    queued_cats   = {CAT_URL}
    links         = []

    # Queue of category URLs to crawl (start with the main one)
    cat_queue = [CAT_URL]

    while cat_queue:
        cat_url = cat_queue.pop(0)
        if cat_url in seen_cats:
            continue
        seen_cats.add(cat_url)

        url = cat_url
        while url:
            html = fetch(url)
            if not html:
                break

            # Collect subcategory links and enqueue them
            subcat_m = re.search(r'id="mw-subcategories"(.*?)(?=id="mw-pages"|<div\s+class="printfooter)', html, re.DOTALL)
            if subcat_m:
                for sm in re.finditer(r'<a href="(/wiki/Category:[^"#]+)"', subcat_m.group(1)):
                    subcat_url = BASE_URL + sm.group(1)
                    if subcat_url not in seen_cats and subcat_url not in queued_cats:
                        cat_queue.append(subcat_url)
                        queued_cats.add(subcat_url)
                        print(f"    → subcategory queued: {sm.group(1)}")

            # Collect page links
            for title, full_url in _extract_page_links(html):
                if full_url not in seen_pages:
                    seen_pages.add(full_url)
                    links.append((title, full_url))

            # MediaWiki pagination — try several link-text variants used across
            # different wiki configurations: "(next 200)", "next page", "Next"
            next_m = re.search(
                r'<a href="([^"]*(?:pagefrom|from)[^"]*)"[^>]*>[^<]*(?:next|Next)[^<]*</a>',
                html
            )
            if next_m:
                next_href = unescape(next_m.group(1)).replace("&amp;", "&")
                next_url = next_href if next_href.startswith("http") else BASE_URL + next_href
                url = next_url if next_url != url else None
            else:
                url = None

            time.sleep(RATE_DELAY)

    return links


def get_index_page_links(already_seen: set) -> list[tuple[str, str]]:
    """
    Fetch the main LSL_Library index page and return (title, url) pairs for any
    internal wiki pages not already in already_seen.  These are pages that are
    curated in the index but not formally in Category:LSL_Library (e.g. FURWARE_text).
    """
    print(f"Crawling LSL_Library index page for uncategorised links…")
    html = fetch(INDEX_URL)
    if not html:
        print("  WARN: could not fetch LSL_Library index page")
        return []

    # Work inside the main article body only
    content_m = re.search(r'<div[^>]*class="[^"]*mw-parser-output[^"]*"[^>]*>(.*?)(?:<div[^>]*class="[^"]*printfooter|<div[^>]*id="catlinks")', html, re.DOTALL)
    content = content_m.group(1) if content_m else html

    # Skip links to categories, files, special pages, talk pages, and meta articles
    _SKIP_INDEX_PREFIXES = _SKIP_PREFIXES + (
        "Category:", "LSL_Portal", "LSL_Library",   # the index page itself
        "Second_Life_Wiki", "Wikipedia:", "SLurl",
    )
    _SKIP_EXACT = {
        "LSL_Library", "Category:LSL_Library", "LSL_Portal",
        "LSL_Style_Guide", "LSL_Tutorials", "LSL_Script_Limits",
    }

    links = []
    seen = set()
    for m in re.finditer(r'<a\s+href="(/wiki/([^"#]+))"[^>]*>([^<]*)</a>', content):
        href, slug, anchor_text = m.group(1), m.group(2), m.group(3).strip()
        slug_decoded = urllib.parse.unquote(slug)

        # Skip meta/navigation slugs
        if any(slug_decoded.startswith(p) for p in _SKIP_INDEX_PREFIXES):
            continue
        if slug_decoded in _SKIP_EXACT:
            continue
        # Skip subpages at discovery time — they are picked up when their parent is fetched
        if "/" in slug_decoded:
            continue

        full_url = BASE_URL + href
        if full_url in already_seen or full_url in seen:
            continue

        title = unescape(anchor_text) if anchor_text else slug_decoded.replace("_", " ")
        seen.add(full_url)
        links.append((title, full_url))
        print(f"    + index link: {slug_decoded}")

    print(f"  Found {len(links)} new page(s) from index not in category.\n")
    return links


# ── Page parser ───────────────────────────────────────────────────────────────

def parse_library_page(title: str, url: str, html: str) -> dict:
    """Extract description, author, tags and code from a library script page."""

    # Remove noise: hidden spans, edit links, TOC, categories
    html = re.sub(r'<span[^>]*display:\s*none[^>]*>.*?</span>', '', html, flags=re.DOTALL)
    html = re.sub(r'<div[^>]*id="toc"[^>]*>.*?</div>', '', html, flags=re.DOTALL)
    html = re.sub(r'<span class="mw-editsection"[^>]*>.*?</span>', '', html, flags=re.DOTALL)
    html = re.sub(r'<div[^>]*id="catlinks"[^>]*>.*?</div>', '', html, flags=re.DOTALL)
    html = re.sub(r'<div[^>]*class="[^"]*printfooter[^"]*"[^>]*>.*', '', html, flags=re.DOTALL)

    # Grab main content area (mw-parser-output is the article body)
    content_m = re.search(r'<div[^>]*class="[^"]*mw-parser-output[^"]*"[^>]*>(.*)', html, re.DOTALL)
    if not content_m:
        content_m = re.search(r'<div[^>]*id="mw-content-text"[^>]*>(.*)', html, re.DOTALL)
    content = content_m.group(1) if content_m else html

    # Strip the LSL Portal nav template and any leading tables/navboxes
    content = strip_nav_chrome(content)

    # Description: first non-empty <p> before any code block
    desc = ""
    code_start = content.find('<div class="mw-highlight')
    if code_start == -1:
        code_start = content.find("<pre")
    pre_code = content[:code_start] if code_start > 0 else content
    for pm in re.finditer(r"<p[^>]*>(.*?)</p>", pre_code, re.DOTALL):
        candidate = unescape(strip_tags(pm.group(1))).strip()
        if len(candidate) > 20:
            desc = candidate
            break

    # Author from categories or page text
    author = ""
    author_m = re.search(r'(?:Author|Created by|by)\s*:?\s*<a[^>]*>([^<]+)</a>', html, re.DOTALL | re.IGNORECASE)
    if author_m:
        author = strip_tags(author_m.group(1)).strip()

    # Detect subpages: links to /wiki/<PageSlug>/<SubpageName>
    page_slug = urllib.parse.unquote(url.split("/wiki/")[-1])
    subpage_urls = []
    subpage_pattern = re.compile(
        r'<a\s+href="(/wiki/' + re.escape(urllib.parse.quote(page_slug, safe="")) +
        r'/([^"#]+))"', re.IGNORECASE
    )
    # Also match decoded slug form
    subpage_pattern2 = re.compile(
        r'<a\s+href="(/wiki/' + re.escape(page_slug.replace(" ", "_")) +
        r'/([^"#]+))"', re.IGNORECASE
    )
    seen_sub = set()
    for pat in (subpage_pattern, subpage_pattern2):
        for sm in pat.finditer(html):
            sub_url = BASE_URL + sm.group(1)
            if sub_url not in seen_sub:
                seen_sub.add(sub_url)
                subpage_urls.append((sm.group(2), sub_url))

    # Convert main content to markdown
    body_md = html_to_markdown(content)

    # Count code blocks to infer complexity
    code_count = body_md.count("```lsl")

    return {
        "description": desc,
        "author": author,
        "body": body_md,
        "code_count": code_count,
        "subpages": subpage_urls,  # list of (subpage_name, url)
    }


# ── File writer ───────────────────────────────────────────────────────────────

def title_to_filename(title: str) -> str:
    """Convert a wiki page title to a safe filename."""
    safe = re.sub(r'[<>:"/\\|?*]', "", title)
    safe = re.sub(r'\s+', "_", safe.strip())
    return safe[:120] + ".md"


def save_example(title: str, url: str, data: dict) -> Path:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    filename = title_to_filename(title)
    path = OUT_DIR / filename

    front_matter = f"""---
name: {json_str(title)}
category: "examples"
type: "example"
language: "LSL"
description: {json_str(data['description'])}
wiki_url: {json_str(url)}
author: {json_str(data['author'])}
first_fetched: {json_str(TODAY)}
last_updated: {json_str(TODAY)}
---

"""
    content = front_matter + data["body"]

    if path.exists():
        chunk_hash = hashlib.sha1(content.encode("utf-8")).hexdigest()[:12]
        marker = f"<!-- cache-chunk:library:{chunk_hash} -->"
        existing = path.read_text(encoding="utf-8")
        if marker not in existing:
            with open(path, "a", encoding="utf-8") as fh:
                fh.write(
                    f"\n\n{marker}\n"
                    f"### Cache Delta — {TODAY} (library refresh)\n\n"
                    f"{content.rstrip()}\n"
                )
    else:
        path.write_text(content, encoding="utf-8")
    return path


def json_str(s: str) -> str:
    """Wrap a string in double quotes, escaping internal quotes."""
    return '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print(f"scrape-lsl-library v0.1.2.0 — {TODAY}")
    print(f"Output: {OUT_DIR}")
    print()

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    if TARGET:
        # Single-page mode: guess URL from name
        url = f"{BASE_URL}/wiki/{urllib.parse.quote(TARGET)}"
        targets = [(TARGET, url)]
    else:
        print("Crawling Category:LSL_Library for page list…")
        targets = get_category_links()
        print(f"  Found {len(targets)} script pages.\n")

        # Also collect pages linked from the curated index but not in the category
        cat_urls = {u for _, u in targets}
        index_extras = get_index_page_links(cat_urls)
        targets.extend(index_extras)

        print(f"  Total targets: {len(targets)} ({len(index_extras)} from index page).\n")
        if LIMIT:
            targets = targets[:LIMIT]

    total   = len(targets)
    written = skipped = failed = 0

    for i, (title, url) in enumerate(targets, 1):
        print(f"  [{i:>4}/{total}] {title:<50}", end=" ", flush=True)

        if SKIP_EXISTING:
            filename = title_to_filename(title)
            if (OUT_DIR / filename).exists():
                print("(exists, skip)")
                skipped += 1
                continue

        html = fetch(url)
        if not html:
            failed += 1
            time.sleep(RATE_DELAY)
            continue

        # Skip redirect pages (they have very little content)
        if '<div class="redirectMsg"' in html or "REDIRECT" in html[:500]:
            print("(redirect, skip)")
            skipped += 1
            time.sleep(RATE_DELAY)
            continue

        data = parse_library_page(title, url, html)

        # Fetch and append subpages
        if data["subpages"]:
            subpage_bodies = []
            for sub_name, sub_url in data["subpages"]:
                time.sleep(RATE_DELAY)
                sub_html = fetch(sub_url)
                if not sub_html:
                    continue
                sub_data = parse_library_page(f"{title}/{sub_name}", sub_url, sub_html)
                if sub_data["body"].strip():
                    sub_name_clean = unescape(urllib.parse.unquote(sub_name))
                    subpage_bodies.append(f"\n\n---\n\n## Subpage: {sub_name_clean}\n\n{sub_data['body']}")
                    data["code_count"] += sub_data["code_count"]
            if subpage_bodies:
                data["body"] += "".join(subpage_bodies)

        if not data["body"].strip() or "```lsl" not in data["body"]:
            print("(no code, skip)")
            skipped += 1
            time.sleep(RATE_DELAY)
            continue

        path = save_example(title, url, data)
        sub_note = f" +{len(data['subpages'])}sub" if data["subpages"] else ""
        print(f"OK ({data['code_count']} code block{'s' if data['code_count'] != 1 else ''}{sub_note})")
        written += 1
        time.sleep(RATE_DELAY)

    # Update CHANGELOG
    entry = f"\n## {TODAY} — LSL Library scrape (v0.1.2.0)\n"
    entry += f"- Fetched {total} pages (Category:LSL_Library + LSL_Library index links)\n"
    entry += f"- Saved: {written}, Skipped (no code/redirect/exists): {skipped}, Failed: {failed}\n"
    if CHANGELOG.exists():
        CHANGELOG.write_text(
            CHANGELOG.read_text(encoding="utf-8") + entry, encoding="utf-8"
        )

    print()
    print(f"Done.  Saved: {written}  Skipped: {skipped}  Failed: {failed}")
    print(f"Files in {OUT_DIR}")


if __name__ == "__main__":
    main()
