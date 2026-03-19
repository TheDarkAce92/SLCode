# SLCode

LSL documentation browser, code assistant, and IDE for Second Life / OpenSimulator scripting.

The app runs fully offline using a bundled local cache — no internet required for core usage.

---

## What's in this repository

| File / Dir | Purpose |
|---|---|
| `search-cache.py` | The entire application: server, web UI, CLI, cache tools |
| `slcode-launcher.py` | PyInstaller entry point |
| `slcode-stub.c` | C stub launcher — compiles to `SLCode.exe` and `slcode-cli.exe` |
| `slcode-res.rc` | Windows resource file (icon embedding via windres) |
| `icon.ico` | App icon |
| `build.py` | Build script: PyInstaller + zip + C stubs via MinGW |
| `build-bootloader.py` | Custom PyInstaller bootloader (run once, rarely needed) |
| `requirements.txt` | Python dependencies |
| `LSL Cache/` | Bundled documentation cache and skill scripts |
| `LSL Cache/skills/` | Cache maintenance scripts (invoked by Tools panel / CLI) |
| `dist/` | Build output |
| `docs/` | Developer documentation |

---

## Setup

**Requirements:** Windows, Python 3.13+, MinGW gcc (for stub compilation)

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

MinGW gcc is only required to build the stub executables. It is not needed to run the app from source.

---

## Running from source

```
python search-cache.py serve                  # open UI (pywebview or browser)
python search-cache.py serve --as-browser     # force system browser
python search-cache.py serve --no-open        # headless server only
python search-cache.py serve --port 9000      # custom port
```

### CLI commands (from source)

```
python search-cache.py status
python search-cache.py search llSay
python search-cache.py lookup llSetText --json
python search-cache.py check path/to/script.lsl --mode both
python search-cache.py check path/to/script.lsl --ossl --fs
python search-cache.py analyze path/to/script.lsl --json
python search-cache.py debug path/to/script.lsl
python search-cache.py format path/to/script.lsl
python search-cache.py flatten path/to/script.lsl
python search-cache.py cache status
python search-cache.py cache run full-update
```

### Post-pull format audit

Run this after scraper pulls to verify imported docs still match expected front matter/body format:

```
python skills/format-audit.py
```

Optional: audit a broader tree (legacy docs may report non-critical misses):

```
python skills/format-audit.py --root "LSL Cache/lsl-docs"
```

---

## Build

**Requirements:** all Python deps installed + MinGW gcc (`C:\msys64\mingw64\bin\gcc.exe` or on PATH)

```
python build.py                      # standard build (recommended)
python build.py --prune-artifacts    # build + clean PyInstaller cache after
python build.py --onefile            # legacy single-file mode
```

**Output in `dist/`:**

| File | Purpose |
|---|---|
| `SLCode.exe` | GUI launcher stub — double-click, no console |
| `slcode-cli.exe` | CLI launcher stub — run from terminal |
| `SLCode-app.zip` | Python bundle — extracted to `%LOCALAPPDATA%\SLCode\` on first launch |
| `README.md` | User-facing documentation |

On first launch the stub extracts `SLCode-app.zip` (~5–10 s). Subsequent launches start instantly.
The extraction re-runs automatically whenever a new build is installed (detected via `version.txt`).
Delete `%LOCALAPPDATA%\SLCode\SLCode-app\version.txt` to force re-extraction manually.

---

## Documentation

| Doc | Contents |
|---|---|
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | Runtime architecture, stub design, IPC, build pipeline |
| [docs/CLI_REFERENCE.md](docs/CLI_REFERENCE.md) | Full CLI command reference |
| [docs/NAVIGATION.md](docs/NAVIGATION.md) | Where to make specific types of changes |
| [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) | Known issues and fixes |
| [CLAUDE.md](CLAUDE.md) | AI/maintainer guide for this repo |
| [dist/README.md](dist/README.md) | End-user documentation (shipped with the app) |
