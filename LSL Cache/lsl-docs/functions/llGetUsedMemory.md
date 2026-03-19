---
name: "llGetUsedMemory"
category: "function"
type: "function"
language: "LSL"
description: "Returns the number of bytes of memory currently in use by the script"
wiki_url: "https://wiki.secondlife.com/wiki/llGetUsedMemory"
first_fetched: "2026-03-09"
last_updated: "2026-03-09"
signature: "integer llGetUsedMemory()"
parameters: []
return_type: "integer"
energy_cost: "10.0"
sleep_time: "0.0"
patterns: ["llgetusedmemory"]
deprecated: "false"
---

# llGetUsedMemory

```lsl
integer llGetUsedMemory()
```

Returns the number of bytes of memory currently in use by the script.

## Return Value

`integer` — bytes of memory in use.

## Behaviour by VM

| VM | Behaviour |
|----|-----------|
| Mono | Returns actual bytes currently reachable on the heap (unreachable objects awaiting GC not counted) |
| LSO | Always returns 16384 (16 KiB) regardless of actual usage |

## Caveats

- Memory values update at server frame boundaries. For stable readings, call after `llSleep(0.01)` to wait one frame.
- Does not require `llScriptProfiler` to be active.

## Example

```lsl
default
{
    state_entry()
    {
        llSleep(0.01);  // wait for accurate reading
        llOwnerSay("Memory limit: " + (string)llGetMemoryLimit());
        llOwnerSay("Used memory:  " + (string)llGetUsedMemory());
        llOwnerSay("Free memory:  " + (string)llGetFreeMemory());
    }
}
```

## See Also

- `llGetMemoryLimit` — current memory allocation
- `llGetFreeMemory` — bytes remaining (limit − used)
- `llSetMemoryLimit` — adjust memory allocation (Mono only)
- `llScriptProfiler` — detailed memory profiling


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetUsedMemory) — scraped 2026-03-18_

Returns the integer of the number of bytes of memory currently in use by the script.

## Caveats

- Scripts compiled to LSO always report 16KB memory used.
- This can be called at any time and does **not** require llScriptProfiler

## Examples

Calling llGetUsedMemory can look like this:

```lsl
integer used_memory = llGetUsedMemory();
llOwnerSay((string)used_memory + " bytes of memory currently used.");
```

## Notes

The amount of used memory is updated only at the start of a server frame, meaning the values from this function can fluctuate. To ensure stable values, it's possible to wait until the next frame, e.g. llSleep(0.01) before the call to llGetUsedMemory.

## See Also

### Functions

- llGetFreeMemory
- llSetMemoryLimit
- llScriptProfiler

<!-- /wiki-source -->
