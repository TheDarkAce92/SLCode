---
name: "llSetScriptState"
category: "function"
type: "function"
language: "LSL"
description: "Set the running state of the script name."
signature: "void llSetScriptState(string name, integer run)"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llSetScriptState'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llsetscriptstate"]
---

Set the running state of the script name.


## Signature

```lsl
void llSetScriptState(string name, integer run);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `string` | `name` | a script in the inventory of the prim this script is in |
| `integer (boolean)` | `running` | boolean, if TRUE[1] the script will be enabled, if FALSE the script will be disabled |


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llSetScriptState)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llSetScriptState) — scraped 2026-03-18_

Set the running state of the script name.

## Caveats

- If name is missing from the prim's inventory   or it is not a script then an error is shouted on DEBUG_CHANNEL.
- Cannot be used to restart a script that has encountered a run-time error.
- Cannot be used to start a script that has been added via llGiveInventory.  Scripts sent via llRemoteLoadScriptPin, and which have the running state set FALSE by that command, may be started.
- The script appears to stop when its time slice ends, not sooner. If a script tries to stop itself then some LSL code following the llSetScriptState call may be executed before the script stops.
- If a script is paused by llSetScriptState and is then either re-rezzed, in a region during a restart, or moved into a different region, the script's memory is reset.

## Examples

```lsl
//Stops the Script, at some non-deterministic time later, until invoked with TRUE, in another script
llSetScriptState(llGetScriptName(),FALSE);
// Stall until end of time slice
llSleep(0.1);
```

```lsl
//Starts Another Script
llSetScriptState("somescript",TRUE);
```

## See Also

### Functions

- llGetScriptState
- llResetOtherScript

<!-- /wiki-source -->
