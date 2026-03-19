# Claude Change Log

All changes made by Claude to this project are recorded here.

---

## [0.1.0.1] — 2026-03-09
### Initialisation
- Created project.json (cache_path: ~/.lsl-cache, language: LSL, region: mainland)
- Cache status: FULL BUILD — all steps complete as of session 2026-03-09
- Downloaded LSL documentation to ~/.lsl-cache/lsl-docs/ (39 functions, 17 events, 7 constant groups, 3 tutorials, 5 reference pages)
- Imported extension data: jyaoma (4 files), kwdb (1 file), pyoptimizer (2 files), makopo (1 file), buildersbrewery (2 files)
- Created ~/.lsl-cache/lsl-docs/vscode-extension-data/RECONCILIATION.md — 3 makopo-only functions noted, return type gaps flagged
- Created ~/.lsl-cache/cache-manifest.json — all 5 sources marked, patterns_last_run: 2026-03-09
- Ran ~/.lsl-cache/skills/analyse-snippets.py (v0.1.0.1) — pattern library built: 850 idioms, 5 patterns, 5 anti-patterns, 406 function-usage notes (1266 total); 411 function docs updated with pattern refs
- Copied jyaoma/snippets.json → .vscode/lsl.code-snippets (91 entries)
- Created .vscode/extensions.json with recommended LSL extensions
- Created skills/templates/state-machine.lsl — reusable FSM boilerplate
- Created skills/templates/listen-handler.lsl — reusable listen/dialog boilerplate
- Created skills/templates/timer-loop.lsl — reusable timer pattern
- Created skills/lint-check.sh — LSLint wrapper for all project scripts
- Created ~/.lsl-cache/skills/doc-format-reference.md
- Created ~/.lsl-cache/skills/analyse-snippets.py (updated to v0.1.0.1: JSONC support, Windows UTF-8 stdout fix)
- Created ~/.lsl-cache/skills/update-extension-data.sh
- Updated file-index.md with final counts
- Updated claudelog.md

## [0.1.0.1] — 2026-03-10 (doc gap-fill)
### Summary
Generated docs for all 489 missing LSL functions and events from local cache data (jyaoma + pyoptimizer + makopo). No web requests needed. Cache now has complete coverage of all 502 known functions and 43 events.

### Changes
- Created ~/.lsl-cache/skills/generate-docs-from-cache.py — synthesises docs from jyaoma + pyoptimizer + makopo without web fetching
- Created ~/.lsl-cache/skills/fetch-missing-docs.py — web fetcher (disabled: SL wiki api.php returns 404; HTML scraping approach archived)
- Generated 463 function docs: llAbs through llZeroMemory — all with signatures, parameters, return types, sleep/energy costs, flags
- Generated 26 event docs: at_rot_target, collision, email, experience_permissions, http_request, linkset_data, etc.
- Updated cache-manifest.json: functions 39→502, events 17→43, total 71→560
- Updated lsl-docs/README.md, CHANGELOG.md, file-index.md

## [0.1.0.1] — 2026-03-09 (sanity check + fixes)
### Summary
Full cache sanity check performed. 11 issues found (5 FAIL, 6 WARN). All FAILs resolved; all WARNs addressed or documented.

### Changes
- Re-fetched kwdb/kwdb.xml from correct path (`database/kwdb.xml`). Original fetch stored "404: Not Found" (14 bytes). File now valid (498 KB, ~5000+ entries).
- Fixed lsl-docs/README.md: header count corrected from 78 to 71 (actual)
- Updated RECONCILIATION.md: kwdb fetch failure history noted; kwdb re-fetch and Experience API function confirmations logged
- Updated ~/.lsl-cache/skills/analyse-snippets.py → v0.1.0.2:
  - Added `is_completion_token()` to skip single-token buildersbrewery constant entries (these are completion tokens, not patterns)
  - Restricted `ANTI_PATTERN_MARKERS` to genuinely harmful patterns (llSleep, llResetScript only — removed llSensor/llSensorRepeat/llGetAgentList which are legitimate functions)
  - Added `None` return from classifier for completion tokens — these are now silently skipped
  - Fixed hardcoded version string in output banner
- Deleted and rebuilt full pattern library with corrected classifier:
  - Before: 1266 entries (850 false-idioms, 5 misclassified anti-patterns)
  - After: 451 entries (37 real idioms, 3 patterns, 2 anti-patterns, 409 function-usage notes)
- switch-statement.md: added Firestorm-only warning, populated When to Use and Gotchas sections
- Updated cache-manifest.json: added kwdb_notes, pattern_counts

## [0.1.0.2] — 2026-03-10
### Summary
Fixed scraper output quality issues, ran full wiki scrape, fixed search frontend index staleness.

### Changes
- Updated ~/.lsl-cache/skills/scrape-wiki-pages.py → v0.1.3.0:
  - Fixed truncated Caveats: `<[^>]+>` → `<[a-zA-Z/!][^>]*>` so literal `<200/10sec` in wiki text is preserved
  - Fixed empty See Also: removed separate `convert_see_also_row` pass (which conflicted with `convert_table`); integrated bullet-table detection directly into `convert_table`
  - Added `&mdash;`, `&ndash;`, `&bull;` to `unescape()`
- Ran full wiki scrape across all 545 docs: 541 merged, 4 skipped (2 no-content, 2 no-change), 0 failed
- Updated search-cache.py → v0.1.0.1: added reference category (types/operators/flow-control/script-limits/style-guide), removed all result limits, added /api/reload and /api/status endpoints, added ↺ reload button
- Updated cache-manifest.json: wiki_scrape_last_run, wiki_scrape_counts

## [0.1.0.1] — 2026-03-16 (documentation overhaul)
### Summary
Reworked project documentation for faster human/AI onboarding and updated the project index to include the new docs set.

### Changes
- Rewrote README.md with complete setup, run modes, validation, build, and docs-map guidance
- Created docs/ARCHITECTURE.md — runtime architecture and subsystem map
- Created docs/CLI_REFERENCE.md — CLI command reference and usage patterns
- Created docs/TROUBLESHOOTING.md — known issues, diagnostics, and recovery steps
- Created docs/NAVIGATION.md — maintainer map for where to change what
- Updated file-index.md — refreshed last-updated date and added new documentation files

## [0.1.0.2] — 2026-03-18
### Summary
Fixed the console (CLI) launcher stub, rewrote the Outworldz script scraper using the GitHub tree API, added GitHub PAT auth support to both the scraper and the GUI tools pane, and shipped a full clean build.

### Changes
- Modified `slcode-stub.c` — renamed console stub output to `slcode-cli.exe`; fixed silent extraction failure by replacing env-var PowerShell approach with a temp `.ps1` file (paths baked as single-quoted literals); added `CONSOLE_MODE` debug output with `%ls` wide-string format fix (build +1)
- Modified `build.py` — updated console stub output name from `slcode.exe` → `slcode-cli.exe` (build +1)
- Created `LSL Cache/skills/fetch-outworldz.py` — new dedicated Outworldz scraper using GitHub tree API for instant file discovery (1 API call vs 3000+ HTTP crawl requests); supports `--token`, `--save-token`, `--clear-token`, `--force`, `--limit`, `--dry-run`
- Modified `search-cache.py` — added `_GH_TOKEN_FILE`, `_gh_token_status()`, `GET /api/github/token`, `POST /api/github/token` (save/clear actions), GitHub auth card in tools pane (`ghAuthCardHtml`, `_bindGhAuthEvents`, `_ghAuthAction`), auto-injection of saved token into all tool job subprocess environments (build +1)
- Full build: `dist/SLCode.exe` (138 KB), `dist/slcode-cli.exe` (265 KB), `dist/SLCode-app.zip` (24 MB)

## [0.1.0.3] — 2026-03-18
### Summary
Repo cleanup, CLAUDE.md rewrite for app maintenance context, OSSL fetch fallback chain with
GitHub source, version-based extraction with user-deletable version.txt, and full documentation
overhaul across README and all docs/*.

### Changes
- Deleted 53 stale files: all `_` prefixed test/debug scripts and output files, old `.spec` files,
  old `.cmd` launchers, `CLAUDE_CODE_HANDOFF.md`, `DEPLOYMENT-NOTES.md`, `RELEASE.md`, `file-index.md`
- Rewrote `CLAUDE.md` — now documents the SLCode app repo (architecture, key files, build process,
  conventions, common tasks) instead of being a generic LSL scripting assistant guide
- Created `LSL Cache/skills/fetch-ossl-from-github.py` (v0.1.0.0) — parses `IOSSL_Api.cs` and
  `OSSL_Api.cs` from opensim/opensim GitHub; extracts `//ApiDesc` descriptions and
  `CheckThreatLevel()` threat levels; cross-references kwdb and makopo; generates OSSL .md files
- Modified `LSL Cache/skills/fetch-ossl-docs.py` (v0.1.0.2) — added three-level fallback chain:
  opensimulator.org wiki → GitHub source (`fetch-ossl-from-github.py`) → local kwdb
  (`generate-ossl-from-kwdb.py`); fallback triggers on 0 results or >80% error rate
- Modified `search-cache.py` — updated `fetch-ossl` tool description and note to describe the
  fallback chain; added new `fetch-ossl-github` tool entry pointing to the GitHub skill
- Modified `slcode-stub.c` — replaced mtime-based extraction check with version string comparison:
  reads `version.txt` from extracted bundle, compares with compiled-in `APP_VERSION`; added
  `is_update` flag to show "Installing…" vs "Updating…" vs "Loading…" on splash and CLI spinner;
  removed `_write_mtime_file` / `_read_mtime_file` / `_get_file_mtime` helpers
- Modified `build.py` — added `_build_version_string()` (git short hash + date, or date+local),
  `_write_version_file()` (writes version.txt into bundle before zipping), passes
  `-DAPP_VERSION="..."` to gcc for both stubs; handles both onedir and onefile modes
- Rewrote `README.md` — reflects current file layout, correct build/run commands, removed
  references to deleted files
- Rewrote `docs/ARCHITECTURE.md` — added two-stub design, splash/IPC, version-based extraction,
  CLI detach, OSSL fallback chain, full build pipeline steps, runtime path table
- Rewrote `docs/NAVIGATION.md` — updated entry points, per-subsystem change locations, current
  repo layout, clean workflow; removed references to deleted files
- Rewrote `docs/CLI_REFERENCE.md` — removed deleted validation scripts section, corrected serve
  options, added --ossl/--fs flags, added new OSSL cache tool entries
- Rewrote `docs/TROUBLESHOOTING.md` — removed deleted script references, added version.txt
  re-extraction section, OSSL fallback explanation, MinGW install instructions, updated health check
- Full rebuild: version 20260318-local embedded in both stubs and bundle

<!-- INIT_COMPLETE -->
