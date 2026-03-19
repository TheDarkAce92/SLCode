#!/usr/bin/env python3
# Skill: fetch-extra-libraries
# Version: 0.2.3.0
# Purpose: Fetch LSL script examples from GitHub repos and web libraries not on the SL wiki
# Usage: python3 fetch-extra-libraries.py [--force] [--limit N] [--source ID]
# Created: 2026-03-17
# Last modified: 2026-03-18

"""
Fetches LSL scripts from four additional sources:
  - https://outworldz.com/lib/                          (web index page)
  - github.com/AbsolutelyCraiCrai/lsl-scripts-lib       (GitHub)
  - github.com/Outworldz/LSL-Scripts                    (GitHub)
  - github.com/AvaCon/LSL-OpenSim-Script-Library        (GitHub)

Scripts are saved to lsl-docs/examples/ with YAML front matter.
Overlap is detected by normalised filename and content hash — duplicates
from any source (including the existing SL wiki examples) are skipped.

Updates cache-manifest.json on completion.
"""

import hashlib
import io
import json
import os
import re
import ssl
import sys
import tempfile
import time
import urllib.parse
import urllib.request
import zipfile
from datetime import date
from pathlib import Path
from collections import defaultdict

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# ── Config ───────────────────────────────────────────────────────────────────

_env_base  = os.environ.get("LSL_CACHE_BASE", "").strip()
CACHE_ROOT = Path(_env_base) if _env_base else Path(__file__).resolve().parents[1]
DOCS_DIR   = CACHE_ROOT / "lsl-docs"
OUT_DIR    = DOCS_DIR / "examples"
CHANGELOG  = DOCS_DIR / "CHANGELOG.md"
MANIFEST   = CACHE_ROOT / "cache-manifest.json"
TODAY      = date.today().isoformat()
RATE_DELAY = 0.4

FORCE      = "--force" in sys.argv
LIMIT      = None
SOURCE_ID  = None

for a in sys.argv[1:]:
    if a.startswith("--limit="):  LIMIT     = int(a.split("=", 1)[1])
    elif a.startswith("--source="): SOURCE_ID = a.split("=", 1)[1]

OUT_DIR.mkdir(parents=True, exist_ok=True)

# ── Sources ───────────────────────────────────────────────────────────────────

SOURCES = [
    {
        "id":      "outworldz-web",
        "type":    "web",
        "name":    "Outworldz Script Library",
        "url":     "https://outworldz.com/lib/",
        "lang":    "LSL",
    },
    {
        "id":      "absolutelycraicrai",
        "type":    "github",
        "name":    "AbsolutelyCraiCrai LSL Scripts",
        "owner":   "AbsolutelyCraiCrai",
        "repo":    "lsl-scripts-lib",
        "lang":    "LSL",
    },
    {
        "id":      "outworldz-github",
        "type":    "github",
        "name":    "Outworldz LSL Scripts (GitHub)",
        "owner":   "Outworldz",
        "repo":    "LSL-Scripts",
        "lang":    "LSL",
    },
    {
        "id":      "avacon-opensim",
        "type":    "github",
        "name":    "AvaCon OpenSim Script Library",
        "owner":   "AvaCon",
        "repo":    "LSL-OpenSim-Script-Library",
        "lang":    "LSL",
    },
]

# Extensions treated as LSL scripts
LSL_EXTS = {".lsl", ".sl", ".lslp", ".lslm"}
# Also accept companion file types (notecards, docs, changelogs, licences).
DOC_EXTS = {".txt", ".md"}
LSL_KEYWORDS_RE = re.compile(
    r'\b(default\s*\{|state\s+\w+\s*\{|state_entry\s*\(|touch_start\s*\(|listen\s*\(|timer\s*\(|on_rez\s*\(|changed\s*\(|dataserver\s*\(|http_response\s*\(|link_message\s*\(|sensor\s*\(|no_sensor\s*\(|ll[A-Z]\w*\s*\(|integer\s+\w|float\s+\w|string\s+\w|list\s+\w|vector\s+\w|rotation\s+\w|key\s+\w)',
    re.DOTALL,
)

_DOC_KIND_LICENSE_RE = re.compile(r'\b(licen[cs]e|eula|copyright|gpl|mit|apache|bsd)\b', re.IGNORECASE)
_DOC_KIND_NOTECARD_RE = re.compile(r'\b(notecard|note\s*card|route|waypoint)\b', re.IGNORECASE)
_DOC_KIND_CONFIG_RE = re.compile(r'\b(config|settings?|ini|menuitems?|positions?|channel|param)\b', re.IGNORECASE)
_DOC_KIND_USERDOC_RE = re.compile(r'\b(readme|manual|install|usage|history|changelog|attribution|docs?|documentation|help|guide)\b', re.IGNORECASE)

PROJECT_MARKERS = {
    "readme.md",
    "readme.txt",
    "project.json",
    "requirements.txt",
    "pyproject.toml",
    "package.json",
    ".sln",
    ".gitmodules",
}


# ── HTTP helpers ──────────────────────────────────────────────────────────────

HEADERS = {
    "Accept":     "text/html,application/xhtml+xml,application/json,*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) SLCode/1.0 LSL-cache-builder",
}

GH_HEADERS = {
    "Accept":     "application/vnd.github+json",
    "User-Agent": "SLCode/1.0 LSL-cache-builder",
}

# Permissive SSL context — frozen-exe CA bundle may be incomplete
_SSL_CTX = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
_SSL_CTX.check_hostname = False
_SSL_CTX.verify_mode    = ssl.CERT_NONE


def fetch(url: str, headers: dict = HEADERS, timeout: int = 20) -> str:
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=_SSL_CTX) as r:
            ct = r.headers.get_content_charset("utf-8")
            return r.read().decode(ct, errors="replace")
    except Exception as e:
        print(f"  [fetch error] {url}: {e}", flush=True)
        return ""


def fetch_json(url: str, headers: dict = GH_HEADERS) -> dict | list | None:
    raw = fetch(url, headers=headers)
    if not raw:
        return None
    try:
        return json.loads(raw)
    except Exception:
        return None


def fetch_bytes(url: str, headers: dict = HEADERS, timeout: int = 45, label: str = "") -> bytes:
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=_SSL_CTX) as r:
            total = int(r.headers.get("Content-Length") or 0)
            tag   = f"  Downloading {label}" if label else "  Downloading"
            chunks, received = [], 0
            while True:
                chunk = r.read(65536)
                if not chunk:
                    break
                chunks.append(chunk)
                received += len(chunk)
                kb = received // 1024
                if total:
                    pct = received * 100 // total
                    print(f"{tag}: {kb} KB / {total//1024} KB ({pct}%)", end="\r", flush=True)
                else:
                    print(f"{tag}: {kb} KB...", end="\r", flush=True)
            mb = received / 1024 / 1024
            print(f"{tag}: {mb:.1f} MB — done.                    ", flush=True)
            return b"".join(chunks)
    except Exception as e:
        print(f"  [fetch error] {url}: {e}", flush=True)
        return b""


# ── Deduplication ─────────────────────────────────────────────────────────────

def _norm_name(name: str) -> str:
    """Normalise a script name for duplicate detection."""
    n = name.lower()
    n = re.sub(r'[\s\-_]+', '', n)
    n = re.sub(r'\.(lsl|sl|lslp|lslm|txt|md)$', '', n)
    return n


def _content_hash(content: str) -> str:
    return hashlib.md5(
        re.sub(r'\s+', ' ', content).strip().encode("utf-8", errors="replace")
    ).hexdigest()


def _extract_lsl_from_markdown(text: str) -> str:
    m = re.search(r"```(?:lsl)?\s*(.*?)\n```", text, re.DOTALL | re.IGNORECASE)
    if m:
        return m.group(1).strip()
    body = re.split(r'^---\s*$', text, maxsplit=2, flags=re.MULTILINE)
    return (body[-1] if len(body) >= 2 else text).strip()


def _build_existing_index() -> tuple[set, set]:
    """Return (normalised_names, content_hashes) from existing examples."""
    names   = set()
    hashes  = set()
    if not OUT_DIR.exists():
        return names, hashes
    for p in OUT_DIR.glob("*.md"):
        names.add(_norm_name(p.stem))
        try:
            txt = p.read_text(encoding="utf-8", errors="replace")
            code_section = _extract_lsl_from_markdown(txt)
            if code_section:
                hashes.add(_content_hash(code_section))
        except Exception:
            pass
    return names, hashes


# ── LSL helpers ───────────────────────────────────────────────────────────────

def classify_doc_kind(source_name: str, content: str) -> str:
    """Classify source content for UI ordering and rendering."""
    src = (source_name or "").lower()
    name = Path(src).name
    ext = Path(src).suffix.lower()
    preview = (content or "")[:4000].lower()

    if ext in LSL_EXTS:
        return "script"

    # .md files are almost always user-facing docs — classify by name first
    if ext == ".md":
        combined = f"{name}\n{preview}"
        if _DOC_KIND_LICENSE_RE.search(combined):
            return "license"
        if _DOC_KIND_USERDOC_RE.search(combined):
            return "user-doc"
        # .md files containing LSL code blocks are treated as examples
        if "```lsl" in (content or "").lower() or LSL_KEYWORDS_RE.search(content or ""):
            return "script"
        return "user-doc"

    combined = f"{name}\n{preview}"
    if _DOC_KIND_LICENSE_RE.search(combined):
        return "license"
    if _DOC_KIND_NOTECARD_RE.search(combined):
        return "notecard"
    if _DOC_KIND_CONFIG_RE.search(combined):
        return "config"
    if _DOC_KIND_USERDOC_RE.search(combined):
        return "user-doc"
    if ext == ".txt" and LSL_KEYWORDS_RE.search(content or ""):
        return "script"
    return "user-doc"

def is_lsl_content(filename: str, content: str) -> bool:
    ext = Path(filename).suffix.lower()
    if ext in LSL_EXTS:
        return True
    if ext in DOC_EXTS:
        return True
    return False


_OW_META_KEY_RE = re.compile(r'^:(?:CATEGORY|NAME|AUTHOR|CREATED|EDITED|ID|NUM|REV|WORLD|DESCRIPTION|CODE):')

def extract_description(content: str) -> str:
    """Extract a description from LSL script comments or first non-empty line."""
    # Outworldz metadata: :DESCRIPTION: may be inline or on its own line with content on next // line
    # Format A (inline):    // :DESCRIPTION: Some text
    # Format B (multiline): // :DESCRIPTION:\n// Some text\n// :CODE:
    ow_inline = re.search(r':DESCRIPTION:[ \t]+(.+)', content)
    if ow_inline:
        # strip trailing :CODE: or other tags
        desc = re.sub(r'\s*:[A-Z]+:.*$', '', ow_inline.group(1)).strip()
        if len(desc) > 5:
            return desc[:300]
    # Multiline: find :DESCRIPTION: line, grab next non-meta, non-empty // line
    ow_ml = re.search(r':DESCRIPTION:\s*\n\s*//\s*(.+)', content)
    if ow_ml:
        desc = ow_ml.group(1).strip()
        if not _OW_META_KEY_RE.match(desc) and len(desc) > 5:
            return desc[:300]

    # Block comment at top: /* ... */
    bm = re.match(r'\s*/\*(.*?)\*/', content, re.DOTALL)
    if bm:
        lines = [l.strip().lstrip('*').strip() for l in bm.group(1).splitlines()]
        prose = ' '.join(l for l in lines if l and not l.startswith('@'))
        if len(prose) > 10:
            return prose[:300]

    # Line comments at top: // ... — skip Outworldz :KEY: metadata lines
    lines = []
    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith("//"):
            body = stripped[2:].strip()
            if _OW_META_KEY_RE.match(body):
                continue   # skip :CATEGORY:, :NAME:, etc.
            lines.append(body)
        elif stripped == "" and lines:
            break
        elif stripped and not stripped.startswith("//"):
            break
    if lines:
        prose = ' '.join(l for l in lines if l)
        if len(prose) > 10:
            return prose[:300]

    return ""


def script_to_markdown(filename: str, content: str, doc_kind: str = "script") -> str:
    if doc_kind in {"script", "notecard", "config"}:
        return f"```lsl\n{content.rstrip()}\n```\n"
    if doc_kind == "license":
        return f"```text\n{content.rstrip()}\n```\n"
    return content.rstrip() + "\n"


# ── File writer ───────────────────────────────────────────────────────────────

def _json_str(s: str) -> str:
    return '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'


def _slugify(s: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", s.strip().lower()).strip("-")
    return slug or "root"


def _humanize_stem(stem: str) -> str:
    """Convert a raw script stem to a human-readable name.

    Strips a trailing part-number suffix (e.g. _1, -2, ' 3') and converts
    underscore/hyphen word-separators to spaces.
    """
    name = re.sub(r'[-_ ]+\d+$', '', stem)
    name = name or stem
    name = re.sub(r'[-_]+', ' ', name).strip()
    return name or stem


def _composed_name(stem: str, project_slug: str) -> str:
    """Build a human-readable composed name, avoiding redundant project prefix."""
    human    = _humanize_stem(stem)
    proj_h   = re.sub(r'[-_]+', ' ', project_slug).strip()
    if not proj_h or human.lower() == proj_h.lower():
        return human
    # If human name starts with project name (or vice versa — stem is a truncation),
    # just use whichever is longer (the project slug is usually more complete)
    if human.lower().startswith(proj_h.lower()):
        return human
    if proj_h.lower().startswith(human.lower()):
        return proj_h
    return f"{proj_h}: {human}"


def _next_available_path(stem: str) -> Path:
    base = OUT_DIR / f"{stem}.md"
    if not base.exists():
        return base
    i = 2
    while True:
        p = OUT_DIR / f"{stem}_{i}.md"
        if not p.exists():
            return p
        i += 1


# ── Version sidecar helpers ───────────────────────────────────────────────────

def _versions_dir(doc_path: Path) -> Path:
    return doc_path.parent / ".versions" / doc_path.stem


def _version_id(source_name: str) -> str:
    slug = re.sub(r'[^a-z0-9]+', '-', source_name.lower()).strip('-')
    return f"scraped-{slug}-{TODAY}"


def _save_sidecar(doc_path: Path, version_id: str, full_md_text: str):
    vdir = _versions_dir(doc_path)
    vdir.mkdir(parents=True, exist_ok=True)
    (vdir / f"{version_id}.md").write_text(full_md_text, encoding="utf-8")


def _mark_has_versions(doc_path: Path):
    """Ensure has_versions: \"true\" is in the active file's front matter."""
    text = doc_path.read_text(encoding="utf-8", errors="replace")
    if 'has_versions: "true"' in text:
        return
    text = re.sub(r'(\n---\n)', '\nhas_versions: "true"\\1', text, count=1)
    doc_path.write_text(text, encoding="utf-8")


def _parse_fm_simple(text: str) -> dict:
    """Extract key: \"value\" pairs from YAML front matter."""
    m = re.match(r'^---\n(.*?)\n---', text, re.DOTALL)
    if not m:
        return {}
    result = {}
    for line in m.group(1).splitlines():
        km = re.match(r'^([\w_]+)\s*:\s*"((?:[^"\\]|\\.)*)"', line)
        if km:
            result[km.group(1)] = km.group(2).replace('\\"', '"')
    return result


def save_script(stem: str, source_url: str, source_name: str,
                lang: str, content: str,
                description: str = "", meta: dict | None = None,
                doc_kind: str = "script") -> str:
    # display_name: human-readable (spaces OK, no filesystem-illegal chars)
    display_name = re.sub(r'[<>:"/\\|?*]', '', stem).strip()[:200]
    # safe: filename-safe (spaces → underscores)
    safe = re.sub(r'\s+', '_', display_name)[:100]
    desc = description or extract_description(content)
    body       = script_to_markdown(stem, content, doc_kind=doc_kind)
    version_id = _version_id(source_name)

    extra = ""
    if meta:
        for k, v in meta.items():
            if v is None:
                continue
            extra += f"{k}: {_json_str(str(v))}\n"

    def _build_front(first_fetched: str, has_versions: bool = False,
                     active_version: str = "") -> str:
        hv_line = 'has_versions: "true"\n' if has_versions else ''
        av_line = f'active_version: {_json_str(active_version)}\n' if active_version else ''
        return (
            f'---\n'
            f'name: {_json_str(display_name)}\n'
            f'category: "example"\n'
            f'type: "example"\n'
            f'language: {_json_str(lang)}\n'
            f'description: {_json_str(desc)}\n'
            f'source_url: {_json_str(source_url)}\n'
            f'source_name: {_json_str(source_name)}\n'
            f'{extra}'
            f'first_fetched: {_json_str(first_fetched)}\n'
            f'last_updated: {_json_str(TODAY)}\n'
            f'{hv_line}'
            f'{av_line}'
            f'---\n\n'
        )

    active_path = OUT_DIR / f"{safe}.md"
    if active_path.exists():
        existing    = active_path.read_text(encoding="utf-8", errors="replace")
        efm         = _parse_fm_simple(existing)
        first_fetch = efm.get("first_fetched", TODAY)

        # User-locked custom version — save new scraped as sidecar only
        if efm.get("custom") == "true":
            _save_sidecar(active_path, version_id, _build_front(first_fetch) + body)
            _mark_has_versions(active_path)
            return "sidecar"

        # Content changed — rotate existing to sidecar, write new as active
        old_ver_id = efm.get("active_version") or f"scraped-prev-{TODAY}"
        _save_sidecar(active_path, old_ver_id, existing)
        active_path.write_text(
            _build_front(first_fetch, has_versions=True, active_version=version_id) + body,
            encoding="utf-8",
        )
        return "updated"

    # New file — write fresh
    path = _next_available_path(safe)
    path.write_text(_build_front(TODAY) + body, encoding="utf-8")
    return "new"


def _analyse_repo_projects(tree_items: list[dict], script_paths: list[str]) -> tuple[dict[str, dict], list[dict]]:
    """
    Infer project grouping for script files from a repo tree.
    Returns: (path -> project metadata, summary list)
    """
    if not script_paths:
        return {}, []

    marker_dirs = set()
    for item in tree_items:
        path = item.get("path", "")
        if item.get("type") != "blob" or not path:
            continue
        name = Path(path).name.lower()
        if name in PROJECT_MARKERS:
            d = Path(path).parent.as_posix()
            marker_dirs.add("" if d == "." else d)

    top_counts = defaultdict(int)
    for p in script_paths:
        parts = Path(p).parts
        if parts:
            top_counts[parts[0]] += 1
        else:
            top_counts["root"] += 1

    candidate_dirs = set(marker_dirs)
    candidate_dirs.update(k for k, v in top_counts.items() if v >= 2)
    candidate_dirs.add("")

    counts = {}
    for d in candidate_dirs:
        if not d:
            counts[d] = len(script_paths)
            continue
        prefix = d + "/"
        counts[d] = sum(1 for p in script_paths if p == d or p.startswith(prefix))

    candidates = [d for d in candidate_dirs if counts.get(d, 0) >= 2 or d == ""]
    candidates.sort(key=lambda d: len(Path(d).parts), reverse=True)

    file_meta: dict[str, dict] = {}
    summary = defaultdict(lambda: {"count": 0, "confidence": "low"})

    # Large repos can contain deeply nested micro-folders that fragment project labels.
    # For very large libraries, prefer stable top-level family grouping.
    use_parent_family_mode = len(script_paths) >= 300

    for p in script_paths:
        project_dir = ""
        confidence = "low"
        for d in candidates:
            if not d:
                continue
            if p == d or p.startswith(d + "/"):
                project_dir = d
                confidence = "high" if d in marker_dirs else "medium"
                break

        if not project_dir:
            parts = Path(p).parts
            if len(parts) >= 2:
                project_dir = parts[0]
                confidence = "medium"
            else:
                project_dir = ""
                confidence = "low"

        if use_parent_family_mode and project_dir and "/" in project_dir:
            top = project_dir.split("/", 1)[0]
            if top_counts.get(top, 0) >= 20:
                project_dir = top
                if confidence == "high":
                    confidence = "medium"

        label = Path(project_dir).name if project_dir else "repo-root"
        slug = _slugify(project_dir or "repo-root")

        info = {
            "project_dir": project_dir,
            "project_label": label,
            "project_slug": slug,
            "project_confidence": confidence,
        }
        file_meta[p] = info
        summary[slug]["count"] += 1
        if confidence == "high" or summary[slug]["confidence"] == "low":
            summary[slug]["confidence"] = confidence

    summary_rows = []
    slug_to_label = {}
    for p, meta in file_meta.items():
        slug_to_label.setdefault(meta["project_slug"], meta["project_label"])
    for slug, stats in summary.items():
        summary_rows.append({
            "slug": slug,
            "label": slug_to_label.get(slug, slug),
            "count": stats["count"],
            "confidence": stats["confidence"],
        })
    summary_rows.sort(key=lambda r: (-r["count"], r["label"]))

    return file_meta, summary_rows


def _pull_repo_snapshot(owner: str, repo: str, branch: str) -> tuple[Path | None, Path | None]:
    """
    Download a GitHub repo branch as a zipball and extract locally.
    Returns (temp_dir, repo_root_dir).
    """
    zip_url = f"https://codeload.github.com/{owner}/{repo}/zip/refs/heads/{branch}"
    blob = fetch_bytes(zip_url, headers=GH_HEADERS, timeout=90, label=f"{owner}/{repo} archive")
    if not blob:
        return None, None

    temp_dir = Path(tempfile.mkdtemp(prefix=f"slcode-{owner}-{repo}-"))
    archive = temp_dir / "repo.zip"
    archive.write_bytes(blob)

    try:
        with zipfile.ZipFile(archive) as zf:
            members = zf.namelist()
            total_m = len(members)
            for i, member in enumerate(members, 1):
                zf.extract(member, temp_dir)
                if i % 500 == 0 or i == total_m:
                    print(f"  Extracting: {i}/{total_m} files...", end="\r", flush=True)
            print(f"  Extracted {total_m} files.                    ", flush=True)
    except Exception as e:
        print(f"  Could not extract repo snapshot: {e}", flush=True)
        return None, None

    roots = [p for p in temp_dir.iterdir() if p.is_dir()]
    if not roots:
        return None, None
    return temp_dir, roots[0]


# ── Multipart cluster detection ───────────────────────────────────────────────

_PART_SUFFIX_RE = re.compile(r"^(.+?)[-_ ](\d+)$")


def _detect_multipart_clusters(script_paths: list[str]) -> dict[str, tuple[int, int]]:
    """
    Detect SL-style multipart scripts: one logical script split across numbered
    files sharing a common base prefix, e.g.:
        Go_Game/Go_Game/Object/Go_Game_1.lsl  ..  Go_Game_11.lsl
        ~poser 1.lsl  ..  ~poser 5.lsl

    Returns a dict mapping each file path -> (part_index, part_total).
    Only paths that form a confirmed sequential cluster (starting at 0 or 1)
    are included; lone numbered files are excluded.
    """
    grouped: dict[tuple, list[tuple[int, str]]] = defaultdict(list)
    for p in script_paths:
        stem   = Path(p).stem
        parent = Path(p).parent.as_posix()
        m = _PART_SUFFIX_RE.match(stem)
        if m:
            base = m.group(1)
            num  = int(m.group(2))
            grouped[(parent, base)].append((num, p))

    result: dict[str, tuple[int, int]] = {}
    for (_parent, _base), items in grouped.items():
        if len(items) < 2:
            continue
        nums = sorted(n for n, _ in items)
        # Must be sequential starting at 0 or 1
        if nums[0] > 1 or nums[-1] != nums[0] + len(nums) - 1:
            continue
        total = len(nums)
        for num, path in items:
            result[path] = (num, total)
    return result


# ── GitHub source ─────────────────────────────────────────────────────────────

def _github_default_branch(owner: str, repo: str) -> str:
    data = fetch_json(f"https://api.github.com/repos/{owner}/{repo}")
    if isinstance(data, dict):
        return data.get("default_branch", "main")
    return "main"


def fetch_github(source: dict, existing_names: set, existing_hashes: set,
                 limit: int | None) -> tuple[int, int, int]:
    owner = source["owner"]
    repo  = source["repo"]
    name  = source["name"]
    lang  = source.get("lang", "LSL")

    print(f"\n[GitHub] {owner}/{repo}", flush=True)

    branch = _github_default_branch(owner, repo)
    time.sleep(RATE_DELAY)

    pull_dir, repo_root = _pull_repo_snapshot(owner, repo, branch)
    time.sleep(RATE_DELAY)

    if not repo_root:
        print(f"  Could not pull repo snapshot — skipping.", flush=True)
        return 0, 0, 1

    all_rel_files = []
    blobs = []
    for p in repo_root.rglob("*"):
        if not p.is_file():
            continue
        rel = p.relative_to(repo_root).as_posix()
        all_rel_files.append(rel)
        if p.suffix.lower() in LSL_EXTS | DOC_EXTS:
            blobs.append({"path": rel, "type": "blob"})

    if not blobs:
        print(f"  No script files found in tree.", flush=True)
        return 0, 0, 0

    print(f"  {len(blobs)} candidate file(s) in tree.", flush=True)

    script_paths = [item["path"] for item in blobs]
    analysis_tree = [{"type": "blob", "path": rel} for rel in all_rel_files]
    project_map, project_summary = _analyse_repo_projects(analysis_tree, script_paths)
    if project_summary:
        print(f"  Project analysis: {len(project_summary)} group(s)", flush=True)
        for row in project_summary[:12]:
            print(
                f"    - {row['label']} [{row['slug']}] — {row['count']} script(s), {row['confidence']} confidence",
                flush=True,
            )
        if len(project_summary) > 12:
            print(f"    ... {len(project_summary) - 12} more group(s)", flush=True)

    part_map = _detect_multipart_clusters(script_paths)
    if part_map:
        n_clusters = len({t for _, t in part_map.values()})
        print(f"  Multipart clusters: {len(part_map)} files across {n_clusters} cluster(s)", flush=True)

    saved = skipped = errors = 0
    skipped_dup_content = 0
    skipped_non_lsl = 0

    _NO_META = {"project_slug": "", "project_label": "", "project_confidence": "low", "project_dir": ""}

    # ── Partition: multipart clusters vs singleton blobs ─────────────────────
    # cluster_groups: (parent_dir, base_name) -> [(part_idx, item)]
    cluster_groups: dict[tuple, list] = defaultdict(list)
    for item in blobs:
        p = item["path"]
        if p in part_map:
            m_ = _PART_SUFFIX_RE.match(Path(p).stem)
            if m_:
                cluster_groups[(Path(p).parent.as_posix(), m_.group(1))].append(
                    (part_map[p][0], item)
                )
    for key in cluster_groups:
        cluster_groups[key].sort(key=lambda x: x[0])
    cluster_paths   = {item["path"] for parts in cluster_groups.values() for _, item in parts}
    singleton_blobs = [b for b in blobs if b["path"] not in cluster_paths]
    total_blobs     = len(blobs)
    blob_idx        = 0

    # ── Process multipart clusters (combine all parts into one document) ──────
    for (parent_dir, base_name), parts in cluster_groups.items():
        if limit and (saved + skipped) >= limit:
            break
        blob_idx   += len(parts)
        part_total  = len(parts)
        _, first_item = parts[0]
        first_path    = first_item["path"]
        meta_info     = project_map.get(first_path, _NO_META)

        # Read every part in order
        part_contents: list[tuple[int, str, str]] = []  # (idx, content, path)
        for part_idx, item in parts:
            try:
                c = (repo_root / Path(item["path"])).read_text(encoding="utf-8", errors="replace")
                part_contents.append((part_idx, c, item["path"]))
            except Exception:
                errors += 1

        if not part_contents:
            continue

        # At least one part must be valid LSL content
        if not any(is_lsl_content(pi_path, c) for _, c, pi_path in part_contents):
            skipped += len(parts)
            skipped_non_lsl += len(parts)
            print(f"  [{blob_idx}/{total_blobs}] skip (non-lsl cluster): {base_name}", flush=True)
            continue

        combined_raw = "\n\n".join(c for _, c, _ in part_contents)
        h = _content_hash(combined_raw)
        if not FORCE and h in existing_hashes:
            skipped += len(parts)
            skipped_dup_content += len(parts)
            print(f"  [{blob_idx}/{total_blobs}] skip (dup cluster): {base_name}", flush=True)
            continue

        # Build combined body: one lsl code block with part separators
        first_desc = extract_description(part_contents[0][1])
        if part_total > 1:
            sections = [
                f"// === Part {pi}/{part_total} ===\n{c.rstrip()}"
                for pi, c, _ in part_contents
            ]
            combined_content = "\n\n".join(sections)
        else:
            combined_content = part_contents[0][1]

        composed = _composed_name(base_name, meta_info.get("project_slug", ""))
        repo_page = f"https://github.com/{owner}/{repo}/blob/{branch}/{urllib.parse.quote(first_path)}"
        save_script(
            composed, repo_page,
            f"{name} / {meta_info.get('project_label', base_name)}",
            lang, combined_content,
            description=first_desc,
            meta={
                "source_owner":      owner,
                "source_repo":       repo,
                "source_branch":     branch,
                "source_path":       first_path,
                "source_project":    meta_info.get("project_label", ""),
                "source_part_total": str(part_total),
            },
        )
        existing_names.add(_norm_name(composed))
        existing_hashes.add(h)
        saved += 1
        label = f"cluster {part_total}pt" if part_total > 1 else "single"
        print(f"  [{blob_idx}/{total_blobs}] saved ({label}): {base_name}", flush=True)

    # ── Process singleton blobs ───────────────────────────────────────────────
    for item in singleton_blobs:
        if limit and (saved + skipped) >= limit:
            break
        blob_idx += 1
        path      = item["path"]
        meta_info = project_map.get(path, _NO_META)
        stem      = Path(path).stem
        composed  = _composed_name(stem, meta_info.get("project_slug", ""))

        try:
            content = (repo_root / Path(path)).read_text(encoding="utf-8", errors="replace")
        except Exception:
            errors += 1
            continue

        doc_kind = classify_doc_kind(path, content)

        if not is_lsl_content(path, content):
            skipped += 1
            skipped_non_lsl += 1
            print(f"  [{blob_idx}/{total_blobs}] skip (non-lsl): {path}", flush=True)
            continue

        h = _content_hash(content)
        if not FORCE and h in existing_hashes:
            skipped += 1
            skipped_dup_content += 1
            print(f"  [{blob_idx}/{total_blobs}] skip (dup content): {path}", flush=True)
            continue

        repo_page = f"https://github.com/{owner}/{repo}/blob/{branch}/{urllib.parse.quote(path)}"
        save_script(
            composed, repo_page,
            f"{name} / {meta_info.get('project_label', stem)}",
            lang, content,
            doc_kind=doc_kind,
            meta={
                "source_owner":              owner,
                "source_repo":               repo,
                "source_branch":             branch,
                "source_path":               path,
                "source_doc_kind":           doc_kind,
                "source_project":            meta_info.get("project_label", ""),
                "source_project_dir":        meta_info.get("project_dir", ""),
                "source_project_confidence": meta_info.get("project_confidence", ""),
            },
        )
        existing_names.add(_norm_name(composed))
        existing_hashes.add(h)
        saved += 1
        print(f"  [{blob_idx}/{total_blobs}] saved: {path}", flush=True)

    print(
        f"  Skip breakdown: dup-content={skipped_dup_content}, non-lsl={skipped_non_lsl}",
        flush=True,
    )

    return saved, skipped, errors


# ── Web source ────────────────────────────────────────────────────────────────

def _crawl_web_dir(base_url: str, current_url: str,
                   visited: set, script_links: list, depth: int = 0):
    """
    Recursively crawl a web directory listing.
    Collects script file links and follows subdirectory links.
    Stays within base_url to avoid leaving the library.
    """
    if current_url in visited or depth > 8:
        return
    visited.add(current_url)

    html = fetch(current_url)
    if not html:
        return

    for m in re.finditer(r'<a[^>]+href=["\']([^"\'?#]+)["\'][^>]*>', html, re.IGNORECASE):
        href = m.group(1).strip()
        # Skip parent directory navigation and absolute external links
        if href in ("..", "../", "/") or href.startswith("?") or href.startswith("#"):
            continue
        full = urllib.parse.urljoin(current_url, href)
        # Stay within the base library URL
        if not full.startswith(base_url):
            continue
        if full in visited:
            continue

        path_part = urllib.parse.urlparse(full).path
        ext = Path(path_part).suffix.lower()

        if ext in LSL_EXTS | {".txt"}:
            stem = Path(path_part).stem
            if full not in {u for _, u in script_links}:
                script_links.append((stem, full))
        elif not ext or href.endswith("/"):
            # Likely a subdirectory — recurse
            time.sleep(0.2)
            _crawl_web_dir(base_url, full, visited, script_links, depth + 1)


def fetch_web(source: dict, existing_names: set, existing_hashes: set,
              limit: int | None) -> tuple[int, int, int]:
    url  = source["url"]
    name = source["name"]
    lang = source.get("lang", "LSL")

    print(f"\n[Web] {url}", flush=True)

    visited      = set()
    script_links = []
    _crawl_web_dir(url, url, visited, script_links)
    links = script_links
    print(f"  {len(links)} script link(s) found across {len(visited)} page(s).", flush=True)

    saved = skipped = errors = 0

    for stem, script_url in links:
        if limit and (saved + skipped) >= limit:
            break

        time.sleep(RATE_DELAY)
        content = fetch(script_url)
        if not content:
            errors += 1
            continue

        if not is_lsl_content(script_url, content):
            skipped += 1
            print(f"  skip (non-lsl): {stem}", flush=True)
            continue

        h = _content_hash(content)
        if not FORCE and h in existing_hashes:
            skipped += 1
            print(f"  skip (dup content): {stem}", flush=True)
            continue

        doc_kind = classify_doc_kind(script_url, content)
        save_script(
            stem,
            script_url,
            name,
            lang,
            content,
            doc_kind=doc_kind,
            meta={"source_doc_kind": doc_kind},
        )
        existing_names.add(_norm_name(stem))
        existing_hashes.add(h)
        saved += 1
        print(f"  saved: {stem}", flush=True)

    return saved, skipped, errors


# ── Wiki source (MediaWiki script library pages) ──────────────────────────────

def _extract_wiki_page_links(base: str, html: str, seen: set) -> list[tuple[str, str]]:
    """Extract internal wiki links from a page, skipping meta/category pages."""
    _SKIP = ("Category:", "User:", "Talk:", "Special:", "Help:", "File:", "Template:")
    links = []
    for m in re.finditer(r'<a[^>]+href="(/wiki/([^"#]+))"[^>]*>([^<]*)</a>', html):
        href, slug, anchor = m.group(1), urllib.parse.unquote(m.group(2)), m.group(3).strip()
        if any(slug.startswith(p) for p in _SKIP):
            continue
        full = base + href
        if full not in seen:
            seen.add(full)
            title = anchor or slug.replace("_", " ")
            links.append((title, full))
    return links


def _extract_code_blocks(html: str) -> str:
    """Pull LSL code blocks out of wiki HTML as plain text."""
    blocks = []
    for m in re.finditer(
        r'<div[^>]*class="[^"]*mw-highlight[^"]*"[^>]*>\s*<pre[^>]*>(.*?)</pre>\s*</div>',
        html, re.DOTALL
    ):
        code = re.sub(r"<[^>]+>", "", m.group(1))
        code = code.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")
        blocks.append(code.strip())
    if not blocks:
        for m in re.finditer(r"<pre[^>]*>(.*?)</pre>", html, re.DOTALL):
            code = re.sub(r"<[^>]+>", "", m.group(1))
            code = code.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")
            blocks.append(code.strip())
    return "\n\n".join(blocks)


def fetch_wiki(source: dict, existing_names: set, existing_hashes: set,
               limit: int | None) -> tuple[int, int, int]:
    index_url = source["url"]
    base      = source.get("base", "")
    name      = source["name"]
    lang      = source.get("lang", "LSL")

    print(f"\n[Wiki] {index_url}", flush=True)

    index_html = fetch(index_url)
    if not index_html:
        print(f"  Could not fetch index — skipping.", flush=True)
        return 0, 0, 1

    seen  = {index_url}
    pages = _extract_wiki_page_links(base, index_html, seen)
    print(f"  {len(pages)} page link(s) found on index.", flush=True)

    saved = skipped = errors = 0

    for title, page_url in pages:
        if limit and (saved + skipped) >= limit:
            break

        time.sleep(RATE_DELAY)
        html = fetch(page_url)
        if not html:
            errors += 1
            continue

        code = _extract_code_blocks(html)
        if not code or not LSL_KEYWORDS_RE.search(code):
            skipped += 1
            print(f"  skip (non-lsl): {title}", flush=True)
            continue

        h = _content_hash(code)
        if not FORCE and h in existing_hashes:
            skipped += 1
            print(f"  skip (dup content): {title}", flush=True)
            continue

        desc_m = re.search(r'<p[^>]*>(.*?)</p>', html, re.DOTALL)
        desc   = re.sub(r"<[^>]+>", "", desc_m.group(1)).strip()[:300] if desc_m else ""

        doc_kind = classify_doc_kind(title, code)
        stem    = re.sub(r'[<>:"/\\|?*]', '', title).replace(" ", "_")[:100]
        safe    = stem
        path    = _next_available_path(safe)
        front   = (
            f'---\nname: {_json_str(safe)}\ncategory: "examples"\ntype: "example"\n'
            f'language: {_json_str(lang)}\ndescription: {_json_str(desc)}\n'
            f'source_url: {_json_str(page_url)}\nsource_name: {_json_str(name)}\n'
            f'source_doc_kind: {_json_str(doc_kind)}\n'
            f'first_fetched: {_json_str(TODAY)}\nlast_updated: {_json_str(TODAY)}\n---\n\n'
        )
        path.write_text(front + script_to_markdown(safe, code, doc_kind=doc_kind), encoding="utf-8")
        existing_names.add(_norm_name(safe))
        existing_hashes.add(h)
        saved += 1
        print(f"  saved: {title}", flush=True)

    return saved, skipped, errors


# ── Manifest ──────────────────────────────────────────────────────────────────

def update_manifest(total_saved: int):
    manifest = {}
    if MANIFEST.exists():
        try:
            manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        except Exception:
            pass
    sources = manifest.setdefault("extra_library_sources", {})
    for s in SOURCES:
        if SOURCE_ID and s["id"] != SOURCE_ID:
            continue
        sources[s["id"]] = TODAY
    manifest["last_updated"] = TODAY
    MANIFEST.write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def append_changelog(totals: dict):
    lines = [f"\n## {TODAY} — Extra library fetch\n"]
    for src_id, (sv, sk, er) in totals.items():
        lines.append(f"- [{src_id}] saved: {sv}, skipped: {sk}, errors: {er}\n")
    entry = "".join(lines)
    try:
        existing = CHANGELOG.read_text(encoding="utf-8") if CHANGELOG.exists() else ""
        CHANGELOG.write_text(existing + entry, encoding="utf-8")
    except Exception:
        pass


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print(f"fetch-extra-libraries v0.2.3.0 — {TODAY}", flush=True)
    print(f"Output: {OUT_DIR}", flush=True)
    if SOURCE_ID:
        print(f"Source filter: {SOURCE_ID}", flush=True)
    print(flush=True)

    existing_names, existing_hashes = _build_existing_index()
    print(f"Existing examples: {len(existing_names)} (used for deduplication)\n", flush=True)

    totals: dict[str, tuple[int, int, int]] = {}
    grand_saved = 0

    # Determine which source IDs will actually run this pass.
    _active_ids = {s["id"] for s in SOURCES if not SOURCE_ID or s["id"] == SOURCE_ID}

    for source in SOURCES:
        if SOURCE_ID and source["id"] != SOURCE_ID:
            continue

        # outworldz-web is a slow HTML crawl of the same repo that outworldz-github
        # fetches via the GitHub tree API.  Skip the web crawl whenever the GitHub
        # path is also being run — it would only add network cost and duplicates.
        if source["id"] == "outworldz-web" and "outworldz-github" in _active_ids:
            print(f"[skip] outworldz-web — outworldz-github covers the same content", flush=True)
            continue

        if source["type"] == "github":
            sv, sk, er = fetch_github(source, existing_names, existing_hashes, LIMIT)
        elif source["type"] == "wiki":
            sv, sk, er = fetch_wiki(source, existing_names, existing_hashes, LIMIT)
        else:
            sv, sk, er = fetch_web(source, existing_names, existing_hashes, LIMIT)

        totals[source["id"]] = (sv, sk, er)
        grand_saved += sv
        print(f"  → {source['id']}: saved {sv}, skipped {sk}, errors {er}\n", flush=True)

    print("=" * 50, flush=True)
    print(f"Total saved: {grand_saved}", flush=True)

    if grand_saved > 0:
        update_manifest(grand_saved)
        append_changelog(totals)
        print("Manifest and changelog updated.", flush=True)


if __name__ == "__main__":
    main()
