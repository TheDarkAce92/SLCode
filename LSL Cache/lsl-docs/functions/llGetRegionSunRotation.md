---
name: "llGetRegionSunRotation"
category: "function"
type: "function"
language: "LSL"
description: "Return the rotation applied to the sun for the region at the location of the object containing the script. These functions are altitude aware and so will pick up the sun for their current track. llGetRegionSunRotation returns the rotation applied at the region level, llGetSunRotation does the same f"
signature: "rotation llGetRegionSunRotation()"
return_type: "rotation"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetRegionSunRotation'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
---

Return the rotation applied to the sun for the region at the location of the object containing the script. These functions are altitude aware and so will pick up the sun for their current track. llGetRegionSunRotation returns the rotation applied at the region level, llGetSunRotation does the same for the parcel. If there is no custom environment applied to parcel llGetSunRotation returns the same value as llGetRegionSunRotation.


## Signature

```lsl
rotation llGetRegionSunRotation();
```


## Return Value

Returns `rotation`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetRegionSunRotation)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetRegionSunRotation) — scraped 2026-03-18_

Return the rotation applied to the sun for the region at the location of the object containing the script. These functions are altitude aware and so will pick up the sun for their current track. llGetRegionSunRotation returns the rotation applied at the region level, llGetSunRotation does the same for the parcel. If there is no custom environment applied to parcel llGetSunRotation returns the same value as llGetRegionSunRotation.Returns a rotation

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
