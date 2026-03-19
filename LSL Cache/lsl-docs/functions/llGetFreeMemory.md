---
name: "llGetFreeMemory"
category: "function"
type: "function"
language: "LSL"
description: "Returns the integer of the number of free bytes of memory the script can use."
signature: "integer llGetFreeMemory()"
return_type: "integer"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetFreeMemory'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgetfreememory"]
---

Returns the integer of the number of free bytes of memory the script can use.


## Signature

```lsl
integer llGetFreeMemory();
```


## Return Value

Returns `integer`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetFreeMemory)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetFreeMemory) — scraped 2026-03-18_

Returns the integer of the number of free bytes of memory the script can use.

## Caveats

- The number of free bytes the Heap can use may be greater but not less.
- "*the number of free bytes of memory the script can use*" means that if a memory limit is set (via llSetMemoryLimit), this function will report the free space between the script's current memory usage and the defined memory limit, **not** the uncapped memory limit.

## Examples

Calling llGetFreeMemory can look like this:

```lsl
llOwnerSay((string)llGetFreeMemory() + " bytes of free memory available for allocation.");
```

## Notes

The amount of free memory is updated only at the start of a server frame, meaning the values from this function can fluctuate. To ensure stable values, use a single-frame sleep, e.g. llSleep(0.01) before the call to llGetFreeMemory.

## See Also

### Functions

- llGetUsedMemory
- **llScriptProfiler** — A more advanced function for analyzing script performance, and can also measure memory usage over time.
- **llSetMemoryLimit** — Define a memory limit (lower than the maximum for the appropriate VM).

### Articles

- **Stack-Heap Collision** — LSL Error

<!-- /wiki-source -->
