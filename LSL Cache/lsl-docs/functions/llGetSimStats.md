---
name: "llGetSimStats"
category: "function"
type: "function"
language: "LSL"
description: "Returns a float that is the requested statistic."
signature: "float llGetSimStats(integer stat_type)"
return_type: "float"
sleep_time: ""
energy_cost: ""
wiki_url: 'https://wiki.secondlife.com/wiki/llGetSimStats'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgetsimstats"]
---

Returns a float that is the requested statistic.


## Signature

```lsl
float llGetSimStats(integer stat_type);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `integer` | `stat_type` | SIM_STAT_* flag |


## Return Value

Returns `float`.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetSimStats)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetSimStats) — scraped 2026-03-18_

Returns a float that is the requested statistic.

## Examples

```lsl
default
{
    touch_start(integer num_detected)
    {
        float pct_chars_stepped = llGetSimStats(SIM_STAT_PCT_CHARS_STEPPED);
        llSay(0,
            "The percentage of pathfinding characters updated each frame was "
            + (string)pct_chars_stepped + "averaged over the last minute. The "
            + "value corresponds to the 'Characters Updated' stat in the "
            + "viewer's Statistics Bar. ");
    }
}
```

## See Also

### Functions

- **llAbs** — integer

<!-- /wiki-source -->
