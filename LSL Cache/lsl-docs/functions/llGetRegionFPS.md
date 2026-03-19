---
name: "llGetRegionFPS"
category: "function"
type: "function"
language: "LSL"
description: "Returns a float that is the mean region frames per second."
signature: "float llGetRegionFPS()"
return_type: "float"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetRegionFPS'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgetregionfps"]
---

Returns a float that is the mean region frames per second.


## Signature

```lsl
float llGetRegionFPS();
```


## Return Value

Returns `float`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetRegionFPS)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetRegionFPS) — scraped 2026-03-18_

Returns a float that is the mean region frames per second.

## Caveats

- Region FPS is currently capped at 45.0 frames per second, so this function never returns greater than 45.0

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
              "\nTIME DIALATION : " + (string)llGetRegionTimeDilation() +
              "\n    REGION FPS : " + (string)llGetRegionFPS(),
            <0,1,0>, 1.0);
    }
}
```

## See Also

### Functions

- **llGetSimulatorHostname** — Gets the hostname of the server
- **llGetRegionTimeDilation** — Gets the region time dilation

<!-- /wiki-source -->
