---
name: "llGetScriptState"
category: "function"
type: "function"
language: "LSL"
description: "Returns a boolean (an integer) that is TRUE if the script is running."
signature: "integer llGetScriptState(string name)"
return_type: "integer"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetScriptState'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgetscriptstate"]
---

Returns a boolean (an integer) that is TRUE if the script is running.


## Signature

```lsl
integer llGetScriptState(string name);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `string` | `script` | a script in the inventory of the prim this script is in |


## Return Value

Returns `integer`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetScriptState)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetScriptState) — scraped 2026-03-18_

Returns a boolean (an integer) that is TRUE if the script is running.

## Caveats

- If script is missing from the prim's inventory   or it is not a script then an error is shouted on DEBUG_CHANNEL.

## Examples

```lsl
default
{
    touch_start(integer num_detected)
    {
        integer numberOfScripts = llGetInventoryNumber(INVENTORY_SCRIPT);

        integer index;
        do
        {
            string scriptName = llGetInventoryName(INVENTORY_SCRIPT, index);
            integer scriptState = llGetScriptState(scriptName);

        //  default value
            string output = "FALSE";
        //  else
            if (scriptState) output = "TRUE";

            // PUBLIC_CHANNEL has the integer value 0
            llSay(PUBLIC_CHANNEL,
                "Script named '" + scriptName + "' has current script state '" + output + "'.");
        }
        while (++index < numberOfScripts);
    }
}
```

```lsl
// Monitor other scripts in the object, then report, restart or both if some have crashed
// NB: cannot distinguish a manually stopped script or restart one
integer TRY_RESTART = FALSE;
integer REPORT = TRUE;

default
{
    state_entry() {
        // monitoring rate = once per minute
        llSetTimerEvent(60);
    }

    timer() {
        integer i = llGetInventoryNumber(INVENTORY_SCRIPT);
        string script_name;
        list stopped;

        while(--i >= 0) {
            // the script will also monitor itself, but there is little reason to specifically skip
            script_name = llGetInventoryName(INVENTORY_SCRIPT, i);
            if(!llGetScriptState(script_name)) {
                if(TRY_RESTART)
                    llResetOtherScript(script_name);
                if(REPORT)
                    stopped += script_name;
            }
        }
        if(stopped) {
            string message = "The following scripts were crashed/stopped: " + llList2CSV(stopped) + ".";
            if(TRY_RESTART)
                message += " A restart was attempted.";
            llInstantMessage(llGetOwner(), message);
        }
    }
}
```

## See Also

### Functions

- llSetScriptState
- llResetOtherScript

<!-- /wiki-source -->
