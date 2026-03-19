---
name: "LSL Script Limits"
category: "script-limits"
type: "reference"
language: "LSL"
description: "Hard limits for LSL scripts: memory, event queue depth, string/list sizes, prim limits, and region capacity"
wiki_url: "https://wiki.secondlife.com/wiki/LSL_Script_Limits"
first_fetched: "2026-03-09"
last_updated: "2026-03-09"
---

# LSL Script Limits

## Memory Limits

| Limit | Mono VM | LSO VM |
|-------|---------|--------|
| Compiled script size (bytecode) | 64 KB | 16 KB |
| Heap + stack memory | 256 KB | 16 KB |
| Default memory allocation (new scripts) | 64 KB | 16 KB |
| Minimum memory allocation | ~4–16 KB (via `llSetMemoryLimit`) | 16 KB (fixed) |
| Maximum memory allocation | 64 KB | 16 KB (fixed) |

**Note:** Mono scripts can reduce their allocation with `llSetMemoryLimit` to free server-side memory for other scripts on the same object. LSO scripts always use exactly 16 KB.

## Event Queue

| Property | Value |
|----------|-------|
| Maximum queued events per script | 64 |
| Behaviour when queue full | Incoming events are silently dropped |

## String Limits

| Limit | Value |
|-------|-------|
| Maximum string length (general) | No hard limit in script memory; limited by available heap |
| `llSay` / `llShout` / `llWhisper` message | 1024 bytes |
| `llRegionSay` / `llRegionSayTo` message | 1024 bytes |
| `llOwnerSay` / `llInstantMessage` message | 1024 bytes |
| `llDialog` message | 512 bytes |
| `llSetText` floating text | 254 bytes (UTF-8) |
| `llSetObjectName` / `llSetObjectDesc` | 63 bytes / 127 bytes |
| HTTP request body | 32 KB (Mono) |
| HTTP response body (default) | 2048 bytes (configurable up to 16384) |
| Notecard line | 255 bytes |
| Inventory item name | 63 bytes |

## List Limits

| Limit | Value |
|-------|-------|
| Maximum list size | Limited by available script heap |
| `llParseString2List` separators | 8 maximum |
| `llParseString2List` spacers | 8 maximum |
| `llDialog` buttons | 12 maximum |
| `llSensor` / `llSensorRepeat` detections | 32 maximum per scan |
| `llListenRemove` simultaneous listeners | 65 per script |

## Timing Limits

| Function | Forced Delay |
|----------|-------------|
| `llSay`, `llOwnerSay`, `llRegionSay` | 0.0 seconds |
| `llDialog` | 1.0 seconds |
| `llSetPos`, `llSetRot`, `llSetScale` | 0.2 seconds |
| `llSetTimerEvent` | 0.0 seconds |
| `llSensor` | 0.0 seconds |
| `llSensorRepeat` | 0.0 seconds |
| `llRezObject` | 0.1 seconds |
| `llEmail` | 20.0 seconds |
| `llHTTPRequest` | 0.0 seconds |

## Prim and Region Limits

| Limit | Value |
|-------|-------|
| Maximum prims per object | 256 |
| Maximum scripts per prim | No hard limit (RAM-limited) |
| Maximum link distance | 54 metres (between prim centres) |
| Maximum prim scale | 64m × 64m × 64m (mesh/sculpt) |
| Minimum prim scale | 0.001m |
| Region size | 256m × 256m |
| Region maximum height | 4096m (functional) |

## Region Type Capacity Differences

| Region Type | Script Capacity | Notes |
|------------|----------------|-------|
| Full region | Standard | Full prims, full script capacity |
| Homestead | Reduced | ~¼ script CPU vs full region |
| Openspace | Very reduced | Minimal script support |

**Homestead note:** Apply conservative memory limits. Scripts competing for limited CPU may run sluggishly; prefer event-driven patterns over polling loops.

## Chat Throttles

| Channel | Throttle |
|---------|----------|
| PUBLIC_CHANNEL (0) | < 200 messages per 10 seconds per owner per region |
| DEBUG_CHANNEL | < 200 messages per 10 seconds per owner per region |
| All other channels | No throttle |

## HTTP Throttles

| Scope | Limit |
|-------|-------|
| Per object | 25 requests per 20 seconds |
| Per owner | 1000 requests per 20 seconds |
| HTTP 5xx errors | 5 per 60 seconds per script |

## Memory Management

```lsl
// Check and instrument memory usage
default
{
    state_entry()
    {
        llOwnerSay("Memory limit: " + (string)llGetMemoryLimit());
        llOwnerSay("Used memory:  " + (string)llGetUsedMemory());
        llOwnerSay("Free memory:  " + (string)llGetFreeMemory());
    }
}
```

```lsl
// Reduce memory footprint (Mono only)
// Call after all global variables and data structures are initialised
llSetMemoryLimit(llGetUsedMemory() + 4096);  // headroom for runtime use
```

Warning threshold: Consider displaying a warning when `llGetUsedMemory() / llGetMemoryLimit() > 0.8` (80% of limit).

## See Also

- `llGetMemoryLimit` — current memory allocation
- `llGetUsedMemory` — current memory consumption
- `llGetFreeMemory` — bytes remaining before limit
- `llSetMemoryLimit` — adjust memory allocation (Mono only)
- `llGetSPMaxMemory` — peak memory usage since profiling start
- `llScriptProfiler` — memory profiling
