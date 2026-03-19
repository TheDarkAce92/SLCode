---
name: "llResetOtherScript"
category: "function"
type: "function"
language: "LSL"
description: 'Resets script name.

On script reset...
* The current event/function is exited without further execution or return.
* All global variables are set to their defaults
* The event queue is cleared, and recurring events are stopped.
* The default state is set as the active state
** If it has a state_ent'
signature: "void llResetOtherScript(string name)"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llResetOtherScript'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llresetotherscript"]
---

Resets script name.

On script reset...
* The current event/function is exited without further execution or return.
* All global variables are set to their defaults
* The event queue is cleared, and recurring events are stopped.
* The default state is set as the active state
** If it has a state_entry event, then it is queued.


## Signature

```lsl
void llResetOtherScript(string name);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `string` | `name` | a script in the inventory of the prim this script is in |


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llResetOtherScript)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llResetOtherScript) — scraped 2026-03-18_

Resets script name.

## Caveats

- If name is missing from the prim's inventory   or it is not a script then an error is shouted on DEBUG_CHANNEL.
- If the script is not running, this call has no effect, even after the script is set running again.
- A script can reset itself with this function (not just other scripts).

## Examples

```lsl
// the other script must be within the same prim and has to be running

default
{
    touch_start(integer num_detected)
    {
        llResetTime();
    }

    touch_end(integer num_detected)
    {
        if (llGetTime() < 3.0)
            llSay(0, "Please click & hold for at least 3.0 seconds.");
        else
            llResetOtherScript("second");
    }
}
```

## See Also

### Functions

- llResetScript
- llGetScriptState
- llSetScriptState

<!-- /wiki-source -->
