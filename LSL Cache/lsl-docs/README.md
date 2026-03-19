# LSL Documentation Cache
_Last updated: 2026-03-19_
_Total documents: 586_

## Summary by Category

| Category | Count |
|----------|-------|
| Functions | 520 |
| Events | 43 |
| Constants (groups) | 7 |
| Tutorials | 11 |
| Reference (types, operators, flow-control, script-limits, style-guide) | 5 |
| **Total** | **586** |

---

## Reference Documents

| Path | Category | Description |
|------|----------|-------------|
| `types.md` | types | All LSL data types: integer, float, string, key, vector, rotation, list â€” ranges, literals, casting, pass-by-value |
| `operators.md` | operators | All LSL operators with precedence table, type rules, caveats about non-short-circuit evaluation |
| `flow-control.md` | flow-control | if/else, while, do-while, for, jump/@label, return, state changes |
| `script-limits.md` | script-limits | Memory limits, event queue depth, string/list/prim limits, throttles, Mono vs LSO |
| `style-guide.md` | style-guide | Indentation styles, naming conventions, commenting, code organisation |

---

## Functions (`functions/`)

| File | Description |
|------|-------------|
| `llDetectedKey.md` | UUID of Nth detected entity in detection events |
| `llDetectedName.md` | Name of Nth detected entity in detection events |
| `llDialog.md` | Show dialog box with buttons to avatar; 1s delay |
| `llEuler2Rot.md` | Convert Euler angles (radians) to rotation quaternion |
| `llGetEnv.md` | Query region environment data (sim_version, chat_range, etc.) |
| `llGetKey.md` | UUID of the prim containing this script |
| `llGetListLength.md` | Count elements in a list |
| `llGetOwner.md` | UUID of the object's owner |
| `llGetPos.md` | Position in region coordinates |
| `llGetRegionName.md` | Name of the current region |
| `llGetSubString.md` | Extract substring by index range (supports negative indexing) |
| `llGetTime.md` | Elapsed seconds since script start or last llResetTime |
| `llGetUsedMemory.md` | Bytes of memory currently used by the script |
| `llHTTPRequest.md` | Send HTTP/HTTPS request; triggers http_response event |
| `llInstantMessage.md` | Private IM to avatar by UUID; 2s delay |
| `llList2String.md` | Get list element at index as string |
| `llListFindList.md` | Search for sublist (needle) in list (haystack); returns index or -1 |
| `llListen.md` | Register a chat listener with filters; returns handle |
| `llListenRemove.md` | Remove a listener by handle |
| `llMessageLinked.md` | Send message to scripts in linked prims via link_message event |
| `llOwnerSay.md` | Send chat to owner only (no range limit within region) |
| `llParseString2List.md` | Split string into list using separators and spacers |
| `llRegionSay.md` | Region-wide chat on non-zero channel |
| `llResetScript.md` | Reset script to initial state, clear all variables and listeners |
| `llRound.md` | Round float to nearest integer |
| `llSay.md` | Public chat within 20m |
| `llSetMemoryLimit.md` | Adjust script memory allocation (Mono only) |
| `llSetPos.md` | Move prim to position (non-physics, 10m cap, 0.2s delay) |
| `llSetPrimitiveParams.md` | Set multiple prim parameters with PRIM_* constants |
| `llSetText.md` | Display hovering text above prim |
| `llSetTimerEvent.md` | Start/stop repeating timer event |
| `llShout.md` | Public chat within 100m |
| `llSleep.md` | Pause script execution for N seconds |
| `llStringLength.md` | Character count of a string |
| `llSubStringIndex.md` | Find position of substring in string; returns index or -1 |
| `llToLower.md` | Convert string to lowercase |
| `llToUpper.md` | Convert string to uppercase |
| `llVecNorm.md` | Normalise a vector to unit length (magnitude 1.0) |
| `llWhisper.md` | Public chat within 10m |

---

## Events (`events/`)

| File | Description |
|------|-------------|
| `attach.md` | Object attached to or detached from avatar |
| `changed.md` | Object property changed (uses CHANGED_* bitmask) |
| `collision_start.md` | Object begins colliding with another object or avatar |
| `dataserver.md` | Asynchronous data arrived (llGetNotecardLine, llRequestAgentData, etc.) |
| `http_response.md` | HTTP response received for llHTTPRequest |
| `link_message.md` | Message received from llMessageLinked in a linked prim |
| `listen.md` | Chat message matching an llListen filter was received |
| `money.md` | Avatar paid the object |
| `on_rez.md` | Object was rezzed or attachment owner logged in |
| `run_time_permissions.md` | Avatar granted or denied permissions (PERMISSION_* flags) |
| `sensor.md` | llSensor or llSensorRepeat detected objects or avatars |
| `state_entry.md` | Script entered a state (start, reset, or state change) |
| `state_exit.md` | Script leaving current state (before state change completes) |
| `timer.md` | Timer interval fired (set by llSetTimerEvent) |
| `touch.md` | Avatar is holding a click/touch on the prim (continuous) |
| `touch_end.md` | Avatar released a click/touch |
| `touch_start.md` | Avatar began clicking/touching the prim |

---

## Constants (`constants/`)

| File | Description |
|------|-------------|
| `CHANGED.md` | CHANGED_* bitmask constants for the changed event |
| `HTTP.md` | HTTP_* constants for llHTTPRequest configuration and http_response metadata |
| `JSON.md` | JSON_* type and modifier constants for JSON functions |
| `LINK.md` | LINK_ROOT, LINK_SET, LINK_ALL_OTHERS, LINK_ALL_CHILDREN, LINK_THIS |
| `MISC.md` | TRUE, FALSE, NULL_KEY, ZERO_VECTOR, ZERO_ROTATION, math constants, channel constants, INVENTORY_* |
| `PERMISSION.md` | PERMISSION_* constants for llRequestPermissions and run_time_permissions |
| `STATUS.md` | STATUS_* constants for llSetStatus and llGetStatus |

---

## Tutorials (`tutorials/`)

| File | Description |
|------|-------------|
| `a-basic-lsl-tutorial.md` | 10-task beginner tutorial: chat, colours, text, transparency, textures, conditionals, listeners, movement, physics |
| `dialog-menus.md` | Step-by-step dialog menu system with llDialog, llListen, and timeout cleanup |
| `hello-avatar.md` | The default LSL script â€” Hello World equivalent |
| `lovebridge-api.md` | LoveBridge Scripting API v2.9 (private reference) |
| `profile-picture-retrieval.md` | Profile picture retrieval via web profile HTML |

---

## Notes

- All function files include: signature, parameter types and descriptions, return type, energy cost, forced delay/sleep time, description, caveats, and code examples.
- All event files include: event signature, parameter types and descriptions, when triggered, caveats, and code examples.
- All constant files include: constant values (decimal and hex), descriptions, and usage examples.
- Cached from the Second Life wiki: https://wiki.secondlife.com/wiki/LSL_Portal
- This cache is shared across all LSL projects on this machine.
