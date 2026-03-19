# Architecture

## Overview

SLCode is a Python application with two faces:

- **Interactive UI** — local HTTP server + pywebview (embedded WebView2) or system browser
- **CLI** — subcommands for search, docs, check, analyse, format, flatten, cache management, and project filesystem

All application logic lives in `search-cache.py` (a single intentionally self-contained file).
The web UI (HTML/CSS/JS) is embedded inline as a string — no separate asset files.

---

## Stub launcher architecture

The app is distributed as two small C executables that wrap the Python bundle:

| Stub | Subsystem | Entry point | Purpose |
|---|---|---|---|
| `SLCode.exe` | WINDOWS (`-mwindows`) | `wWinMain` | GUI launch — no console, shows splash window |
| `slcode-cli.exe` | CONSOLE (`-DCONSOLE_MODE`) | `wmain` | CLI launch — inherits terminal, shows spinner |

Both are compiled from the same `slcode-stub.c` source via MinGW gcc.
Icon is embedded in both via a `.rc` resource file compiled with windres.

### Launch modes (inside the stub)

| Mode | Trigger | Behaviour |
|---|---|---|
| `MODE_GUI` | `SLCode.exe` | Splash window → extract if needed → launch Python → wait for ready event |
| `MODE_CLI_CMD` | `slcode-cli <command>` | No splash → extract if needed → launch Python → wait for exit, propagate code |
| `MODE_CLI_GUI` | `slcode-cli` (no args / serve) | Delegates to `SLCode.exe` next to itself, prints detach message, exits |

### Extraction and version checking

On each GUI or CLI launch the stub checks whether the Python bundle needs extracting:

1. If `%LOCALAPPDATA%\SLCode\SLCode-app\version.txt` is missing → fresh install, extract
2. If `version.txt` content differs from the compiled-in `APP_VERSION` → update, re-extract
3. Otherwise → skip extraction, start Python directly

`version.txt` is written into the bundle at build time by `build.py` and extracted as part of the zip.
Deleting `version.txt` or running with `-extract` forces re-extraction on next launch.

The splash shows "Installing…", "Updating…", or "Loading…" accordingly.

### Splash window / named event IPC

The GUI stub creates a Win32 splash window before launching Python. It stays visible until:

- Python signals a named Windows event (`SLCodeReady_<stub-pid>`) when the UI is ready, **or**
- 30-second timeout

Python opens the event using the `SLCODE_STUB_PID` environment variable (set by the stub before launching the child). The signal is sent in `_signal_splash_ready()` in `search-cache.py`:

- **pywebview mode** — called via `webview.start(func=_signal_splash_ready)`
- **browser mode** — called after `webbrowser.open(url)`
- **no-open mode** — called after the server thread starts

---

## search-cache.py structure

Key sections (roughly in order):

1. Imports and path constants (`CACHE_ROOT`, `DOCS_DIR`, category dirs)
2. INDEX loading — reads YAML front matter from all `.md` files on startup
3. Cache tools registry — `CACHE_TOOLS` list: `{id, name, description, cmd, options, note, web}`
4. `_skill_cmd(name)` — resolves skill script path for subprocess invocation
5. `run_skill_cmd()` — invokes a skill, streams output to stdout
6. LSL checker — `run_checks()`, `run_sanity_checks()`, lslint wrapper
7. Analyser — memory estimator, channel map, sleep profiler
8. Formatter — `format_lsl()`
9. HTTP server — `BaseHTTPRequestHandler` subclass; all routes under `/api/`
10. CLI — `argparse` subcommands dispatched in `main()`
11. `initialize_runtime()` — startup: build index, start file watchers
12. `serve_ui()` — start HTTP server + pywebview or browser; signal splash when ready
13. `main()` — entry point; sets `_QUIET_MODE` for non-serve commands
14. `HTML_CONTENT` — the entire web UI as an inline string

### Startup log suppression

For non-`serve` CLI commands (check, search, lookup, etc.), `_QUIET_MODE = True` is set before
`initialize_runtime()` to suppress startup logs that would pollute CLI output. It is reset to
`False` (or kept `True` for `--json` mode) after init.

---

## Cache tools / skills

Skills live in `LSL Cache/skills/` as standalone Python scripts. They are launched as subprocesses
by `run_skill_cmd()`, with the `LSL_CACHE_BASE` environment variable set to the cache root path.

Each skill:
- Has a standard header comment (`# Skill:`, `# Version:`, `# Purpose:`, `# Usage:`)
- Reads `LSL_CACHE_BASE` to locate cache files
- Streams progress to stdout (shown live in the Tools panel)
- Updates `cache-manifest.json` and `lsl-docs/CHANGELOG.md` on completion

### OSSL fetch fallback chain

`fetch-ossl-docs.py` tries three sources in order:
1. opensimulator.org wiki (often unreachable)
2. `fetch-ossl-from-github.py` — parses `IOSSL_Api.cs` + `OSSL_Api.cs` from opensim/opensim GitHub (signatures + `//ApiDesc` descriptions + threat levels)
3. `generate-ossl-from-kwdb.py` — local only, uses cached `kwdb.xml` + `makopo/tooltipdata.json`

---

## HTTP API

The UI communicates with the local server via fetch calls to `/api/*` endpoints.

Major groups:

| Prefix | Purpose |
|---|---|
| `/api/search` `/api/doc` `/api/lookup` | Documentation queries |
| `/api/check` `/api/analyze` `/api/debug` | Script analysis |
| `/api/format` `/api/flatten` | Code transformation |
| `/api/cache/*` | Cache status, tool listing, tool run, poll |
| `/api/fs/*` | Project-scoped filesystem operations |
| `/api/external/*` | Firestorm external editor sync |
| `/api/github/*` | GitHub PAT save/clear/status |
| `/api/reload` | Rebuild in-memory index |
| `/api/status` | Cache and index summary |

---

## Build pipeline

`build.py` performs these steps:

1. Copies `search-cache.py` → `build/_slcode_runtime.py` and `build/slcode_runtime.py`
2. Runs PyInstaller on `slcode-launcher.py` (onedir mode)
3. Generates a version string (`YYYYMMDD-<git-hash>` or `YYYYMMDD-local`)
4. Writes `version.txt` into `dist/SLCode-app/` with the version string
5. Zips `dist/SLCode-app/` → `dist/SLCode-app.zip`
6. Compiles `slcode-res.rc` → `build/slcode-res.o` via windres (icon)
7. Compiles `slcode-stub.c` → `dist/SLCode.exe` with `-DAPP_VERSION="..."` `-mwindows`
8. Compiles `slcode-stub.c` → `dist/slcode-cli.exe` with `-DAPP_VERSION="..."` `-DCONSOLE_MODE`

**Runtime paths:**

| Context | Cache location |
|---|---|
| Installed (`dist/`) | `%LOCALAPPDATA%\SLCode\LSL Cache\` |
| Dev (from source) | `./LSL Cache/` (repo root) |

`search-cache.py` detects which path exists at startup.
