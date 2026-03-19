---
name: "llScriptProfiler"
category: "function"
type: "function"
language: "LSL"
description: "Enables or disables the scripts profiling state."
signature: "void llScriptProfiler(integer flags)"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llScriptProfiler'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llscriptprofiler"]
---

Enables or disables the scripts profiling state.


## Signature

```lsl
void llScriptProfiler(integer flags);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `integer` | `flags` | PROFILE_* flags |


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llScriptProfiler)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llScriptProfiler) — scraped 2026-03-18_

Enables or disables the scripts profiling state.

## Caveats

- Scripts compiled to LSO can not be profiled for memory use.
- The profile state will reset to PROFILE_NONE if:

  - the object the script is in is de-rezed, rezed or changes regions (via region cross or teleport)
  - the region that object with the script is in shuts down or restarts
  - if the script is reset or taken to or from inventory
- There is up to 100x performance penalty to the script being profiled (but not the region).

## Examples

Calling llScriptProfiler can look like this:

```lsl
llScriptProfiler(PROFILE_SCRIPT_MEMORY);
my_func();
llScriptProfiler(PROFILE_NONE);
llOwnerSay("This script used at most " + (string)llGetSPMaxMemory() + " bytes of memory during my_func.");
```

This is how it looks in a script as an example:

```lsl
// need to run something for the profile to register...
workerMethod()
{
    float mathNumber = 3 * PI + 3 * llSin( PI );
    llSetText( "Answer: " + (string)mathNumber, <1, 0, 0>, 1.0 );
}

default
{
    state_entry()
    {
        llSetMemoryLimit( 5000 ); // set the memory limit

        // call up the profiler, execute a method, stop profiler
        llScriptProfiler( PROFILE_SCRIPT_MEMORY );
        workerMethod();
        llScriptProfiler( PROFILE_NONE );

        // display memory usage...
        llSay(0, "Memory used: " + (string)llGetSPMaxMemory() + " bytes, total memory: " +
            (string)llGetMemoryLimit() + " bytes." );
    }
}

// outputs
// Object: Memory used: 4968 bytes, total memory: 5000 bytes.
```

## See Also

### Functions

- llGetSPMaxMemory
- llGetMemoryLimit
- llSetMemoryLimit

<!-- /wiki-source -->
