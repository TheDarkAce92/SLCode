# Troubleshooting

## App won't start / extraction hangs

### Symptom
`SLCode.exe` splash appears but never progresses, or nothing opens.

### Checks
- Look for a stale PowerShell extraction process in Task Manager
- Delete `%LOCALAPPDATA%\SLCode\SLCode-app\` and relaunch (fresh extraction)
- Run from terminal via `slcode-cli.exe serve` to see error output
- Verify `SLCode-app.zip` exists next to `SLCode.exe` in the dist folder

---

## Splash appears but UI never loads

### Symptom
Splash shows "Loading SLCode…" indefinitely, then closes without a window.

### Cause
Python crashed during startup, or pywebview failed to open.

### Fix
- Run `slcode-cli.exe serve` from a terminal — errors will appear in the console
- Try `slcode-cli.exe serve --as-browser` to bypass pywebview

---

## App doesn't update after installing a new build

### Expected behaviour
On each launch the stub reads `version.txt` from the extracted bundle and compares it to the compiled-in build version. A mismatch triggers automatic re-extraction.

### Force re-extraction manually
Either:
- Delete `%LOCALAPPDATA%\SLCode\SLCode-app\version.txt` (triggers update on next launch)
- Run `SLCode.exe -extract` or `slcode-cli.exe serve -extract`

---

## OSSL docs fetch fails

### Symptom
"Fetch OSSL Docs" in the Tools panel reports errors or produces 0 results.

### Cause
opensimulator.org wiki is frequently unreachable.

### How the fallback works
`fetch-ossl-docs.py` automatically tries three sources in order:
1. opensimulator.org wiki (often fails)
2. GitHub source (`IOSSL_Api.cs` + `OSSL_Api.cs` from opensim/opensim) — includes descriptions and threat levels
3. Local kwdb + makopo data — no internet required

If the wiki fails you'll see `[fetch-ossl] Falling back to GitHub source...` in the output.
Use **"Fetch OSSL Docs (GitHub)"** in the Tools panel to skip directly to the GitHub source.

---

## pywebview file dialog errors

### Symptom
Error about invalid file filter when opening or saving via native dialog.

### Current behaviour
The app tries filtered dialogs first, then retries without filters if the backend rejects the syntax.

### If still failing
- Run with `--as-browser` and use the browser's HTML file input fallback
- Verify pywebview version: `pip show pywebview`

---

## Ctrl+C / shutdown doesn't clean up

### Browser / terminal mode
Ctrl+C should terminate cleanly. If not, check for stale Python processes.

### GUI mode (pywebview)
Window close triggers shutdown cleanup. If a Python process remains, kill it manually.

---

## Cache tool timeout

### Symptom
`cache run` returns "tool timed out".

### Causes
- Long-running scraper or update job
- Option forwarding syntax error

### Checks
- Pass options with `--set=<flag>=<value>`, e.g. `--set=--limit=10`
- Test with a small limit first: `--set=--limit=1`
- Check available tools: `slcode-cli cache tools --json`

---

## Wiki scrape failures

### Symptom
Scraper exits with code 1 or parser exceptions for specific pages.

### Current behaviour
Scraper handles page and section parsing errors defensively and continues with remaining targets.

### Recommended workflow
- Test a single page: `cache run scrape-wiki --set=--limit=1`
- Scale up: limit 10, then 50

---

## Build errors

### Clean rebuild
```
python build.py --prune-artifacts
```

### gcc / windres not found
MinGW gcc is required for stub compilation. Install via:
```
winget install MSYS2.MSYS2
```
Then install MinGW toolchain inside MSYS2:
```
pacman -S mingw-w64-x86_64-gcc
```
Ensure `C:\msys64\mingw64\bin` is on PATH, or `build.py` will find it automatically.

### Verify built binary (from source)
```
python search-cache.py status --json
```

### Verify built binary (dist)
```
dist\slcode-cli.exe status --json
```

---

## Quick health check

```
python search-cache.py status --json
python search-cache.py search llSay --json
python search-cache.py check path\to\script.lsl
dist\slcode-cli.exe status --json
```
