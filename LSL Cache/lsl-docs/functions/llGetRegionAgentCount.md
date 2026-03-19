---
name: "llGetRegionAgentCount"
category: "function"
type: "function"
language: "LSL"
description: "Returns an integer that is the number of avatars in the region."
signature: "integer llGetRegionAgentCount()"
return_type: "integer"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetRegionAgentCount'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgetregionagentcount"]
---

Returns an integer that is the number of avatars in the region.


## Signature

```lsl
integer llGetRegionAgentCount();
```


## Return Value

Returns `integer`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetRegionAgentCount)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetRegionAgentCount) — scraped 2026-03-18_

Returns an integer that is the number of avatars in the region.

## Caveats

- The value returned by this function is technically the average number of agents who were in the region for the past second, rounded to the nearest integer.  This means that there is a slight (<1 second) delay  in agent count when an agent enters or exits a region.

## Examples

```lsl
default
{
    touch_start(integer num_detected)
    {
        integer numberOfAvatarsInSim = llGetRegionAgentCount();
        llSay(0, "There are currently "
            + (string) numberOfAvatarsInSim + " avatars in this sim.");
    }
}
```

## See Also

### Functions

- llGetAgentList
- llGetRegionFPS
- llGetRegionTimeDilation

<!-- /wiki-source -->
