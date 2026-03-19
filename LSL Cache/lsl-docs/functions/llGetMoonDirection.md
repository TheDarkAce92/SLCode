---
name: "llGetMoonDirection"
category: "function"
type: "function"
language: "LSL"
description: "Returns a normalized vector to the current moon position at the location of object containing the script. llGetMoonDirection is the vector to the parcel's moon, llGetRegionMoonDirection is the vector to region's moon. If there is no custom environment set for the current parcel llGetMoonDirection re"
signature: "vector llGetMoonDirection()"
return_type: "vector"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetMoonDirection'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
---

Returns a normalized vector to the current moon position at the location of object containing the script. llGetMoonDirection is the vector to the parcel's moon, llGetRegionMoonDirection is the vector to region's moon. If there is no custom environment set for the current parcel llGetMoonDirection returns the direction to the region's moon. These functions are altitude aware.


## Signature

```lsl
vector llGetMoonDirection();
```


## Return Value

Returns `vector`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetMoonDirection)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetMoonDirection) — scraped 2026-03-18_

Returns a normalized vector to the current moon position at the location of object containing the script. llGetMoonDirection is the vector to the parcel's moon, llGetRegionMoonDirection is the vector to region's moon. If there is no custom environment set for the current parcel llGetMoonDirection returns the direction to the region's moon. These functions are altitude aware.Returns a vector

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
