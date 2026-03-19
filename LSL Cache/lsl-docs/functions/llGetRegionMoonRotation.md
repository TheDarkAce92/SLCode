---
name: "llGetRegionMoonRotation"
category: "function"
type: "function"
language: "LSL"
description: "Return the rotation applied to the moon for the region at the location of the object containing the script. These function are altitude aware and so will pick up the moon for their current track. llGetRegionMoonRotation returns the rotation applied at the region level, llGetMoonRotation does the sam"
signature: "rotation llGetRegionMoonRotation()"
return_type: "rotation"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetRegionMoonRotation'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
---

Return the rotation applied to the moon for the region at the location of the object containing the script. These function are altitude aware and so will pick up the moon for their current track. llGetRegionMoonRotation returns the rotation applied at the region level, llGetMoonRotation does the same for the parcel. If there is no custom environment applied to parcel llGetMoonRotation returns the same value as llGetRegionMoonRotation.


## Signature

```lsl
rotation llGetRegionMoonRotation();
```


## Return Value

Returns `rotation`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetRegionMoonRotation)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetRegionMoonRotation) — scraped 2026-03-18_

Return the rotation applied to the moon for the region at the location of the object containing the script. These function are altitude aware and so will pick up the moon for their current track. llGetRegionMoonRotation returns the rotation applied at the region level, llGetMoonRotation does the same for the parcel. If there is no custom environment applied to parcel llGetMoonRotation returns the same value as llGetRegionMoonRotation.Returns a rotation

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
