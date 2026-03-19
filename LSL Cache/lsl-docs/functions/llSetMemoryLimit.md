---
name: "llSetMemoryLimit"
category: "function"
type: "function"
language: "LSL"
description: "Requests a specific memory limit for the script (Mono only); reduces server memory footprint"
wiki_url: "https://wiki.secondlife.com/wiki/llSetMemoryLimit"
first_fetched: "2026-03-09"
last_updated: "2026-03-09"
signature: "integer llSetMemoryLimit(integer limit)"
parameters:
  - name: "limit"
    type: "integer"
    description: "Requested memory limit in bytes (max 65536 / 64 KB)"
return_type: "integer"
energy_cost: "0.0"
sleep_time: "0.0"
patterns: ["llsetmemorylimit"]
deprecated: "false"
---

# llSetMemoryLimit

```lsl
integer llSetMemoryLimit(integer limit)
```

Requests `limit` bytes to be reserved for the script. Returns TRUE if successful, FALSE if not.

## Return Value

`integer` — TRUE (1) if limit was set; FALSE (0) if limit was below current usage or above maximum.

## Behaviour by VM

| VM | Behaviour |
|----|-----------|
| Mono | Adjusts memory allocation; max 64 KB; cannot set below current usage |
| LSO | No effect — LSO always uses exactly 16 KB |

## Caveats

- Setting a limit too small is silently ignored (returns FALSE).
- Maximum limit is 65536 bytes (64 KB).
- Best called after all global variables and data structures are fully initialised.
- Reducing the limit frees server-side resources for other scripts in the same object.

## Example

```lsl
default
{
    state_entry()
    {
        // Initialise everything first...
        llSleep(0.01);

        // Then tighten the memory limit
        integer used = llGetUsedMemory();
        integer newLimit = used + 8192;  // 8 KB headroom
        if (llSetMemoryLimit(newLimit))
            llOwnerSay("Memory limit set to " + (string)newLimit + " bytes");
        else
            llOwnerSay("Failed to set memory limit");
    }
}
```

## See Also

- `llGetMemoryLimit` — get the current limit
- `llGetUsedMemory` — get current usage
- `llGetFreeMemory` — remaining memory
- `llGetSPMaxMemory` — peak memory usage


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llSetMemoryLimit) — scraped 2026-03-18_

Request limit bytes to be reserved for this script.Returns the boolean (an integer) TRUE if the memory limit was successfully set (or FALSE if not).

## Caveats

Mono
When ***n*** is too small, llSetMemoryLimit(***n***) is ignored and the memory limit is not changed

## Examples

```lsl
// Memory-walkthrough by Daemonika Nightfire (daemonika.nightfire)

integer limit = 20000; // <- bytes

Test()
{
    llSetText("Limited Memory " + (string)llGetMemoryLimit() +
              "\nUsed Memory " + (string)llGetUsedMemory() +
              "\nFree Memory " + (string)llGetFreeMemory(),<1,1,1>,1);
}

default
{
    state_entry()
    {
        llSetMemoryLimit(limit);

        llScriptProfiler(PROFILE_SCRIPT_MEMORY);
        Test();
        llScriptProfiler(PROFILE_NONE);

        llSay(0,"This script used at most " + (string)llGetSPMaxMemory() + " bytes of memory during Test.");
    }
}

// Result:

// Floating Text:
// Limited Memory 20000
// Used Memory 4972
// Free Memory 15100

// Chat:
// [05:11] Object: This script used at most 4972 bytes of memory during Test.
```

## See Also

### Functions

- llScriptProfiler
- llGetSPMaxMemory
- llGetMemoryLimit
- llGetFreeMemory
- llGetUsedMemory
- llGetObjectDetails

<!-- /wiki-source -->
