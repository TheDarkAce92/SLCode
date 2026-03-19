# SLCode Cache Content Audit — Adversarial Analysis Prompt

Use this prompt with Claude Code (or any capable agentic AI with filesystem access)
to run a maximally hostile, adversarial audit of the LSL Cache documentation.
Drop this file in the repo root and run it as a task.

---

## PROMPT (copy everything below this line)

---

You are a hostile documentation auditor. Your job is to find every flaw, gap, inconsistency,
and silent failure in this documentation cache. Do not be polite. Do not skip edge cases.
Do not assume anything is correct just because it exists. Treat every file as potentially
broken until proven otherwise.

The cache is located at: `LSL Cache/lsl-docs/`

Subfolders:
- `functions/`   — 502 LSL function docs (*.md)
- `events/`      — 43 LSL event docs (*.md)
- `ossl/`        — 275 OSSL function docs (*.md)
- `slua/`        — Lua API docs (*.md)
- `constants/`   — LSL constant docs (*.md)
- `patterns/`    — Pattern snippet docs (*.md)
- `tutorials/`   — Tutorial docs (*.md)
- `examples/`    — Example script docs (*.md)

The manifest is at: `LSL Cache/cache-manifest.json`

Each `.md` file has YAML front matter followed by a markdown body.

---

## AUDIT TASKS — perform ALL of the following:

### 1. FRONT MATTER STRUCTURAL INTEGRITY
For every file in `functions/`, `events/`, `ossl/`, `slua/`, `constants/`:
- Does it have a `---` front matter block?
- Are ALL of these fields present and non-empty: `name`, `category`, `type`, `language`, `description`?
- For functions: are `signature`, `return_type`, `energy_cost`, `sleep_time`, `wiki_url` present?
- For events: is `signature` present? Are `parameters` defined (even if empty list)?
- Is `deprecated` present and a boolean string (`"true"` or `"false"`), not missing or null?
- Flag any file where a required field is present but empty string `""` or `null`.

### 2. DESCRIPTION QUALITY — SHAME THE STUBS
For every doc:
- Is the `description` field shorter than 20 characters? → **STUB ALERT**
- Does `description` exactly repeat the function name? → **STUB ALERT**
- Does `description` follow the pattern `"OSSL function: <name>."` → **STUB ALERT** (these were auto-generated and are useless)
- Does the markdown body below the front matter contain NO content beyond a signature block?
  (i.e., no Parameters section, no Notes, no Examples, no caveats) → **THIN CONTENT**
- Does the body just repeat the description verbatim with nothing added? → **THIN CONTENT**
- Collect and report all STUB and THIN CONTENT hits as a prioritised list.

### 3. CATEGORY / TYPE CONSISTENCY
- `category` and `type` should be consistent. Known valid combos:
  - functions: `category: "function"`, `type: "function"`
  - events: `category: "event"` OR `category: "events"` (note: inconsistency exists — flag all `"events"` as wrong, should be `"event"`)
  - OSSL: `category: "function"`, `type: "function"`, `language: "OSSL"`
  - constants: `category: "constant"`, `type: "constant"`
  - patterns: `category: "pattern"`, `type: "pattern"`
- Flag any file where `category` and `type` disagree with each other.
- Flag any file where `language` is not one of: `"LSL"`, `"OSSL"`, `"Lua"`.
- Flag any file in `functions/` folder with `language: "OSSL"` (wrong folder).
- Flag any file in `ossl/` folder with `language: "LSL"` (wrong folder).

### 4. DUPLICATE DETECTION
- Scan ALL docs across ALL subfolders.
- Find any two docs with the same `name` field value (case-insensitive).
- Find any two docs where the `signature` fields are identical.
- Report duplicates with both file paths.

### 5. BROKEN CROSS-REFERENCES
- For every `see_also` field (if present), extract each referenced name.
- Check whether a doc with that `name` exists anywhere in the cache.
- Report every broken reference: which file, which `see_also` entry, what's missing.
- Also check if `wiki_url` fields are malformed (not starting with `https://`).

### 6. SLEEP TIME ANOMALIES
For functions (LSL only):
- `sleep_time` should be a numeric string (`"0.1"`, `"1.0"`, `"2.0"`) OR empty string `""` (means no sleep).
- Flag any `sleep_time` that is not a valid float string and not empty.
- Check for known high-sleep functions:
  - `llSleep` should have `sleep_time` matching its argument semantics (it's a special case)
  - Functions like `llDialog`, `llTextBox`, `llRequestPermissions` have `sleep_time: "1.0"` — verify.
  - Functions like `llInstantMessage`, `llEmail` have `sleep_time: "2.0"` — verify.
  - Functions like `llGiveInventory` have `sleep_time: "0.0"` but throttle — note any with unusual values.
- Build a sorted table of all non-empty sleep_time values and flag outliers.

### 7. COVERAGE GAPS — WHAT'S MISSING
Cross-reference the documented functions against the known LSL function list.
Use the `lslint-builtins.txt` file at the repo root as the authoritative list of valid LSL identifiers.
- Extract all names from `lslint-builtins.txt` that look like function names (start with `ll`).
- Compare against all `name` fields in `functions/`.
- Report: functions in builtins but NOT in docs (missing docs).
- Report: functions in docs but NOT in builtins (possibly deprecated, OSSL-only, or phantom).

### 8. SIGNATURE FORMAT CORRECTNESS
For every function doc with a `signature` field:
- Does the signature match the pattern: `<return_type> <name>(<params>)`?
- Does `return_type` in the front matter match the return type in `signature`?
- Are parameter types all valid LSL types? Valid types: `integer`, `float`, `string`, `key`, `vector`, `rotation`, `list`, `void`.
- For OSSL: same rules apply but `llKey2Name`-style types may vary — flag anything that looks wrong.
- Flag any signature that contains `???`, `TBD`, `unknown`, or similar placeholder text.

### 9. DATE FIELD SANITY
- `first_fetched` and `last_updated` should be ISO dates (YYYY-MM-DD).
- Flag any that are malformed, in the future (after today: 2026-03-19), or clearly wrong (before 2020).
- Flag any doc where `last_updated` is BEFORE `first_fetched`.

### 10. MANIFEST CONSISTENCY
- `cache-manifest.json` reports: `functions: 502`, `events: 43`.
- Count the actual files in `functions/` and `events/` directories.
- If counts don't match, report the discrepancy and list the extras or missing.
- Check that all `extension_sources` named in the manifest have at least some files traceable to them
  (look for `source:` fields in front matter if present).

### 11. FACTUAL ACCURACY VALIDATION (NOT JUST FORMAT)
Do a truth-check pass for representative samples and all high-risk pages.

- Build a representative accuracy sample:
  - At least 50 LSL function docs across common + obscure APIs
  - At least 10 events
  - At least 25 OSSL docs
  - Include all docs modified in the last 14 days (`last_updated` recent)

- For each sampled doc, verify against authoritative source data:
  - LSL: compare with `lslint-builtins.txt`, `vscode-extension-data` sources, and wiki metadata where available
  - OSSL: compare with GitHub/OpenSim source data first, then local cache datasets:
    - `LSL Cache/skills/fetch-ossl-from-github.py` parsing targets (`IOSSL_Api.cs`, `OSSL_Api.cs`)
    - `vscode-extension-data/kwdb/kwdb.xml`
    - `vscode-extension-data/makopo/tooltipdata.json`
    - OpenSim wiki only as optional secondary corroboration when reachable

- Validate factual fields for correctness (not just presence):
  - function/event name correctness
  - signature correctness (parameter order/types/names)
  - return type correctness
  - OSSL threat level correctness where available from `OSSL_Api.cs`
  - sleep/energy value plausibility and known values where applicable
  - deprecation status plausibility
  - description claim accuracy (flag claims contradicted by source)

- Detect likely hallucinations/fabrications:
  - Signatures that are syntactically valid but not present in source datasets
  - Parameters mentioned in body but not in signature/source
  - Return types that conflict with source
  - OSSL docs claiming unsupported threat levels or capabilities not present in GitHub source
  - "Confident" prose with no matching source support

- Score each sampled doc:
  - `accurate`
  - `partially-accurate`
  - `inaccurate`
  - `unverifiable`

- Report an overall accuracy rate and include hard evidence for each inaccurate item:
  - doc path
  - incorrect value
  - expected value
  - source used for verification

---

## OUTPUT FORMAT

Produce a structured audit report with these sections:

```
## AUDIT SUMMARY
Total files scanned: N
Issues found: N (Critical: N, Warning: N, Info: N)

## CRITICAL (must fix before release)
[list]

## WARNINGS (should fix, degrades quality)
[list]

## INFO (nice to know, low priority)
[list]

## STUB DOCS — Prioritised Fix List
[ranked list: worst stubs first, include file path + current description]

## COVERAGE GAPS
[missing functions | phantom functions]

## DUPLICATE ENTRIES
[file pairs]

## BROKEN CROSS-REFERENCES
[file: bad_ref]

## SLEEP TIME ANOMALIES
[sorted table]

## ACCURACY FAILURES
[doc path | claimed value | expected value | source]

## ACCURACY SCORECARD
[accurate / partially-accurate / inaccurate / unverifiable counts + percentages]

## CLEAN PASSES
[which checks passed with zero issues]
```

Be exhaustive. Be brutal. If something looks wrong, say so even if you're not 100% certain —
flag it as a suspicion. The goal is zero silent failures in the cache before public release.
