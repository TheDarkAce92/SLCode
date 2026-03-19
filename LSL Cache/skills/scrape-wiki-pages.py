#!/usr/bin/env python3
# Skill: scrape-wiki-pages
# Version: 0.1.3.1
# Purpose: Scrape SL wiki HTML pages and merge official content into cache docs
# Usage: python3 skills/scrape-wiki-pages.py [--type functions|events|all] [--limit N] [--name FUNCNAME] [--discover]
# Created: 2026-03-10
# Last modified: 2026-03-17

"""
Fetches SL wiki HTML for LSL functions and events, extracts meaningful
sections (Caveats, Examples, Notes, See Also) using targeted HTML parsing,
converts them to clean Markdown, and merges into existing cache docs.

SL wiki LSL pages have a consistent template structure:
  span#Summary (display:block) — official function signature
  collapsible table            — Forced Delay, Energy
  p                            — main description
  div#box > h2#Caveats         — bugs, rate limits, edge cases
  div#box > h2#Examples        — working LSL code examples
  div#box > h2#Notes           — undocumented behaviour, tips
  div#box > h2#See_Also        — related functions/events/constants

With --discover: fetches LSL wiki categories to find pages not yet in cache,
then downloads them as new docs.
"""

import io
import os
import re
import hashlib
import sys
import time
import traceback
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# ── Config ───────────────────────────────────────────────────────────────────

_env_base  = os.environ.get("LSL_CACHE_BASE", "").strip()
CACHE_ROOT = Path(_env_base) if _env_base else Path(__file__).resolve().parents[1]
DOCS_DIR   = CACHE_ROOT / "lsl-docs"
FN_DIR     = DOCS_DIR / "functions"
EV_DIR     = DOCS_DIR / "events"
CHANGELOG  = DOCS_DIR / "CHANGELOG.md"
TODAY      = date.today().isoformat()
RATE_DELAY = 0.5

SL_WIKI = "https://wiki.secondlife.com"

FETCH_TYPE = "all"
LIMIT      = None
TARGET     = None
DISCOVER   = False

for a in sys.argv[1:]:
    if a.startswith("--type="):    FETCH_TYPE = a.split("=",1)[1]
    elif a.startswith("--limit="): LIMIT = int(a.split("=",1)[1])
    elif a.startswith("--name="):  TARGET = a.split("=",1)[1]; FETCH_TYPE = "single"
    elif a == "--discover":        DISCOVER = True


# ── HTML utilities ────────────────────────────────────────────────────────────

def strip_tags(html: str) -> str:
    """Strip all HTML tags, collapse whitespace."""
    text = re.sub(r"<[^>]+>", "", html)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def unescape(text: str) -> str:
    """Decode common HTML entities."""
    text = text.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
    text = text.replace("&quot;", '"').replace("&#160;", " ").replace("&nbsp;", " ")
    text = text.replace("&#124;", "|").replace("&#39;", "'")
    text = text.replace("&mdash;", "—").replace("&ndash;", "–").replace("&bull;", "•")
    text = text.replace("&rarr;", "→").replace("&larr;", "←").replace("&hellip;", "…")
    text = re.sub(r"&#(\d+);", lambda m: chr(int(m.group(1))), text)
    return text


def html_to_markdown(html: str) -> str:
    """
    Convert a snippet of MediaWiki-rendered HTML to clean Markdown.
    Handles: code blocks, lists, links, bold/italic, paragraphs, simple tables.
    """
    # ── Code blocks ─────────────────────────────────────────────────────────
    # Wiki LSL code blocks: <div class="mw-highlight ..."><pre>...</pre></div>
    def replace_code_block(m):
        inner = m.group(1)
        # Strip span tags (syntax highlighting spans)
        code = re.sub(r"<span[^>]*>|</span>", "", inner)
        code = re.sub(r"<[^>]+>", "", code)
        code = unescape(code).rstrip()
        return f"\n\n```lsl\n{code}\n```\n\n"

    html = re.sub(
        r'<div[^>]*class="[^"]*mw-highlight[^"]*"[^>]*>\s*<pre[^>]*>(.*?)</pre>\s*</div>',
        replace_code_block, html, flags=re.DOTALL
    )
    # Bare <pre> tags
    html = re.sub(
        r"<pre[^>]*>(.*?)</pre>",
        lambda m: f"\n\n```lsl\n{unescape(re.sub(r'<[^>]+>','',m.group(1))).rstrip()}\n```\n\n",
        html, flags=re.DOTALL
    )
    # Inline <code>
    html = re.sub(r"<code[^>]*>(.*?)</code>",
                  lambda m: f"`{strip_tags(m.group(1))}`", html, flags=re.DOTALL)

    # ── Headings ─────────────────────────────────────────────────────────────
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

    # ── Lists ────────────────────────────────────────────────────────────────
    # Process only LEAF lists (no nested ul/ol inside) — inner-to-outer pass.
    # This avoids the non-greedy regex eating outer-open to inner-close.
    LEAF_LIST = re.compile(
        r"<(ul|ol)[^>]*>((?:(?!<(?:ul|ol)\b).)*?)</(ul|ol)>",
        re.DOTALL
    )

    def convert_list(m):
        tag        = m.group(1)
        items_html = m.group(2)
        bullet     = "1. " if tag == "ol" else "- "
        # Extract <li> items — safe here because no nested lists remain
        items = re.findall(r"<li[^>]*>(.*?)</li>", items_html, re.DOTALL)
        lines = []
        for item in items:
            text = html_to_markdown(item).strip()
            # Indent any already-converted sub-lists
            text = re.sub(r"\n(- |[0-9]+\. )", r"\n  \1", text)
            lines.append(f"{bullet}{text}")
        return "\n" + "\n".join(lines) + "\n"

    for _ in range(8):  # up to 8 levels of nesting
        new_html = LEAF_LIST.sub(convert_list, html)
        if new_html == html:
            break
        html = new_html

    # ── Tables ───────────────────────────────────────────────────────────────
    # Detect "bullet-style" tables (e.g. See Also): first data cell is a bullet •
    # Convert those to bullet lists; convert all others to Markdown tables.
    # NOTE: do NOT do a separate <tr> pass before this — that causes <table> wrappers
    # to eat the already-converted content when convert_table runs afterward.
    _BULLET_CHARS = {"•", "·", "‣", "&bull;", "&#8226;"}

    def convert_table(m):
        content   = m.group(1)
        rows_html = re.findall(r"<tr[^>]*>(.*?)</tr>", content, re.DOTALL)
        if not rows_html:
            return ""

        data_rows = [r for r in rows_html if re.search(r"<td", r)]

        # Detect bullet-style table
        is_bullet = False
        if data_rows:
            first_cells = re.findall(r"<td[^>]*>(.*?)</td>", data_rows[0], re.DOTALL)
            if first_cells:
                raw  = strip_tags(first_cells[0]).strip()
                text = unescape(raw).strip()
                is_bullet = text in _BULLET_CHARS or raw in _BULLET_CHARS

        if is_bullet:
            lines = []
            for row_html in data_rows:
                cells_html = re.findall(r"<td[^>]*>(.*?)</td>", row_html, re.DOTALL)
                entries = []
                for cell_html in cells_html:
                    # Prefer the visible text of an <a> link
                    link_m = re.search(r"<a[^>]*>(.*?)</a>", cell_html, re.DOTALL)
                    text = unescape(strip_tags(
                        link_m.group(1) if link_m else cell_html
                    )).strip()
                    if text and text not in _BULLET_CHARS and text not in ("–", "—", "-"):
                        entries.append(text)
                if not entries:
                    continue
                name = entries[0]
                desc = entries[1] if len(entries) > 1 else ""
                if desc:
                    lines.append(f"- **{name}** — {desc}")
                else:
                    lines.append(f"- {name}")
            return ("\n" + "\n".join(lines) + "\n") if lines else ""

        # Regular table → Markdown table
        rows = []
        for row_html in rows_html:
            cells = re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", row_html, re.DOTALL)
            cells = [strip_tags(c).strip() for c in cells]
            if any(cells):
                rows.append(cells)
        if not rows:
            return ""
        max_cols = max(len(r) for r in rows)
        lines = []
        for i, row in enumerate(rows):
            while len(row) < max_cols:
                row.append("")
            row = [c.replace("|", "\\|") for c in row]
            lines.append("| " + " | ".join(row) + " |")
            if i == 0:
                lines.append("|" + "|".join(" --- " for _ in row) + "|")
        return "\n" + "\n".join(lines) + "\n"

    html = re.sub(r"<table[^>]*>(.*?)</table>", convert_table, html, flags=re.DOTALL)

    # ── Inline formatting ────────────────────────────────────────────────────
    html = re.sub(r"<(?:b|strong)[^>]*>(.*?)</(?:b|strong)>",
                  lambda m: f"**{strip_tags(m.group(1))}**", html, flags=re.DOTALL)
    html = re.sub(r"<(?:i|em)[^>]*>(.*?)</(?:i|em)>",
                  lambda m: f"*{strip_tags(m.group(1))}*", html, flags=re.DOTALL)

    # ── Links ────────────────────────────────────────────────────────────────
    # Internal wiki links → plain text; external → [text](url)
    html = re.sub(
        r'<a[^>]+href="(/wiki/[^"]+)"[^>]*>(.*?)</a>',
        lambda m: strip_tags(m.group(2)),
        html, flags=re.DOTALL
    )
    html = re.sub(
        r'<a[^>]+href="(https?://[^"]+)"[^>]*>(.*?)</a>',
        lambda m: f"[{strip_tags(m.group(2))}]({m.group(1)})",
        html, flags=re.DOTALL
    )

    # ── Paragraphs and remaining tags ────────────────────────────────────────
    html = re.sub(r"<p[^>]*>", "\n\n", html)
    html = re.sub(r"</p>", "", html)
    html = re.sub(r"<br\s*/?>", "  \n", html)
    html = re.sub(r"<sup[^>]*>.*?</sup>", "", html, flags=re.DOTALL)  # strip footnotes
    # Only strip tags that start with a letter, / or ! to avoid eating
    # literal text like "<200/10sec" that the wiki author left unescaped.
    html = re.sub(r"<[a-zA-Z/!][^>]*>", "", html)

    # ── Cleanup ──────────────────────────────────────────────────────────────
    text = unescape(html)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\*\*\s*\*\*", "", text)
    # Remove empty inline code spans (`` with nothing between) but NOT ``` fences
    text = re.sub(r"(?<!`)`{2}(?!`)", "", text)
    return text.strip()


# ── Page parser ───────────────────────────────────────────────────────────────

WANT_SECTIONS = {"Caveats", "Examples", "Example", "Notes", "See Also"}
SKIP_SECTIONS = {"Deep Notes", "Haiku", "Footnotes", "Signature"}

class LSLWikiPage:
    def __init__(self, name: str):
        self.name        = name
        self.url         = f"{SL_WIKI}/wiki/{urllib.parse.quote(name)}"
        self.html        = ""
        self.signature   = ""
        self.delay       = ""
        self.energy      = ""
        self.description = ""
        self.sections    = {}  # {name: markdown}

    def fetch(self) -> bool:
        req = urllib.request.Request(
            self.url,
            headers={"User-Agent": "LSL-Cache-Bot/1.0 (local doc tool)"}
        )
        try:
            with urllib.request.urlopen(req, timeout=15) as r:
                self.html = r.read().decode("utf-8", errors="replace")
            return True
        except Exception as e:
            print(f"FAIL ({e})")
            return False

    def parse(self):
        html = self.html

        # Remove display:none translation noise
        html = re.sub(r'<span[^>]*display:\s*none[^>]*>.*?</span>', '', html, flags=re.DOTALL)
        html = re.sub(r'<div[^>]*id="multilang"[^>]*>.*?</div>', '', html, flags=re.DOTALL)

        # ── Delay and Energy from collapsible stats table ────────────────────
        delay_m = re.search(
            r'title="The number of seconds[^"]*"[^>]*>([0-9.]+)<', html
        )
        if delay_m:
            v = delay_m.group(1)
            self.delay = v if v not in ("0", "0.0") else ""

        energy_m = re.search(
            r'title="The quantity of energy[^"]*"[^>]*>([0-9.]+)<', html
        )
        if energy_m:
            self.energy = energy_m.group(1)

        # ── Official signature ───────────────────────────────────────────────
        # The signature is in a span with style="display:block" that contains
        # "Function:" or "Event:" text — distinct from the h2 span#Summary
        sig_m = re.search(
            r'<span[^>]*display:block[^>]*>\s*<a[^>]*>(?:Function|Event)</a>\s*:\s*(.*?)</span>',
            html, re.DOTALL
        )
        if sig_m:
            raw = sig_m.group(1)
            # Extract return type from first link or bold before the function name
            # Reconstruct: ReturnType FuncName(params);
            raw = re.sub(r'<span[^>]*title="([^"]*)"[^>]*>([^<]+)</span>',
                         r'\2', raw)  # param tooltips → just the name
            sig_text = strip_tags(raw).strip().rstrip(";").strip()
            self.signature = sig_text

        # ── Description ──────────────────────────────────────────────────────
        # First <p> after the stats table inside the summary box
        desc_m = re.search(
            r'<table class="collapsible">.*?</table>.*?<p>(.*?)</p>',
            html, re.DOTALL
        )
        if desc_m:
            self.description = unescape(strip_tags(desc_m.group(1))).strip()

        # ── Named sections ───────────────────────────────────────────────────
        # Split on div#box markers; each section starts with an h2
        section_chunks = re.split(r'<div id="box">', html)
        for chunk in section_chunks[1:]:  # skip preamble
            # Get h2 id and visible text
            h2_m = re.search(r'<h2[^>]*>.*?id="([^"]+)".*?>(.*?)</h2>', chunk, re.DOTALL)
            if not h2_m:
                continue
            section_id   = h2_m.group(1).replace("_", " ")
            section_name = unescape(strip_tags(h2_m.group(2))).strip()

            if section_name in SKIP_SECTIONS or section_id in SKIP_SECTIONS:
                continue
            if section_name not in WANT_SECTIONS and section_id not in WANT_SECTIONS:
                continue

            # Content is everything after the h2
            content_html = chunk[h2_m.end():]
            # Stop before the next major section
            content_html = re.split(r'<h2\b|<div class="printfooter', content_html)[0]
            try:
                md = html_to_markdown(content_html)
            except Exception as exc:
                print(f"WARN section parse failed [{self.name}:{section_name}] ({exc})")
                continue
            if md.strip():
                display_name = section_name if section_name in WANT_SECTIONS else section_id
                self.sections[display_name] = md

    def wiki_block(self) -> str:
        """Return the merged wiki content as a Markdown block."""
        parts = []

        if self.description:
            parts.append(self.description)

        for sec in ("Caveats", "Examples", "Example", "Notes", "See Also"):
            if sec in self.sections:
                display = "Examples" if sec == "Example" else sec
                parts.append(f"## {display}\n\n{self.sections[sec]}")

        return "\n\n".join(parts)

    def has_content(self) -> bool:
        return bool(self.sections)


# ── Doc merger ────────────────────────────────────────────────────────────────

MARKER_START = "<!-- wiki-source -->"
MARKER_END   = "<!-- /wiki-source -->"


def merge_into_doc(doc_path: Path, page: LSLWikiPage) -> bool:
    existing = doc_path.read_text(encoding="utf-8")
    content  = page.wiki_block().strip()
    if not content:
        return False

    block_payload = (
        f"_Source: [SL Wiki]({page.url}) — scraped {TODAY}_\n\n"
        f"{content}"
    )
    chunk_hash = hashlib.sha1(block_payload.encode("utf-8")).hexdigest()[:12]
    marker = f"<!-- wiki-source-chunk:{chunk_hash} -->"

    if marker in existing:
        return False

    block = (
        f"\n\n{marker}\n"
        f"{MARKER_START}\n"
        f"{block_payload}\n"
        f"{MARKER_END}\n"
    )

    with open(doc_path, "a", encoding="utf-8") as fh:
        fh.write(block)
    return True


# ── Discovery: find wiki pages not yet in cache ───────────────────────────────

def _fetch_html(url: str) -> str:
    """Fetch a URL with the standard LSL-Cache-Bot user agent."""
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "LSL-Cache-Bot/1.0 (local doc tool)"}
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.read().decode("utf-8", errors="replace")
    except Exception as e:
        print(f"  [fetch error] {url}: {e}", flush=True)
        return ""


def _extract_page_links(html: str, category: str) -> list:
    """
    Extract (name, wiki_url) pairs from an LSL wiki category page.
    category: "functions" → collect links whose path starts with /wiki/ll
              "events"    → collect any /wiki/ links in the mw-pages div
    """
    results = []
    # Narrow to the mw-pages div first if present; otherwise use full page
    pages_m = re.search(r'<div[^>]*id="mw-pages"[^>]*>(.*?)</div>\s*</div>', html, re.DOTALL)
    search_html = pages_m.group(1) if pages_m else html

    for m in re.finditer(r'<a[^>]*href="(/wiki/([^"#/][^"#]*?))"[^>]*>([^<]+)</a>', search_html):
        path  = m.group(1)
        name  = m.group(2)
        title = m.group(3).strip()
        # Skip category pages and special pages
        if ":" in name:
            continue
        if category == "functions" and not name.startswith("ll"):
            continue
        wiki_url = SL_WIKI + path
        results.append((name, wiki_url))
    return results


def _follow_category_pages(start_url: str, category: str) -> list:
    """
    Follow pagination on an LSL wiki category page and collect all page links.
    Returns deduplicated list of (name, wiki_url).
    """
    results = []
    seen_urls = set()
    next_url  = start_url

    while next_url:
        time.sleep(RATE_DELAY)
        html = _fetch_html(next_url)
        if not html:
            break

        links = _extract_page_links(html, category)
        for item in links:
            if item[1] not in seen_urls:
                seen_urls.add(item[1])
                results.append(item)

        # Follow pagination
        next_m = re.search(
            r'<a href="([^"]*(?:pagefrom|from)[^"]*)"[^>]*>[^<]*next[^<]*</a>',
            html, re.IGNORECASE
        )
        if next_m:
            next_path = unescape(next_m.group(1))
            if next_path.startswith("http"):
                next_url = next_path
            else:
                next_url = SL_WIKI + next_path
        else:
            next_url = None

    return results


def _first_prose(html: str) -> str:
    """Extract first meaningful prose paragraph from page HTML."""
    cm = re.search(r'<div[^>]*id="mw-content-text"[^>]*>(.*?)<div[^>]*class="[^"]*printfooter',
                   html, re.DOTALL)
    content = cm.group(1) if cm else html
    for pm in re.finditer(r'<p[^>]*>(.*?)</p>', content, re.DOTALL):
        text = unescape(strip_tags(pm.group(1))).strip()
        if len(text) > 20 and not text.startswith('{') and not text.startswith('|'):
            return text[:300]
    return ""


def discover_new_pages() -> list:
    """
    Fetch LSL wiki categories to find function/event pages not yet in cache.
    Returns list of (name, wiki_url, dest_dir) for pages that don't exist yet.
    """
    CAT_FUNCTIONS = f"{SL_WIKI}/wiki/Category:LSL_Functions"
    CAT_EVENTS    = f"{SL_WIKI}/wiki/Category:LSL_Events"

    print("Discovering new LSL function pages from wiki category...", flush=True)
    fn_links = _follow_category_pages(CAT_FUNCTIONS, "functions")
    print(f"  Found {len(fn_links)} function page(s) on wiki", flush=True)

    print("Discovering new LSL event pages from wiki category...", flush=True)
    ev_links = _follow_category_pages(CAT_EVENTS, "events")
    print(f"  Found {len(ev_links)} event page(s) on wiki", flush=True)

    new_pages = []
    for name, wiki_url in fn_links:
        if not (FN_DIR / f"{name}.md").exists():
            new_pages.append((name, wiki_url, FN_DIR))

    for name, wiki_url in ev_links:
        if not (EV_DIR / f"{name}.md").exists():
            new_pages.append((name, wiki_url, EV_DIR))

    print(f"  {len(new_pages)} page(s) not yet in cache", flush=True)
    return new_pages


def save_new_doc(name: str, wiki_url: str, dest_dir: Path, html: str) -> bool:
    """
    Save a newly discovered wiki page as a new .md doc with YAML front matter.
    Only saves if the file does not already exist.
    Returns True if saved, False otherwise.
    """
    out_path = dest_dir / f"{name}.md"
    if out_path.exists():
        return False  # never overwrite

    # Determine category from destination dir
    is_event = dest_dir == EV_DIR

    # Extract content area
    cm = re.search(
        r'<div[^>]*id="mw-content-text"[^>]*>(.*?)<div[^>]*class="[^"]*printfooter',
        html, re.DOTALL
    )
    content_html = cm.group(1) if cm else html

    desc = _first_prose(html)
    body = html_to_markdown(content_html)

    # Extract signature from page if present
    sig_m = re.search(
        r'<span[^>]*display:block[^>]*>\s*<a[^>]*>(?:Function|Event)</a>\s*:\s*(.*?)</span>',
        html, re.DOTALL
    )
    signature = ""
    if sig_m:
        raw = re.sub(r'<span[^>]*title="([^"]*)"[^>]*>([^<]+)</span>', r'\2', sig_m.group(1))
        signature = strip_tags(raw).strip().rstrip(";").strip()

    category = "event" if is_event else "function"
    desc_safe = desc.replace('"', '\\"')
    sig_safe  = signature.replace('"', '\\"')

    front = f"""---
name: "{name}"
category: "{category}"
type: "{category}"
language: "LSL"
description: "{desc_safe}"
signature: "{sig_safe}"
wiki_url: "{wiki_url}"
first_fetched: "{TODAY}"
last_updated: "{TODAY}"
---
"""
    out_path.write_text(front + "\n" + body, encoding="utf-8")
    return True


# ── Main ──────────────────────────────────────────────────────────────────────

def get_targets() -> list[tuple[str, Path]]:
    if FETCH_TYPE == "single" and TARGET:
        for d in (FN_DIR, EV_DIR):
            p = d / f"{TARGET}.md"
            if p.exists():
                return [(TARGET, p)]
        print(f"ERROR: {TARGET}.md not found.")
        return []

    targets = []
    if FETCH_TYPE in ("all", "functions") and FN_DIR.exists():
        targets += [(p.stem, p) for p in sorted(FN_DIR.glob("*.md"))]
    if FETCH_TYPE in ("all", "events") and EV_DIR.exists():
        targets += [(p.stem, p) for p in sorted(EV_DIR.glob("*.md"))]
    if LIMIT:
        targets = targets[:LIMIT]
    return targets


def main():
    print(f"scrape-wiki-pages v0.1.3.1 — {TODAY}", flush=True)
    print(f"Cache: {CACHE_ROOT}", flush=True)
    if LIMIT:
        print(f"Limit: {LIMIT} pages", flush=True)
    print(flush=True)

    # ── Discovery mode ────────────────────────────────────────────────────────
    if DISCOVER:
        print("=== Discovery mode: finding new wiki pages ===", flush=True)
        FN_DIR.mkdir(parents=True, exist_ok=True)
        EV_DIR.mkdir(parents=True, exist_ok=True)

        new_pages = discover_new_pages()
        if not new_pages:
            print("No new pages found — cache is up to date.", flush=True)
        else:
            print(f"\nDownloading {len(new_pages)} new page(s)...", flush=True)
            discovered_saved = 0
            for i, (name, wiki_url, dest_dir) in enumerate(new_pages, 1):
                print(f"  [{i}/{len(new_pages)}] {name}", end=" ", flush=True)
                time.sleep(RATE_DELAY)
                html = _fetch_html(wiki_url)
                if not html:
                    print("— fetch error", flush=True)
                    continue
                saved = save_new_doc(name, wiki_url, dest_dir, html)
                if saved:
                    discovered_saved += 1
                    print(f"— saved to {dest_dir.name}/", flush=True)
                else:
                    print("— skipped (exists)", flush=True)

            print(f"\nDiscovery complete: {discovered_saved} new doc(s) saved.", flush=True)

            if discovered_saved > 0:
                entry  = f"\n## {TODAY} — Wiki discovery\n"
                entry += f"- Discovered and saved {discovered_saved} new LSL doc(s) not previously in cache\n"
                CHANGELOG.write_text(CHANGELOG.read_text(encoding="utf-8") + entry, encoding="utf-8")

        print(flush=True)

    # ── Enrichment mode (always runs unless only --discover was requested with no targets) ──
    targets = get_targets()
    if not targets:
        if not DISCOVER:
            print("No targets to process.", flush=True)
        return

    total  = len(targets)
    merged = skipped = failed = 0

    print(f"Processing {total} docs for wiki content enrichment...\n", flush=True)

    for i, (name, doc_path) in enumerate(targets, 1):
        print(f"  [{i:>4}/{total}] {name:<40}", end=" ", flush=True)

        page = LSLWikiPage(name)
        try:
            if not page.fetch():
                failed += 1
                time.sleep(RATE_DELAY)
                continue

            page.parse()

            if not page.has_content():
                print("(no wiki content)", flush=True)
                skipped += 1
                time.sleep(RATE_DELAY)
                continue

            changed = merge_into_doc(doc_path, page)
            secs    = list(page.sections.keys())
            print(f"OK [{', '.join(secs)}]" if changed else "(no change)", flush=True)
            merged  += 1 if changed else 0
            skipped += 0 if changed else 1
        except Exception as exc:
            print(f"FAIL (parse/merge error: {exc})", flush=True)
            tb = traceback.format_exc(limit=2).strip().splitlines()[-1]
            if tb:
                print(f"    {tb}", flush=True)
            failed += 1

        time.sleep(RATE_DELAY)

    # Changelog
    entry  = f"\n## {TODAY} — Wiki HTML scrape\n"
    entry += f"- Scraped {total} pages from wiki.secondlife.com\n"
    entry += f"- Merged (Caveats/Examples/Notes/See Also): {merged}\n"
    entry += f"- Skipped: {skipped}, Failed (not found): {failed}\n"
    CHANGELOG.write_text(CHANGELOG.read_text(encoding="utf-8") + entry, encoding="utf-8")

    print(flush=True)
    print(f"Done.  Merged: {merged}  Skipped: {skipped}  Failed: {failed}", flush=True)


if __name__ == "__main__":
    main()
