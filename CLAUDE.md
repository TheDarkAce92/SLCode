# CLAUDE.md — SLCode Application Repository

## What this repo is

**SLCode** is a standalone Windows desktop app for Second Life / OpenSimulator LSL scripting:
an LSL documentation browser, Monaco-based IDE, syntax checker, and cache management tool.

This is the **application source repo** — not an LSL scripting project. The instructions here
are for maintaining and extending the app itself.

---

## Key files

| File | Purpose |
|---|---|
| `search-cache.py` | The entire application: Python HTTP server, web UI (HTML/CSS/JS inline), CLI, cache tools |
| `slcode-launcher.py` | PyInstaller entry point — thin wrapper that calls `main()` from search-cache.py |
| `slcode-stub.c` | C stub launcher — compiles to `SLCode.exe` (GUI) and `slcode-cli.exe` (CLI) |
| `slcode-res.rc` | Windows resource file for icon embedding via windres |
| `icon.ico` | App icon — embedded in both stubs |
| `build.py` | Build script: runs PyInstaller, zips bundle, compiles C stubs via MinGW gcc |
| `build-bootloader.py` | Compiles a custom PyInstaller bootloader (run once, rarely needed) |
| `requirements.txt` | Python dependencies (pywebview, pystray, Pillow, pyinstaller) |
| `LSL Cache/` | Bundled cache — copied into the dist bundle; also used directly in dev |
| `LSL Cache/skills/` | Cache tool scripts — each is a standalone Python script |
| `dist/` | Build output: `SLCode.exe`, `slcode-cli.exe`, `SLCode-app.zip` |
| `make-release.ps1` | PowerShell release packaging script |

---

## Architecture

### Two-stub build

Two small C executables wrap the Python bundle:

| Stub | Subsystem | Entry | Purpose |
|---|---|---|---|
| `SLCode.exe` | WINDOWS (`-mwindows`) | `wWinMain` | GUI launch — no console ever, shows splash |
| `slcode-cli.exe` | CONSOLE (`-DCONSOLE_MODE`) | `wmain` | CLI — inherits terminal, shows spinner |

The stubs are compiled by `build.py` using MinGW `gcc` + `windres`. Both link `slcode-res.o`
(icon resource) and the same `slcode-stub.c` source — a `#define CONSOLE_MODE` switch controls
which entry point and subsystem is used.

### Stub → Python IPC

The GUI stub creates a named Windows event `SLCodeReady_<pid>` and sets `SLCODE_STUB_PID` in
the child process environment before launching Python. Python signals the event when the UI is
ready (webview shown, browser opened, or server started headless). The stub's splash window
waits on this event (up to 30 s) via `MsgWaitForMultipleObjects`, then closes.

### First-run extraction

On first launch the stub detects that `%LOCALAPPDATA%\SLCode\SLCode-app\` doesn't exist,
shows a splash, and extracts `SLCode-app.zip` via PowerShell. Subsequent launches skip
directly to Python. `--extract` forces re-extraction.

### Runtime paths

| Context | Cache location |
|---|---|
| Installed (dist) | `%LOCALAPPDATA%\SLCode\LSL Cache\` |
| Dev (run from source) | `./LSL Cache/` (repo root) |

`search-cache.py` auto-detects which location exists.

### CLI modes (inside slcode-stub.c)

| Mode | Trigger | Behaviour |
|---|---|---|
| `MODE_GUI` | `SLCode.exe` | Splash + Python GUI |
| `MODE_CLI_CMD` | `slcode-cli <command>` or `--no-open` | No splash, runs Python command directly |
| `MODE_CLI_GUI` | `slcode-cli` (no args) | Delegates to `SLCode.exe` next to itself, prints detach message |

---

## search-cache.py structure

This is a large (~8000 line) intentionally self-contained single file. Do not split it.

Key sections (roughly in order):

1. **Imports and path constants** — `CACHE_ROOT`, `DOCS_DIR`, category dirs
2. **INDEX loading** — reads all `.md` front matter into memory on startup
3. **Cache tools registry** — list of dicts: `{id, name, description, cmd, options, note, web}`
4. **Skill runner** — `run_skill_cmd()`, `_skill_cmd()` helper
5. **LSL checker** — `run_checks()`, `run_sanity_checks()`, lslint wrapper
6. **Analyser** — memory estimator, channel map, sleep profiler
7. **Formatter** — `format_lsl()`
8. **HTTP server** — `BaseHTTPRequestHandler` subclass handling all `/api/*` routes
9. **CLI** — `argparse` subcommands: serve, search, lookup, check, analyze, debug, format, flatten, completions, fs, cache, status
10. **`initialize_runtime()`** — startup: load index, start watchers
11. **`serve_ui()`** — starts HTTP server + pywebview or system browser
12. **`main()`** — entry point, arg dispatch, quiet mode logic
13. **Embedded web UI** — large `HTML_CONTENT` string containing all HTML/CSS/JS inline

### UI is fully inline

All HTML, CSS, and JavaScript live inside `search-cache.py` as a single `HTML_CONTENT` string.
There are no separate `.html`, `.css`, or `.js` files. External CDN resources are not used —
everything must work offline. The only external JS loaded is `marked.js` via a bundled copy
(check how it's currently handled before assuming).

### Quiet mode

`_QUIET_MODE = True` suppresses `_log()` output. Set for all non-`serve` CLI commands during
`initialize_runtime()` to avoid polluting CLI output; cleared (or kept quiet for `--json` mode)
after init.

---

## Cache tools / skills

Skills live in `LSL Cache/skills/` as standalone Python scripts. They are invoked by
`run_skill_cmd()` as subprocesses. Each skill:
- Has a header comment block: `# Skill: ...`, `# Version: ...`, `# Purpose: ...`, `# Usage: ...`
- Reads `LSL_CACHE_BASE` env var (set by the launcher) to find the cache root
- Operates on `lsl-docs/` and `cache-manifest.json` within the cache
- Prints progress to stdout (streamed live to the Tools panel)

The tools registry in `search-cache.py` maps each tool `id` to a `cmd` list via `_skill_cmd(name)`.

### OSSL fetch fallback chain

`fetch-ossl-docs.py` tries opensimulator.org wiki first. If the wiki returns 0 functions
**or** >80% of page fetches fail, it automatically delegates to `generate-ossl-from-kwdb.py`
(local, no internet required). Both scripts exit 0 on success.

---

## Build process

```
python build.py                  # standard build (onedir + zip)
python build.py --onefile        # legacy single-file mode
python build.py --prune-artifacts  # clean PyInstaller cache after build
```

**Requirements:**
- Python packages: `pip install pyinstaller pywebview pystray pillow`
- MinGW gcc (for stub compilation): `C:\msys64\mingw64\bin\gcc.exe` or on PATH
- windres (for icon embedding): in same bin dir as gcc

**Output in `dist/`:**
- `SLCode.exe` — GUI launcher stub
- `slcode-cli.exe` — CLI launcher stub
- `SLCode-app.zip` — Python bundle (extracted to `%LOCALAPPDATA%\SLCode\` on first run)

**What build.py does:**
1. Copies `search-cache.py` → `build/_slcode_runtime.py` and `build/slcode_runtime.py`
2. Runs PyInstaller on `slcode-launcher.py` with all hidden imports and data files
3. Zips the onedir output to `SLCode-app.zip`
4. Compiles `slcode-res.rc` → `slcode-res.o` via windres (icon resource)
5. Compiles `slcode-stub.c` → `SLCode.exe` (WINDOWS subsystem) and `slcode-cli.exe` (CONSOLE)

---

## Conventions

- **Versioning**: `claudelog.md` tracks changes. `project.json` version field is rarely updated
  (it's a dev config, not a release version). Release versioning is managed separately.
- **No external assets in UI**: All UI resources must be inline or bundled. No CDN calls.
- **Self-contained skills**: Each skill in `LSL Cache/skills/` must work as a standalone script.
- **Front matter in docs**: All `.md` files in `lsl-docs/` must have YAML front matter with
  at least `name`, `category`, `type`, `language`, `description`.
- **INDEX is front-matter only**: `search-cache.py` loads only YAML front matter into memory
  at startup, not full doc bodies. Bodies are read on demand per request.

---

## Common tasks

### Add a new cache tool

1. Create `LSL Cache/skills/<tool-name>.py` with the standard skill header
2. Add an entry to the `CACHE_TOOLS` list in `search-cache.py`:
   ```python
   {
       "id":          "my-tool",
       "name":        "Human Name",
       "description": "What it does.",
       "cmd":         _skill_cmd("my-tool"),
       "options":     [...],   # list of {flag, label, type, default}
       "note":        None,    # or a string shown below the run button
       "web":         False,   # True if internet access required
   }
   ```

### Add a new CLI command

Add a subparser in the `main()` / argparse section, add a handler function, and wire it in
the dispatch block at the bottom of `main()`.

### Add a new API route

Add a branch in `do_POST` or `do_GET` inside the `HTTPRequestHandler` class.
All API routes are under `/api/`.

### Modify the UI

Edit the `HTML_CONTENT` string in `search-cache.py`. CSS is in a `<style>` block,
JS in a `<script>` block, both inline. Use `renderDoc()` for displaying markdown docs.

### Test without building

```
python search-cache.py serve
python search-cache.py serve --as-browser
python search-cache.py check path/to/script.lsl
```

---

## What to avoid

- **Don't split `search-cache.py`** — it's intentionally one file for simple distribution.
- **Don't add CDN dependencies** — the app must work offline.
- **Don't use `subprocess` in the web UI JS** — the UI is sandboxed WebView2.
- **Don't modify `dist/` files directly** — always rebuild from source.
- **Don't commit `build/` or `dist/`** — these are build artefacts.
