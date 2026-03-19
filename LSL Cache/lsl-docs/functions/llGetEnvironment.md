---
name: "llGetEnvironment"
category: "function"
type: "function"
language: "LSL"
description: 'Returns a list containing the current environment values for the parcel or region as a list of attributes. Takes a list of attributes to retrieve in params and returns them in the order requested.

If an unknown rule is encountered in the parameter list an error is sent to the debug channel.'
signature: "list llGetEnvironment(vector pos, list params)"
return_type: "list"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetEnvironment'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
---

Returns a list containing the current environment values for the parcel or region as a list of attributes. Takes a list of attributes to retrieve in params and returns them in the order requested.

If an unknown rule is encountered in the parameter list an error is sent to the debug channel.


## Signature

```lsl
list llGetEnvironment(vector pos, list params);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `vector` | `pos` | A position in region coordinates. X and Y are in region coordinates and determine the parcel. If X and Y are both -1, the environment for the region is inspected. Z is the altitude in the region and determines which sky track is accessed. |
| `list` | `params` | A list of parameters to retrieve from the current environment. |


## Return Value

Returns `list`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetEnvironment)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetEnvironment) — scraped 2026-03-18_

Returns a list containing the current environment values for the parcel or region as a list of attributes. Takes a list of attributes to retrieve in params and returns them in the order requested.

## Caveats

- If the script can not run in the requested parcel, this function returns an empty list and issues a warning in the debug channel.
- SKY_LIGHT's param *fade_color* does not return a clamped value, meaning an unusually bright scene will cause it to return an out-of-bounds color. (This can be fixed by clamping the value manually, but this should really return a clamped value).

## Examples

```lsl
default
{
    touch_start(integer total_number)
    {
        list environment = llGetEnvironment(llGetPos(), [SKY_TRACKS, SKY_AMBIENT, SKY_CLOUDS]);
        llOwnerSay(llDumpList2String(environment, ", "));
    }
}
```

## See Also

### Functions

- llReplaceAgentEnvironment
- llSetAgentEnvironment
- llGetSunDirection
- llGetRegionSunDirection
- llGetMoonDirection
- llGetRegionMoonDirection
- llGetSunRotation
- llGetRegionSunRotation
- llGetMoonRotation
- llGetRegionMoonRotation
- llGetDayLength
- llGetRegionDayLength
- llGetDayOffset
- llGetRegionDayOffset
- llGetTimeOfDay
- llGetRegionTimeOfDay

### Articles

- Color in LSL
- Color in LSL

<!-- /wiki-source -->
