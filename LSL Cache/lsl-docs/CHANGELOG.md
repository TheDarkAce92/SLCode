# LSL Docs Changelog

## 2026-03-12 - Gap fill

- Added `tutorials/lovebridge-api.md` - LoveBridge Scripting API v2.9 (private reference)

## 2026-03-09 â€” Initial fetch

### Reference Documents (5 files)
- Fetched `types.md` â€” LSL data types, type casting, pass-by-value semantics
- Fetched `operators.md` â€” all operators, precedence table, type rules, non-short-circuit caveats
- Fetched `flow-control.md` â€” if/else, while, do-while, for, jump, return, state changes
- Created `script-limits.md` â€” memory limits, event queue, throttles, Mono vs LSO (compiled from wiki data + known limits)
- Fetched `style-guide.md` â€” indentation styles, naming conventions, commenting, code organisation

### Function Documents (39 files)
- `llDetectedKey.md` â€” UUID of Nth detected entity
- `llDetectedName.md` â€” name of Nth detected entity
- `llDialog.md` â€” dialog box with buttons
- `llEuler2Rot.md` â€” Euler angles to rotation
- `llGetEnv.md` â€” region environment data
- `llGetKey.md` â€” prim UUID
- `llGetListLength.md` â€” list element count
- `llGetOwner.md` â€” object owner UUID
- `llGetPos.md` â€” prim position
- `llGetRegionName.md` â€” current region name
- `llGetSubString.md` â€” extract substring
- `llGetTime.md` â€” elapsed time
- `llGetUsedMemory.md` â€” script memory usage
- `llHTTPRequest.md` â€” send HTTP request
- `llInstantMessage.md` â€” private IM to avatar
- `llList2String.md` â€” list element as string
- `llListFindList.md` â€” search list for sublist
- `llListen.md` â€” register chat listener
- `llListenRemove.md` â€” remove listener
- `llMessageLinked.md` â€” inter-script linked message
- `llOwnerSay.md` â€” message to owner only
- `llParseString2List.md` â€” split string to list
- `llRegionSay.md` â€” region-wide chat
- `llResetScript.md` â€” reset script state
- `llRound.md` â€” round float to integer
- `llSay.md` â€” public chat 20m
- `llSetMemoryLimit.md` â€” adjust memory allocation
- `llSetPos.md` â€” move prim (non-physics)
- `llSetPrimitiveParams.md` â€” set prim parameters with PRIM_* constants
- `llSetText.md` â€” floating hover text
- `llSetTimerEvent.md` â€” start/stop timer
- `llShout.md` â€” public chat 100m
- `llSleep.md` â€” pause script
- `llStringLength.md` â€” string character count
- `llSubStringIndex.md` â€” find substring position
- `llToLower.md` â€” string to lowercase
- `llToUpper.md` â€” string to uppercase
- `llVecNorm.md` â€” normalise vector
- `llWhisper.md` â€” public chat 10m

### Event Documents (17 files)
- `attach.md` â€” object attached/detached
- `changed.md` â€” object property changed
- `collision_start.md` â€” collision began
- `dataserver.md` â€” async data received
- `http_response.md` â€” HTTP response received
- `link_message.md` â€” linked prim message received
- `listen.md` â€” chat message received
- `money.md` â€” payment received
- `on_rez.md` â€” object rezzed
- `run_time_permissions.md` â€” permissions granted/denied
- `sensor.md` â€” sensor detections
- `state_entry.md` â€” entered state
- `state_exit.md` â€” leaving state
- `timer.md` â€” timer fired
- `touch.md` â€” continuous touch
- `touch_end.md` â€” touch released
- `touch_start.md` â€” touch began

### Constant Group Documents (7 files)
- `CHANGED.md` â€” CHANGED_* bitmask constants
- `HTTP.md` â€” HTTP_* request/response constants
- `JSON.md` â€” JSON_* type and modifier constants
- `LINK.md` â€” LINK_ROOT, LINK_SET, LINK_ALL_OTHERS, etc.
- `MISC.md` â€” TRUE, FALSE, NULL_KEY, ZERO_VECTOR, math constants, channels, INVENTORY_*
- `PERMISSION.md` â€” PERMISSION_* constants
- `STATUS.md` â€” STATUS_* constants

### Tutorial Documents (3 files)
- `a-basic-lsl-tutorial.md` â€” 10-task beginner tutorial
- `dialog-menus.md` â€” dialog menu system tutorial
- `hello-avatar.md` â€” Hello World / default script

### Index and Changelog
- Created `README.md` â€” full index of all 71 documents
- Created `CHANGELOG.md` â€” this file

### Total
- 5 reference docs
- 39 function docs
- 17 event docs
- 7 constant group docs
- 3 tutorial docs
- **71 total documents**

## 2026-03-10 â€” Batch gap-fill
- Fetched 0 new docs (39 total functions, 17 total events)
- Not found on wiki (489): llAbs, llAddToLandPassList, llAdjustDamage, llAcos, llAdjustSoundVolume, llAddToLandBanList, llGetObjectLinkKey, llAvatarOnSitTarget, llDumpList2String, llCloseRemoteDataChannel, llBase64ToInteger, llAxes2Rot, llAngleBetween, llBase64ToString, llGetNotecardLineSync, llAgentInExperience, llCeil, llClearCameraParams, llAxisAngle2Rot, llGetMoonRotation ... and 469 more

## 2026-03-10 â€” Synthesised gap-fill from cache data
- Generated 463 function docs from jyaoma + pyoptimizer + makopo
- Generated 26 event docs from jyaoma
- Total functions on disk: 502, events: 43

## 2026-03-10 â€” Wiki scrape merged into docs
- Scraped 5 pages from wiki.secondlife.com
- Merged wiki content (Caveats, Examples, Notes, See Also) into 5 docs
- Skipped: 0, Failed: 0

## 2026-03-10 â€” Wiki HTML scrape
- Scraped 5 pages from wiki.secondlife.com
- Merged (Caveats/Examples/Notes/See Also): 5
- Skipped: 0, Failed (not found): 0

## 2026-03-10 â€” Wiki HTML scrape
- Scraped 1 pages from wiki.secondlife.com
- Merged (Caveats/Examples/Notes/See Also): 1
- Skipped: 0, Failed (not found): 0

## 2026-03-10 â€” Wiki HTML scrape
- Scraped 1 pages from wiki.secondlife.com
- Merged (Caveats/Examples/Notes/See Also): 1
- Skipped: 0, Failed (not found): 0

## 2026-03-10 â€” Wiki HTML scrape
- Scraped 1 pages from wiki.secondlife.com
- Merged (Caveats/Examples/Notes/See Also): 1
- Skipped: 0, Failed (not found): 0

## 2026-03-10 â€” Wiki HTML scrape
- Scraped 1 pages from wiki.secondlife.com
- Merged (Caveats/Examples/Notes/See Also): 1
- Skipped: 0, Failed (not found): 0

## 2026-03-10 â€” Wiki HTML scrape
- Scraped 1 pages from wiki.secondlife.com
- Merged (Caveats/Examples/Notes/See Also): 1
- Skipped: 0, Failed (not found): 0

## 2026-03-10 â€” Wiki HTML scrape
- Scraped 545 pages from wiki.secondlife.com
- Merged (Caveats/Examples/Notes/See Also): 541
- Skipped: 4, Failed (not found): 0

## 2026-03-10 â€” LSL Library scrape
- Fetched 3 pages from Category:LSL_Library
- Saved: 3, Skipped (no code/redirect): 0, Failed: 0

## 2026-03-10 â€” LSL Library scrape
- Fetched 3 pages from Category:LSL_Library
- Saved: 3, Skipped (no code/redirect): 0, Failed: 0

## 2026-03-10 â€” LSL Library scrape
- Fetched 1 pages from Category:LSL_Library
- Saved: 1, Skipped (no code/redirect): 0, Failed: 0

## 2026-03-10 â€” LSL Library scrape
- Fetched 189 pages from Category:LSL_Library
- Saved: 186, Skipped (no code/redirect): 3, Failed: 0

## 2026-03-10 â€” LSL Library scrape
- Fetched 189 pages from Category:LSL_Library
- Saved: 0, Skipped (no code/redirect): 189, Failed: 0

## 2026-03-10 â€” LSL Library scrape
- Fetched 5 pages from Category:LSL_Library
- Saved: 5, Skipped (no code/redirect): 0, Failed: 0

## 2026-03-10 â€” LSL Library scrape
- Fetched 1 pages from Category:LSL_Library
- Saved: 1, Skipped (no code/redirect): 0, Failed: 0

## 2026-03-10 â€” LSL Library scrape
- Fetched 1 pages from Category:LSL_Library
- Saved: 1, Skipped (no code/redirect): 0, Failed: 0

## 2026-03-10 â€” LSL Library scrape
- Fetched 207 pages from Category:LSL_Library
- Saved: 18, Skipped (no code/redirect): 189, Failed: 0

## 2026-03-10 â€” LSL Library scrape (v0.1.2.0)
- Fetched 365 pages (Category:LSL_Library + LSL_Library index links)
- Saved: 147, Skipped (no code/redirect/exists): 218, Failed: 0

## 2026-03-10 â€” OSSL docs generated from local cache
- Sources: kwdb.xml (241 functions), makopo (231 entries)
- Generated 241 OSSL .md files in lsl-docs/ossl/
- Skipped 0 existing

## 2026-03-10 â€” SLua docs fetch
- Fetched 3 SLua pages, skipped 1 existing
- Saved to lsl-docs/slua/

## 2026-03-11 â€” Synthesised gap-fill from cache data
- Generated 0 function docs from jyaoma + pyoptimizer + makopo
- Generated 0 event docs from jyaoma
- Total functions on disk: 502, events: 43

## 2026-03-15 — Synthesised gap-fill from cache data
- Generated 0 function docs from jyaoma + pyoptimizer + makopo
- Generated 0 event docs from jyaoma
- Total functions on disk: 502, events: 43

## 2026-03-15 — Synthesised gap-fill from cache data
- Generated 0 function docs from jyaoma + pyoptimizer + makopo
- Generated 0 event docs from jyaoma
- Total functions on disk: 502, events: 43

## 2026-03-15 — Synthesised gap-fill from cache data
- Generated 0 function docs from jyaoma + pyoptimizer + makopo
- Generated 0 event docs from jyaoma
- Total functions on disk: 502, events: 43

## 2026-03-16 — Wiki HTML scrape
- Scraped 1 pages from wiki.secondlife.com
- Merged (Caveats/Examples/Notes/See Also): 0
- Skipped: 1, Failed (not found): 0

## 2026-03-16 — Wiki HTML scrape
- Scraped 1 pages from wiki.secondlife.com
- Merged (Caveats/Examples/Notes/See Also): 0
- Skipped: 1, Failed (not found): 0

## 2026-03-16 — Wiki HTML scrape
- Scraped 1 pages from wiki.secondlife.com
- Merged (Caveats/Examples/Notes/See Also): 0
- Skipped: 1, Failed (not found): 0

## 2026-03-16 — Wiki HTML scrape
- Scraped 1 pages from wiki.secondlife.com
- Merged (Caveats/Examples/Notes/See Also): 0
- Skipped: 1, Failed (not found): 0

## 2026-03-16 — Wiki HTML scrape
- Scraped 1 pages from wiki.secondlife.com
- Merged (Caveats/Examples/Notes/See Also): 0
- Skipped: 1, Failed (not found): 0

## 2026-03-16 — Wiki HTML scrape
- Scraped 50 pages from wiki.secondlife.com
- Merged (Caveats/Examples/Notes/See Also): 0
- Skipped: 50, Failed (not found): 0

## 2026-03-18 — OSSL docs from GitHub source
- Source: opensim/opensim IOSSL_Api.cs (265 functions)
- Threat levels from OSSL_Api.cs (125 entries)
- Cross-referenced kwdb (241 entries) + makopo (231 entries)
- Generated 34 OSSL .md files in lsl-docs/ossl/
- Skipped 231 existing

## 2026-03-18 — SLua docs fetch
- Fetched 4 SLua pages, skipped 1 existing
- Saved to lsl-docs/slua/

## 2026-03-18 — Wiki HTML scrape
- Scraped 545 pages from wiki.secondlife.com
- Merged (Caveats/Examples/Notes/See Also): 537
- Skipped: 8, Failed (not found): 0

## 2026-03-18 — LSL Library scrape (v0.1.2.0)
- Fetched 365 pages (Category:LSL_Library + LSL_Library index links)
- Saved: 353, Skipped (no code/redirect/exists): 12, Failed: 0

## 2026-03-18 — Synthesised gap-fill from cache data
- Generated 0 function docs from jyaoma + pyoptimizer + makopo
- Generated 0 event docs from jyaoma
- Total functions on disk: 502, events: 43

## 2026-03-18 — Extra library fetch
- [absolutelycraicrai] saved: 3, skipped: 0, errors: 0

## 2026-03-19 — OSSL docs from GitHub source
- Source: opensim/opensim IOSSL_Api.cs (265 functions)
- Threat levels from OSSL_Api.cs (125 entries)
- Cross-referenced kwdb (241 entries) + makopo (231 entries)
- Generated 265 OSSL .md files in lsl-docs/ossl/
- Skipped 0 existing

## 2026-03-19 — OSSL docs from GitHub source
- Source: opensim/opensim IOSSL_Api.cs (265 functions)
- Threat levels from OSSL_Api.cs (125 entries)
- Cross-referenced kwdb (241 entries) + makopo (231 entries)
- Generated 265 OSSL .md files in lsl-docs/ossl/
- Skipped 0 existing

## 2026-03-19 — OSSL docs from GitHub source
- Source: opensim/opensim IOSSL_Api.cs (265 functions)
- Threat levels from OSSL_Api.cs (125 entries)
- Cross-referenced kwdb (241 entries) + makopo (231 entries)
- Generated 265 OSSL .md files in lsl-docs/ossl/
- Skipped 0 existing

## 2026-03-19 — OSSL docs from GitHub source
- Source: opensim/opensim IOSSL_Api.cs (265 functions)
- Threat levels from OSSL_Api.cs (125 entries)
- Cross-referenced kwdb (241 entries) + makopo (231 entries)
- Generated 265 OSSL .md files in lsl-docs/ossl/
- Skipped 0 existing

## 2026-03-19 — Audit remediation
- Added 18 missing LSL function docs from local kwdb/pyoptimizer/makopo data
- Updated 275 OSSL docs with explicit descriptions and deprecated front-matter defaults
- Refreshed manifest and README summary counts

## 2026-03-19 — Audit remediation
- Added 18 missing LSL function docs from local kwdb/pyoptimizer/makopo data
- Updated 0 OSSL docs with explicit descriptions and deprecated front-matter defaults
- Refreshed manifest and README summary counts

## 2026-03-19 — Extra library fetch
- [outworldz-github] saved: 20, skipped: 0, errors: 0

## 2026-03-19 — Extra library fetch
- [outworldz-github] saved: 20, skipped: 0, errors: 0

## 2026-03-19 — Extra library fetch
- [absolutelycraicrai] saved: 5, skipped: 3, errors: 0
- [outworldz-github] saved: 1806, skipped: 9, errors: 0
- [avacon-opensim] saved: 57, skipped: 1, errors: 0
