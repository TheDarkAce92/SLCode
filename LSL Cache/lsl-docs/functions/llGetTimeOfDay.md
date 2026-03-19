---
name: "llGetTimeOfDay"
category: "function"
type: "function"
language: "LSL"
description: "Returns a float that is the time in seconds with subsecond precision since Second Life midnight (per the parcel-scoped day cycle settings) or region up-time (time since when the region was brought online/rebooted); whichever is smaller. If the parcel is configured so the sun stays in a constant posi"
signature: "float llGetTimeOfDay()"
return_type: "float"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetTimeOfDay'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgettimeofday"]
---

Returns a float that is the time in seconds with subsecond precision since Second Life midnight (per the parcel-scoped day cycle settings) or region up-time (time since when the region was brought online/rebooted); whichever is smaller. If the parcel is configured so the sun stays in a constant position, then the returned value is the region up-time.

By default (without custom environment settings), Second Life day cycles are 4 hours long (3 hours of light, 1 hour of dark). The sunrise and sunset time varies slowly.


## Signature

```lsl
float llGetTimeOfDay();
```


## Return Value

Returns `float`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetTimeOfDay)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetTimeOfDay) — scraped 2026-03-18_

Returns a float that is the time in seconds with subsecond precision since Second Life midnight (per the parcel-scoped day cycle settings) or region up-time (time since when the region was brought online/rebooted); whichever is smaller. If the parcel is configured so the sun stays in a constant position, then the returned value is the region up-time.

## Examples

```lsl
//Time will be less than 4 hours unless the sun is locked.
default
{
    touch_start(integer total_number)
    {
        float tod = llGetTimeOfDay( );
        llOwnerSay("Time since last region restart or SL midnight (based on SL 4 hour day):");
        integer hours = ((integer)tod / 3600) ;
        integer minutes = ((integer)tod / 60) - (hours * 60);
        llOwnerSay((string) tod + " seconds which is "+(string) hours+"h "+(string) minutes+"m");
    }
}
```

## See Also

### Functions

- llGetSunDirection
- llGetRegionTimeOfDay

<!-- /wiki-source -->
