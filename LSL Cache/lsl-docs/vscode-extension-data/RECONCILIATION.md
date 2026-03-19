# Cross-Source Reconciliation Notes
_Last updated: 2026-03-09_

## Source Summary

| Source | Entries | Notes |
|---|---|---|
| jyaoma/functions.json | 502 | ll* functions with signatures |
| jyaoma/constants.json | 664 | Constants with types and values |
| jyaoma/events.json | 43 | Event handlers with signatures |
| jyaoma/snippets.json | 91 | VS Code-format code snippets |
| kwdb/kwdb.xml | 498 KB, ~5000+ entries (XML) | Master keyword database — **Note: initial fetch on 2026-03-09 failed (stored "404: Not Found"). Re-fetched 2026-03-09 from correct path `database/kwdb.xml`. Now valid.** |
| pyoptimizer/fndata.txt | (text — not counted) | Behavioural flags per function |
| makopo/tooltipdata.json | 1746 | Functions + constants with HTML descriptions |
| buildersbrewery/lsl.json | 1178 | Per-entry constant/function records (JSONC format, nested under "lsl" key) |
| buildersbrewery/LSL.tmLanguage.json | (grammar) | TextMate grammar for syntax highlighting |

**Note on buildersbrewery format:** `lsl.json` uses JSONC (JSON with comments, `//` style). Entries are individual constants and functions, each with `prefix`, `body`, and `description` — not VS Code multi-line snippets. Structure differs significantly from jyaoma/snippets.json.

---

## Discrepancies Found

| Function/Constant | Issue | Sources Affected | Resolution |
|---|---|---|---|
| llClearExperiencePermissions | Present in makopo, absent from jyaoma/functions.json | makopo vs jyaoma | Experience API function — kwdb is ground truth. Verify in kwdb.xml. |
| llGetExperienceList | Present in makopo, absent from jyaoma/functions.json | makopo vs jyaoma | Experience API function — kwdb is ground truth. Verify in kwdb.xml. |
| llGetRegionTimeOfDay | Present in makopo, absent from jyaoma/functions.json | makopo vs jyaoma | Present in makopo; may be missing from jyaoma due to version lag. Verify against SL wiki. |
| Return types (general) | jyaoma functions.json `return` field is null for many entries | jyaoma | Use makopo tooltip HTML or kwdb for authoritative return types when needed. |
| Snippet coverage gap | jyaoma/snippets.json has 91 multi-line code snippets; buildersbrewery/lsl.json has 1178 single-entry records (constants/functions) | jyaoma, buildersbrewery | These serve different purposes — jyaoma snippets are code templates, bb entries are completion tokens. Not directly mergeable without transformation. |

---

## Source Priority (reference)

When data conflicts, prefer sources in this order:
1. `kwdb.xml` — community master, most rigorously maintained
2. SL wiki docs (`~/.lsl-cache/lsl-docs/functions/`) — official reference
3. `jyaoma` JSON — practical, VS Code-native
4. `pyoptimizer` fndata — authoritative on behavioural properties
5. `makopo` tooltipdata — good descriptions, may lag on new additions
6. `buildersbrewery` grammar — best for coverage checking, weaker on metadata

---

## Append Log

| Date | Event |
|---|---|
| 2026-03-09 | Initial reconciliation created. All 5 sources fetched and counted. 3 makopo-only ll* functions identified. Return type gap in jyaoma noted. |
| 2026-03-09 | kwdb.xml re-fetched from correct path (`database/kwdb.xml`). Original fetch used wrong URL and stored "404: Not Found" (14 bytes). File is now valid (498 KB). Discrepancy table updated. |
| 2026-03-09 | Sanity check: llClearExperiencePermissions and llGetExperienceList confirmed present in kwdb.xml (Experience API functions). llGetRegionTimeOfDay also present in kwdb. All 3 jyaoma gaps confirmed. |
