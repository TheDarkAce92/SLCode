#!/usr/bin/env python3
# Skill: analyse-repo-naming
# Version: 0.1.0
# Purpose: Pull all GitHub repos used by fetch-extra-libraries and analyse naming/structure trends
# Usage: python3 analyse-repo-naming.py [--repo=ID] [--no-download] [--cache-dir=PATH]
#
# Outputs a plain-text report to stdout.  Re-use a previously downloaded snapshot
# with --no-download --cache-dir=/path/to/existing/snapshots.

import io
import json
import os
import re
import ssl
import sys
import tempfile
import urllib.request
import zipfile
from collections import Counter, defaultdict
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# ── Config ────────────────────────────────────────────────────────────────────

GITHUB_REPOS = [
    {"id": "absolutelycraicrai", "owner": "AbsolutelyCraiCrai", "repo": "lsl-scripts-lib"},
    {"id": "outworldz-github",   "owner": "Outworldz",          "repo": "LSL-Scripts"},
    {"id": "avacon-opensim",     "owner": "AvaCon",              "repo": "LSL-OpenSim-Script-Library"},
]

LSL_EXTS = {".lsl", ".sl", ".lslp", ".lslm"}
ALL_CODE_EXTS = LSL_EXTS | {".txt"}

PROJECT_MARKERS = {
    "readme.md", "readme.txt", "project.json", "package.json", ".gitmodules",
    "requirements.txt", "pyproject.toml", ".sln",
}

# ── CLI args ──────────────────────────────────────────────────────────────────

REPO_ID_FILTER = None
NO_DOWNLOAD    = "--no-download" in sys.argv
CACHE_DIR      = None

for a in sys.argv[1:]:
    if a.startswith("--repo="):
        REPO_ID_FILTER = a.split("=", 1)[1]
    elif a.startswith("--cache-dir="):
        CACHE_DIR = Path(a.split("=", 1)[1])

# ── HTTP helpers ──────────────────────────────────────────────────────────────

GH_HEADERS = {
    "Accept":     "application/vnd.github+json",
    "User-Agent": "SLCode/1.0 LSL-cache-builder",
}

_SSL_CTX = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
_SSL_CTX.check_hostname = False
_SSL_CTX.verify_mode    = ssl.CERT_NONE


def _fetch_json(url: str) -> dict | list | None:
    req = urllib.request.Request(url, headers=GH_HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=20, context=_SSL_CTX) as r:
            return json.loads(r.read().decode("utf-8", errors="replace"))
    except Exception as e:
        print(f"  [fetch_json error] {url}: {e}", flush=True)
        return None


def _fetch_bytes(url: str, timeout: int = 120) -> bytes:
    req = urllib.request.Request(url, headers=GH_HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=_SSL_CTX) as r:
            return r.read()
    except Exception as e:
        print(f"  [fetch_bytes error] {url}: {e}", flush=True)
        return b""


def _default_branch(owner: str, repo: str) -> str:
    data = _fetch_json(f"https://api.github.com/repos/{owner}/{repo}")
    if isinstance(data, dict):
        return data.get("default_branch", "main")
    return "main"


def _pull_snapshot(owner: str, repo: str, branch: str, dest_parent: Path) -> Path | None:
    """Download zipball and extract.  Returns repo root dir inside dest_parent."""
    dest_parent.mkdir(parents=True, exist_ok=True)
    zip_path = dest_parent / "repo.zip"

    if NO_DOWNLOAD and zip_path.exists():
        print(f"  Re-using existing zip: {zip_path}", flush=True)
    else:
        url = f"https://codeload.github.com/{owner}/{repo}/zip/refs/heads/{branch}"
        print(f"  Downloading {url} ...", flush=True)
        blob = _fetch_bytes(url)
        if not blob:
            return None
        zip_path.write_bytes(blob)

    try:
        with zipfile.ZipFile(zip_path) as zf:
            zf.extractall(dest_parent)
    except Exception as e:
        print(f"  Zip extract error: {e}", flush=True)
        return None

    roots = [p for p in dest_parent.iterdir() if p.is_dir()]
    if not roots:
        return None
    return roots[0]


# ── Naming classifiers ────────────────────────────────────────────────────────

_WORD_RE = re.compile(r"[A-Za-z]+")

def _classify_name(name: str) -> str:
    """Classify stem naming convention."""
    # Strip common non-alpha separators for checks
    if " " in name:
        return "space-separated"
    if re.match(r"^[A-Z][A-Z0-9_]+$", name) and "_" in name:
        return "SCREAMING_SNAKE"
    if re.match(r"^[a-z][a-z0-9]+(_[a-z0-9]+)+$", name):
        return "snake_case"
    if re.match(r"^[a-z][a-z0-9]+(-[a-z0-9]+)+$", name):
        return "kebab-case"
    if re.match(r"^[A-Z][a-zA-Z0-9]*([A-Z][a-zA-Z0-9]*)+$", name):
        return "PascalCase"
    if re.match(r"^[a-z][a-z0-9]*([A-Z][a-zA-Z0-9]*)+$", name):
        return "camelCase"
    if re.match(r"^[A-Z][a-zA-Z0-9]+$", name):
        return "TitleCase-single"
    if re.match(r"^[a-z][a-z0-9]+$", name):
        return "lowercase-single"
    if re.match(r"^[A-Z][A-Za-z0-9\-_.]+$", name):
        return "Mixed-upper-start"
    if re.match(r"^[0-9]", name):
        return "numeric-start"
    return "other"


def _tokenize_stem(stem: str) -> list[str]:
    """Split a filename stem into tokens."""
    # normalise separators
    s = re.sub(r"[-_\s.]", "_", stem)
    # split on transitions: camelCase / PascalCase
    s = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s)
    s = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", s)
    return [t.lower() for t in s.split("_") if len(t) >= 2]


def _depth(path_str: str) -> int:
    return len(Path(path_str).parts) - 1  # depth of containing folder (0 = root)


# ── Per-repo analysis ─────────────────────────────────────────────────────────

def analyse_repo(repo_root: Path, repo_id: str) -> dict:
    """
    Walk repo root and collect statistics.
    Returns an analysis dict.
    """
    all_files: list[str] = []
    lsl_files: list[str] = []
    marker_dirs: set[str] = set()

    for p in repo_root.rglob("*"):
        if not p.is_file():
            continue
        rel = p.relative_to(repo_root).as_posix()
        all_files.append(rel)
        name_lower = p.name.lower()
        if name_lower in PROJECT_MARKERS:
            d = p.parent.relative_to(repo_root).as_posix()
            marker_dirs.add("" if d == "." else d)
        if p.suffix.lower() in LSL_EXTS:
            lsl_files.append(rel)

    total_lsl  = len(lsl_files)
    total_files = len(all_files)

    # -- Depth distribution
    depth_counter = Counter(_depth(p) for p in lsl_files)

    # -- Top-level folder distribution
    top_folders: dict[str, list[str]] = defaultdict(list)
    for p in lsl_files:
        parts = Path(p).parts
        top = parts[0] if len(parts) > 1 else "(root)"
        top_folders[top].append(p)

    # -- Naming scheme distribution
    scheme_counter = Counter(_classify_name(Path(p).stem) for p in lsl_files)

    # -- Token frequency (across all stems)
    token_counter: Counter = Counter()
    for p in lsl_files:
        token_counter.update(_tokenize_stem(Path(p).stem))

    # -- Extension distribution (across all .lsl-region files)
    ext_counter = Counter(Path(p).suffix.lower() for p in lsl_files)

    # -- Marker dir coverage
    # For each lsl file, is it under a dir that has a project marker?
    def _has_marker_ancestor(rel_path: str) -> bool:
        parts = Path(rel_path).parts[:-1]
        for i in range(len(parts), -1, -1):
            ancestor = "/".join(parts[:i])
            if ancestor in marker_dirs or ancestor == "":
                return ancestor in marker_dirs
        return False

    marker_coverage = sum(1 for p in lsl_files if _has_marker_ancestor(p))

    # -- Naming scheme per top-level folder
    folder_schemes: dict[str, Counter] = {}
    for folder, paths in top_folders.items():
        folder_schemes[folder] = Counter(_classify_name(Path(p).stem) for p in paths)

    # -- Paths of marker dirs
    marker_dirs_list = sorted(marker_dirs)

    # -- Sample files (up to 10) per top-level folder
    folder_samples: dict[str, list[str]] = {
        f: paths[:10] for f, paths in sorted(top_folders.items(), key=lambda x: -len(x[1]))
    }

    # -- Detect repeated folder name pattern (fragmentation signal)
    #    e.g.  Foo/Foo/script.lsl  or  Foo/FooExtra/script.lsl
    repeated_fragment_count = 0
    for p in lsl_files:
        parts = [x.lower() for x in Path(p).parts[:-1]]
        if len(parts) >= 2 and parts[0] in parts[1]:
            repeated_fragment_count += 1

    # -- Detect version-like suffixes in TOP-LEVEL DIRECTORY names
    #    e.g.  Door_Script_2/  ElevatorKeyFramed-v1.0/  Cyberflight_1_1/
    #    These are versioned PROJECTS (different from file-level multipart patterns).
    def _has_version_suffix(s: str) -> bool:
        return bool(re.search(r"[-_. ]v?\d[\d.]*$", s, re.IGNORECASE))

    version_suffix_dirs = {
        Path(p).parts[0]
        for p in lsl_files
        if len(Path(p).parts) > 1 and _has_version_suffix(Path(p).parts[0])
    }

    # -- Detect MULTIPART FILE CLUSTERS
    #    In SL/LSL a single logical script is sometimes split across multiple
    #    numbered files due to per-script memory limits, e.g.:
    #        SL_Sculpt_to_PHP_script_1.lsl  ..  SL_Sculpt_to_PHP_script_21.lsl
    #        Go_Game_1.lsl  ..  Go_Game_11.lsl
    #    Distinguishing feature: the number is on the FILE stem (not the folder),
    #    the files share an identical base prefix, and the numbers are sequential
    #    starting at 1 (or 0).
    _PART_SUFFIX_RE = re.compile(r"^(.+?)[-_ ](\d+)$")
    _part_grouped: dict[tuple, list] = defaultdict(list)
    for p in lsl_files:
        stem   = Path(p).stem
        parent = Path(p).parent.as_posix()
        m = _PART_SUFFIX_RE.match(stem)
        if m:
            base = m.group(1)
            num  = int(m.group(2))
            _part_grouped[(parent, base)].append((num, p))

    multipart_clusters: dict[str, list[str]] = {}
    for (parent_dir, base), items in _part_grouped.items():
        if len(items) < 2:
            continue
        nums = sorted(x[0] for x in items)
        # Require sequential starting at 0 or 1
        if nums[0] <= 1 and nums[-1] == nums[0] + len(nums) - 1:
            key = f"{parent_dir}/{base}" if parent_dir not in ("", ".") else base
            multipart_clusters[key] = [path for _, path in sorted(items)]

    # Files that are confirmed parts of a multipart cluster
    multipart_files: set[str] = set()
    for paths in multipart_clusters.values():
        multipart_files.update(paths)

    return {
        "repo_id":            repo_id,
        "total_files":        total_files,
        "total_lsl":          total_lsl,
        "ext_counter":        dict(ext_counter.most_common()),
        "depth_counter":      {str(k): v for k, v in sorted(depth_counter.items())},
        "top_folders":        {f: len(paths) for f, paths in top_folders.items()},
        "scheme_counter":     dict(scheme_counter.most_common()),
        "token_counter_top":  dict(token_counter.most_common(50)),
        "marker_dirs":        marker_dirs_list,
        "marker_coverage":    marker_coverage,
        "folder_schemes":     {f: dict(c.most_common()) for f, c in folder_schemes.items()},
        "folder_samples":     folder_samples,
        "repeated_fragments":  repeated_fragment_count,
        "version_suffix_dirs":  sorted(version_suffix_dirs),
        "multipart_clusters":   multipart_clusters,   # key -> ordered list of paths
        "multipart_file_count": len(multipart_files),
    }


# ── Report printer ────────────────────────────────────────────────────────────

def _bar(count: int, total: int, width: int = 30) -> str:
    if not total:
        return " " * width
    filled = round(count / total * width)
    return "█" * filled + "░" * (width - filled)


def print_report(analyses: list[dict]):
    sep = "=" * 72

    for a in analyses:
        rid       = a["repo_id"]
        n_lsl     = a["total_lsl"]
        n_files   = a["total_files"]
        scheme_c  = a["scheme_counter"]
        depth_c   = a["depth_counter"]
        top_f     = a["top_folders"]
        tokens    = a["token_counter_top"]
        markers   = a["marker_dirs"]
        coverage  = a["marker_coverage"]
        f_schemes = a["folder_schemes"]
        f_samples = a["folder_samples"]
        rep_frags = a["repeated_fragments"]
        ver_dirs  = a["version_suffix_dirs"]

        print(sep)
        print(f"  REPO: {rid}")
        print(sep)
        print(f"  Total files in tree : {n_files}")
        print(f"  LSL scripts found   : {n_lsl}")
        print(f"  Ext breakdown       : {a['ext_counter']}")
        print()

        # -- Depth distribution
        print("  FILE DEPTH DISTRIBUTION  (0 = root, 1 = inside one folder, ...)")
        max_d = max(int(k) for k in depth_c) if depth_c else 0
        for d in range(max_d + 1):
            cnt = depth_c.get(str(d), 0)
            pct = cnt / n_lsl * 100 if n_lsl else 0
            print(f"    depth {d}:  {cnt:>5}  {_bar(cnt, n_lsl)}  {pct:.1f}%")
        print()

        # -- Naming schemes
        print("  NAMING SCHEME DISTRIBUTION")
        for scheme, cnt in scheme_c.items():
            pct = cnt / n_lsl * 100 if n_lsl else 0
            print(f"    {scheme:<25}  {cnt:>5}  {_bar(cnt, n_lsl, 24)}  {pct:.1f}%")
        print()

        # -- Top-level folder breakdown
        print("  TOP-LEVEL FOLDERS  (by LSL script count)")
        sorted_folders = sorted(top_f.items(), key=lambda x: -x[1])
        for folder, cnt in sorted_folders[:40]:
            print(f"    {cnt:>5}  {folder}")
        if len(sorted_folders) > 40:
            print(f"    ... {len(sorted_folders) - 40} more folders ...")
        print()

        # -- Project marker dirs
        if markers:
            print(f"  PROJECT MARKER DIRS  ({len(markers)} found)")
            for m in markers[:30]:
                print(f"    {m!r}")
            if len(markers) > 30:
                print(f"    ... {len(markers) - 30} more ...")
            print(f"  LSL files under a marker dir: {coverage}/{n_lsl}  ({coverage/n_lsl*100:.1f}% if n_lsl else 'N/A')")
        else:
            print("  PROJECT MARKER DIRS  (none found)")
        print()

        # -- Fragmentation / structural signals
        if rep_frags:
            print(f"  REPEATED-FOLDER FRAGMENTS (Foo/Foo/... pattern): {rep_frags} files")

        # Versioned project DIRECTORIES — whole project re-uploaded under a new name
        if ver_dirs:
            print(f"  VERSIONED PROJECT DIRS ({len(ver_dirs)})  ← top-level folder has version in name")
            print(f"  (These are distinct projects/versions, NOT multipart files)")
            for vd in sorted(ver_dirs)[:30]:
                print(f"    {vd}")
            if len(ver_dirs) > 30:
                print(f"    ... {len(ver_dirs) - 30} more ...")

        # Multipart file clusters — same logical script split across numbered files
        mp_clusters = a.get("multipart_clusters", {})
        mp_count    = a.get("multipart_file_count", 0)
        if mp_clusters:
            print(f"\n  MULTIPART FILE CLUSTERS ({len(mp_clusters)} clusters, {mp_count} files)")
            print(f"  (Same logical LSL script split across numbered prim slots — keep all parts)")
            # Show up to 20 clusters with their part count and sample files
            sorted_clusters = sorted(mp_clusters.items(), key=lambda x: -len(x[1]))
            for key, paths in sorted_clusters[:20]:
                n_parts = len(paths)
                nums    = []
                _PART_RE = re.compile(r"[-_ ](\d+)$")
                for p in paths:
                    m = _PART_RE.search(Path(p).stem)
                    if m: nums.append(int(m.group(1)))
                nums_str = f"parts {min(nums)}–{max(nums)}" if nums else f"{n_parts} parts"
                print(f"    {n_parts:>3} parts  [{nums_str}]  {key}")
                for p in paths[:3]:
                    print(f"               {Path(p).name}")
                if n_parts > 3:
                    print(f"               ... {n_parts-3} more")
            if len(sorted_clusters) > 20:
                print(f"    ... {len(sorted_clusters)-20} more clusters ...")
            # Proportion of all LSL files that are multipart
            pct_mp = mp_count / n_lsl * 100 if n_lsl else 0
            print(f"\n  {mp_count}/{n_lsl} ({pct_mp:.1f}%) of LSL files are part of a multipart cluster")

        if rep_frags or ver_dirs or mp_clusters:
            print()

        # -- Top token frequency
        print("  TOP-50 STEM TOKENS")
        tok_pairs = list(tokens.items())
        for i in range(0, len(tok_pairs), 5):
            row = tok_pairs[i:i+5]
            print("    " + "   ".join(f"{t}({c})" for t, c in row))
        print()

        # -- Per-folder naming breakdown and samples
        print("  PER-FOLDER NAMING SCHEME  (top 20 folders by count)")
        for folder, cnt in sorted_folders[:20]:
            schemes_here = f_schemes.get(folder, {})
            dominant = max(schemes_here, key=schemes_here.get) if schemes_here else "?"
            print(f"    {cnt:>4}  {folder:<40}  dominant: {dominant}")
            # print a few sample file paths
            samples = f_samples.get(folder, [])[:5]
            for s in samples:
                print(f"           {Path(s).name}")
        print()

    print(sep)
    print()

    # -- Cross-repo summary
    print("  CROSS-REPO SUMMARY")
    print()
    all_schemes: Counter = Counter()
    for a in analyses:
        all_schemes.update(a["scheme_counter"])
    total_all = sum(all_schemes.values())
    print("  Combined naming scheme distribution:")
    for scheme, cnt in all_schemes.most_common():
        pct = cnt / total_all * 100 if total_all else 0
        print(f"    {scheme:<25}  {cnt:>5}  {pct:.1f}%")
    print()

    # -- Cross-repo token overlap
    all_tokens: Counter = Counter()
    for a in analyses:
        all_tokens.update(a["token_counter_top"])
    print("  Most common cross-repo tokens (top 40):")
    tok_pairs = all_tokens.most_common(40)
    for i in range(0, len(tok_pairs), 5):
        row = tok_pairs[i:i+5]
        print("    " + "   ".join(f"{t}({c})" for t, c in row))
    print()
    print(sep)


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    repos = [r for r in GITHUB_REPOS if not REPO_ID_FILTER or r["id"] == REPO_ID_FILTER]
    if not repos:
        print(f"  No repos match filter: {REPO_ID_FILTER}", flush=True)
        sys.exit(1)

    snap_base = CACHE_DIR or Path(tempfile.mkdtemp(prefix="slcode-name-analysis-"))
    print(f"Snapshot directory: {snap_base}", flush=True)
    print(flush=True)

    analyses = []

    for r in repos:
        rid, owner, repo_name = r["id"], r["owner"], r["repo"]
        dest = snap_base / rid
        print(f"[{rid}]  {owner}/{repo_name}", flush=True)

        repo_root_in_cache = dest / (repo_name + "-main")
        if NO_DOWNLOAD and any(dest.glob("*/")) and any(dest.rglob("*.lsl")):
            # Find existing root
            roots = [p for p in dest.iterdir() if p.is_dir() and p.name != "repo.zip"]
            repo_root = roots[0] if roots else None
        else:
            branch = _default_branch(owner, repo_name)
            print(f"  Default branch: {branch}", flush=True)
            repo_root = _pull_snapshot(owner, repo_name, branch, dest)

        if not repo_root:
            print(f"  ERROR: could not get repo root for {rid}", flush=True)
            continue

        print(f"  Extracted to: {repo_root}", flush=True)
        print(f"  Analysing ...", flush=True)
        a = analyse_repo(repo_root, rid)
        analyses.append(a)
        print(f"  Done — {a['total_lsl']} LSL files, {len(a['top_folders'])} top-level folders", flush=True)
        print(flush=True)

    if not analyses:
        print("No analyses produced.", flush=True)
        sys.exit(1)

    print()
    print_report(analyses)

    print(f"\nSnapshot dir preserved at: {snap_base}", flush=True)
    print("Re-run with: --no-download --cache-dir=" + str(snap_base), flush=True)


if __name__ == "__main__":
    main()
