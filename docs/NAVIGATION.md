# Navigation Guide

Where to look and what to change for common maintenance tasks.

---

## Primary entry points

| File | Role |
|---|---|
| `search-cache.py` | Everything: server, UI, CLI, cache tools, index |
| `slcode-stub.c` | C launcher stub — extraction, splash, IPC, mode detection |
| `build.py` | Build orchestration: PyInstaller, version string, zip, stubs |
| `LSL Cache/skills/` | Cache maintenance scripts |
| `docs/` | Developer documentation |
| `CLAUDE.md` | AI/maintainer guide |

---

## Where to make specific changes

### CLI behaviour

- Subcommand parsers: `main()` → argparse setup block
- Command handlers: functions named `_cmd_*` or inline in the dispatch block at the bottom of `main()`
- Quiet mode (suppress startup logs for non-serve commands): `_QUIET_MODE` logic in `main()`

### Web UI behaviour

- All UI code is in the `HTML_CONTENT` string in `search-cache.py`
- CSS: inside the `<style>` block in `HTML_CONTENT`
- JavaScript: inside the `<script>` block in `HTML_CONTENT`
- Key JS functions: `setMode()` (page switching), `renderDoc()` (markdown rendering), `doSearch()` (search)
- Subcategory menus: `OSSL_SUBTABS`, `EXAMPLE_SUBTABS`, `_buildSubtabs()`, `osslSubcat()`, `exampleSubcat()`
- Mode switching clears subtabs in the `else` branch of `setMode()` — if a submenu persists across pages, that's where to fix it

### HTTP API endpoints

- All in the `HTTPRequestHandler` class: `do_GET` / `do_POST` dispatch to inner methods
- Add new routes by matching on `self.path` in `_do_GET_inner` or `_do_POST_inner`

### Cache tools (Tools panel)

- Registry: `CACHE_TOOLS` list in `search-cache.py` — each entry has `id`, `name`, `description`, `cmd`, `options`, `note`, `web`
- Skill script: `LSL Cache/skills/<tool-name>.py`
- Add a tool: create the skill script + add an entry to `CACHE_TOOLS`

### Splash window

- `slcode-stub.c`: `_splash_create()`, `_splash_set_status()`, `_splash_destroy()`
- Status text at each stage: in `_run()` where `need_extract`/`is_update` are checked
- Python side signal: `_signal_splash_ready()` in `search-cache.py`

### Extraction / version check

- Stub side: `_read_version_file()` + version check block in `_run()` in `slcode-stub.c`
- Build side: `_build_version_string()`, `_write_version_file()` in `build.py`
- Version is compiled in as `-DAPP_VERSION="..."` gcc flag
- `version.txt` lives at `%LOCALAPPDATA%\SLCode\SLCode-app\version.txt` after extraction

### CLI detach (slcode-cli → SLCode.exe delegation)

- `slcode-stub.c`: `MODE_CLI_GUI` branch — locates `SLCode.exe` next to itself, launches it, prints detach message

### Stub compilation / icon

- `slcode-stub.c` — source
- `slcode-res.rc` — resource file (icon ID 1)
- `icon.ico` — icon file
- `build.py`: `_compile_resource()` (windres), `_build_stub_exe()` (gcc)

### OSSL documentation fetch

- `LSL Cache/skills/fetch-ossl-docs.py` — wiki scraper + fallback chain trigger
- `LSL Cache/skills/fetch-ossl-from-github.py` — GitHub C# source parser (preferred fallback)
- `LSL Cache/skills/generate-ossl-from-kwdb.py` — local-only kwdb/makopo generator (final fallback)
- Fallback order: wiki → GitHub → kwdb

### Index / cache

- Index is built from YAML front matter of all `.md` files in `LSL Cache/lsl-docs/`
- Rebuilt on startup and via `/api/reload` or `cache reload` CLI command
- `initialize_runtime()` in `search-cache.py` drives the build

---

## Repository layout (clean)

```
LSL Queries/
  search-cache.py          app
  slcode-launcher.py       PyInstaller entry point
  slcode-stub.c            C stub source
  slcode-res.rc            icon resource
  icon.ico
  build.py
  build-bootloader.py
  requirements.txt
  CLAUDE.md
  README.md
  claudelog.md
  project.json
  SLCode-app.spec          PyInstaller spec (generated; kept for reference)
  make-release.ps1
  LSL Cache/               bundled cache
    skills/
    lsl-docs/
  dist/                    build output
  build/                   PyInstaller intermediate (do not commit)
  docs/
    ARCHITECTURE.md
    CLI_REFERENCE.md
    NAVIGATION.md
    TROUBLESHOOTING.md
  src/                     project LSL scripts (if any)
  skills/                  project-local skill templates
  icon-slices/             icon source assets
  bootloader-patch/        custom bootloader source
```

---

## Recommended change workflow

1. Edit `search-cache.py` (or stub/build files as appropriate)
2. Test from source: `python search-cache.py <command>`
3. For stub changes: rebuild with `python build.py` and test `dist/SLCode.exe` / `dist/slcode-cli.exe`
4. For full distribution changes: rebuild + force re-extract with `-extract` flag or by deleting `version.txt`
