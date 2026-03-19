---
name: "llGetSPMaxMemory"
category: "function"
type: "function"
language: "LSL"
description: "Returns the integer of the most bytes used while LlScriptProfiler was last active."
signature: "integer llGetSPMaxMemory()"
return_type: "integer"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetSPMaxMemory'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgetspmaxmemory"]
---

Returns the integer of the most bytes used while LlScriptProfiler was last active.


## Signature

```lsl
integer llGetSPMaxMemory();
```


## Return Value

Returns `integer`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetSPMaxMemory)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetSPMaxMemory) — scraped 2026-03-18_

Returns the integer of the most bytes used while LlScriptProfiler was last active.

## Examples

```lsl
// need to run something for the profile to register...
ScriptRotate()
{
    llTargetOmega(<0.5, 0.7, 0.2>, 0.75, 0.75);
}

default
{
    state_entry()
    {
        llSetMemoryLimit( 5000 ); // set the memory limit

        // call up the profiler, execute a method, stop profiler
        llScriptProfiler( PROFILE_SCRIPT_MEMORY );
        ScriptRotate();
        llScriptProfiler( PROFILE_NONE );

        // display memory usage...
        llSay(0, "Memory used: " + (string)llGetSPMaxMemory() + " bytes, total memory: " +
            (string)llGetMemoryLimit() + " bytes." );
    }
}

// outputs
// Object: Memory used: 4448 bytes, total memory: 5000 bytes.
```

## See Also

### Functions

- llGetFreeMemory
- llGetUsedMemory
- llGetMemoryLimit
- llSetMemoryLimit

<!-- /wiki-source -->
