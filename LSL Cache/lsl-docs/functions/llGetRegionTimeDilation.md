---
name: "llGetRegionTimeDilation"
category: "function"
type: "function"
language: "LSL"
description: 'Returns a float that is the current time dilation, the value range is [0.0, 1.0], 0.0 (full dilation) and 1.0 (no dilation).

It is used as the ratio between the change of script time to that of real world time.'
signature: "float llGetRegionTimeDilation()"
return_type: "float"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetRegionTimeDilation'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgetregiontimedilation"]
---

Returns a float that is the current time dilation, the value range is [0.0, 1.0], 0.0 (full dilation) and 1.0 (no dilation).

It is used as the ratio between the change of script time to that of real world time.


## Signature

```lsl
float llGetRegionTimeDilation();
```


## Return Value

Returns `float`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetRegionTimeDilation)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetRegionTimeDilation) — scraped 2026-03-18_

Returns a float that is the current time dilation, the value range is [0.0, 1.0], 0.0 (full dilation) and 1.0 (no dilation).[1]

## Caveats

- [Region idling](http://community.secondlife.com/t5/Second-Life-Server/Region-Idling-FAQ/m-p/1535497) lowers a region's framerate when no avatars are currently on or looking into the region. Scripts measuring time dilation with llGetRegionTimeDilation may report significant time dilation if the region is idle.

## Examples

```lsl
// The beginnings of a region-info script.
string region;
string sim;

default
{
    state_entry()
    {
        llSetTimerEvent(1.0);
    }
    timer()
    {
        string here = llGetRegionName();
        if(region != here)
        {
            sim = llGetSimulatorHostname();
            region = here;
        }
        llSetText(
                "   REGION NAME : " + region +
              "\n  SIM HOSTNAME : " + sim +
              "\n TIME DILATION : " + (string)llGetRegionTimeDilation() +
              "\n    REGION FPS : " + (string)llGetRegionFPS(),
            <0,1,0>, 1.0);
    }
}
```

## See Also

### Functions

- llGetRegionFPS
- llGetTime
- llGetAndResetTime

<!-- /wiki-source -->
