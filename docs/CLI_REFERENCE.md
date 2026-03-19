# CLI Reference

## Running from source vs. installed

**From source:**
```
python search-cache.py <command> [options]
```

**From installed build:**
```
slcode-cli <command> [options]
```

All commands, options, and exit codes are identical either way.

---

## serve — start the UI server

```
slcode-cli serve
slcode-cli serve --port 9000
slcode-cli serve --as-browser          # force system browser
slcode-cli serve --no-open             # headless server (no window)
slcode-cli serve --use-external path\to\file   # Firestorm external editor mode
```

**Options:**
- `--port N` — listen port (default: 8080)
- `--as-browser` — open in system browser instead of embedded WebView2
- `--no-open` — start server without opening any window
- `--use-external <path>` — watch a file for Firestorm external editor sync

---

## status — cache and index summary

```
slcode-cli status
slcode-cli status --json
```

---

## search — search the doc cache

```
slcode-cli search llSay
slcode-cli search "touch start" --cat events
slcode-cli search timer --limit 5
slcode-cli search llSetPos --json
```

**`--cat` values:** `all` · `functions` · `events` · `constants` · `tutorials` · `ossl` · `slua` · `examples` · `patterns` · `idioms` · `anti-patterns` · `function-usage` · `reference`

---

## lookup — exact symbol lookup

```
slcode-cli lookup llSay
slcode-cli lookup PRIM_TYPE_BOX
slcode-cli lookup touch_start --json
```

---

## doc — read a cache doc file

```
slcode-cli doc functions/llSay.md
slcode-cli doc events/touch_start.md
slcode-cli doc ossl/osNpcCreate.md
```

---

## check — lint and syntax-check a script

```
slcode-cli check path\to\script.lsl
slcode-cli check path\to\script.lsl --mode syntax
slcode-cli check path\to\script.lsl --mode lint
slcode-cli check path\to\script.lsl --mode all
slcode-cli check --stdin < script.lsl
slcode-cli check path\to\script.lsl --json
slcode-cli check path\to\script.lsl --ossl        # treat os* functions as valid
slcode-cli check path\to\script.lsl --fs          # Firestorm preprocessor mode
slcode-cli check path\to\script.lsl --ossl --fs   # both
```

**Modes:** `syntax` · `sanity` · `lint` · `both` (syntax+sanity, default) · `all`

`--ossl` — suppresses unknown-function errors for all `os*` OpenSimulator extension functions.
`--fs` — pre-flattens Firestorm `#include` / `#define` directives before checking.

---

## analyze — run analysis tools

```
slcode-cli analyze path\to\script.lsl
slcode-cli analyze --stdin < script.lsl
slcode-cli analyze path\to\script.lsl --json
```

Runs: memory estimator, channel map, sleep profiler.

---

## debug — full pipeline (check + analyze)

```
slcode-cli debug path\to\script.lsl
slcode-cli debug path\to\script.lsl --json
slcode-cli debug path\to\script.lsl --ossl
slcode-cli debug path\to\script.lsl --fs
slcode-cli debug path\to\script.lsl --ossl --fs
```

---

## format — auto-format a script

```
slcode-cli format path\to\script.lsl
slcode-cli format --stdin < script.lsl
```

Prints formatted output to stdout. Does not modify the file.

---

## flatten — resolve `#include` directives

```
slcode-cli flatten path\to\script.lsl
slcode-cli flatten --stdin < script.lsl
```

Expands Firestorm preprocessor `#include` chains and prints the result.

---

## completions — IDE completion data

```
slcode-cli completions
slcode-cli completions --json
```

---

## fs — project filesystem

```
slcode-cli fs cwd
slcode-cli fs chdir path\to\project
slcode-cli fs list
slcode-cli fs read  relative\path.lsl
slcode-cli fs write relative\path.lsl     # content on stdin
slcode-cli fs mkdir relative\dir
slcode-cli fs delete relative\path
slcode-cli fs rename old\path new\path
```

---

## cache — cache inspection and maintenance

```
slcode-cli cache status
slcode-cli cache reload
slcode-cli cache tools
slcode-cli cache gaps
slcode-cli cache validate
slcode-cli cache disk-usage
slcode-cli cache reconciliation
slcode-cli cache pattern-tags
slcode-cli cache run <tool-id> [--flag=<flag>] [--set=<flag>=<value>]
```

### cache run examples

```
slcode-cli cache run full-update
slcode-cli cache run fetch-ossl             # tries wiki → GitHub → kwdb fallback
slcode-cli cache run fetch-ossl-github      # directly from opensim/opensim GitHub source
slcode-cli cache run generate-ossl-from-kwdb  # local only, no internet
slcode-cli cache run scrape-wiki --set=--type=functions --set=--limit=10
slcode-cli cache run cache-repair --flag=--dry-run
```

**Option forwarding:**
- `--flag=<tool-flag>` — pass a boolean flag to the tool (e.g. `--flag=--force`)
- `--set=<tool-flag>=<value>` — pass a key=value option (e.g. `--set=--limit=50`)

---

## Exit codes

| Code | Meaning |
|---|---|
| `0` | Success |
| `1` | Error / issues found |
| `2` | Argument / usage error |

Output lines prefixed `[slcode-cli]` go to stderr. Actual command output goes to stdout.
