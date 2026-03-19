---
name: "llGetSunDirection"
category: "function"
type: "function"
language: "LSL"
description: "Returns a normalized vector to the current sun position at the location of object containing the script. llGetSunDirection is the vector to the parcel's sun, llGetRegionSunDirection is the vector to region's sun. If there is no custom environment set for the current parcel llGetSunDirection returns "
signature: "vector llGetSunDirection()"
return_type: "vector"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetSunDirection'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgetsundirection"]
---

Returns a normalized vector to the current sun position at the location of object containing the script. llGetSunDirection is the vector to the parcel's sun, llGetRegionSunDirection is the vector to region's sun. If there is no custom environment set for the current parcel llGetSunDirection returns the direction to the region's sun. These functions are altitude aware.


## Signature

```lsl
vector llGetSunDirection();
```


## Return Value

Returns `vector`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetSunDirection)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetSunDirection) — scraped 2026-03-18_

Returns a normalized vector to the current sun position at the location of object containing the script. llGetSunDirection is the vector to the parcel's sun, llGetRegionSunDirection is the vector to region's sun. If there is no custom environment set for the current parcel llGetSunDirection returns the direction to the region's sun. These functions are altitude aware.Returns a vector

## See Also

### Functions

- **llGetEnvironment** — Newer function that consolidates many environment-based settings.
- llGetDayLength
- llGetDayOffset
- llGetMoonDirection
- llGetMoonRotation
- llGetSunDirection
- llGetSunRotation
- llGetRegionDayLength
- llGetRegionDayOffset
- llGetRegionMoonDirection
- llGetRegionMoonRotation
- llGetRegionSunDirection
- llGetRegionSunRotation

<!-- /wiki-source -->
