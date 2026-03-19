---
name: "llGetStartParameter"
category: "function"
type: "function"
language: "LSL"
description: 'Returns an integer that is the script start/rez parameter.

* If the script was loaded with llRemoteLoadScriptPin then that start parameter is returned.
* If the containing object was rezzed by llRezObject or llRezAtRoot then the return is the on_rez parameter.
* If the containing object was manuall'
signature: "integer llGetStartParameter()"
return_type: "integer"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetStartParameter'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgetstartparameter"]
---

Returns an integer that is the script start/rez parameter.

* If the script was loaded with llRemoteLoadScriptPin then that start parameter is returned.
* If the containing object was rezzed by llRezObject or llRezAtRoot then the return is the on_rez parameter.
* If the containing object was manually rezzed, by dragging from inventory, the start parameter is 0.


## Signature

```lsl
integer llGetStartParameter();
```


## Return Value

Returns `integer`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetStartParameter)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetStartParameter) — scraped 2026-03-18_

Returns an integer that is the script start/rez parameter.

## Caveats

- The start parameter does not survive region restarts ([SVC-2251](https://jira.secondlife.com/browse/SVC-2251)) or region change ([SVC-3258](https://jira.secondlife.com/browse/SVC-3258), crossing or teleport).
- If the script is reset (using llResetScript or other means), the start parameter is set to 0.

## Examples

```lsl
default
{
    on_rez(integer param)
    {
        llOwnerSay("rezzed with the number " + (string)param);
    }
    state_entry()
    {
        integer i = llGetStartParameter();
        if (i)
        {
            llOwnerSay("I was given the number " + (string)i + " when I was rezzed");
        }
        else
        {
            llOwnerSay("rezzed from inventory (or rezzed/loaded with 0)");
        }
    }
}
```

## See Also

### Events

- on_rez

### Functions

- **llRemoteLoadScriptPin** — Used to load a script into a remote prim
- **llRezObject** — Used to rez an object at the center of mass
- **llRezAtRoot** — Used to rez an object at the root

<!-- /wiki-source -->
