---
name: "llGetRegionDayLength"
category: "function"
type: "function"
language: "LSL"
description: "Return the number of seconds in the day cycle applied to the current region. llGetDayLength returns the number of seconds for the current parcel, llGetRegionDayLength is the number of seconds in the day cycle applied to the entire region."
signature: "integer llGetRegionDayLength()"
return_type: "integer"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetRegionDayLength'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
---

Return the number of seconds in the day cycle applied to the current region. llGetDayLength returns the number of seconds for the current parcel, llGetRegionDayLength is the number of seconds in the day cycle applied to the entire region.


## Signature

```lsl
integer llGetRegionDayLength();
```


## Return Value

Returns `integer`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetRegionDayLength)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetRegionDayLength) — scraped 2026-03-18_

Return the number of seconds in the day cycle applied to the current region. llGetDayLength returns the number of seconds for the current parcel, llGetRegionDayLength is the number of seconds in the day cycle applied to the entire region.Returns an integer

## Examples

```lsl
// print the apparent time of day as HH:MM (%), just like the environment window in the viewer.
// Time of day is a fraction between 0 and 1, 0 is midnight, 0.5 is noon
string printTimeOfDay(float dayFraction) {
    integer hours = (integer)(dayFraction * 24);
    integer minutes = (integer)(dayFraction * 24 * 60) % 60;
    integer percent = (integer)(dayFraction * 100);
    return (string)hours + ":" + llGetSubString((string)(100+minutes), 1, 2) + " (" + (string)percent + "%)";
}

default {
    state_entry() {
        llSetTimerEvent(5);
    }

    timer() {
        float timeOfDay = (llGetUnixTime() + llGetRegionDayOffset()) % llGetRegionDayLength() * 1.0 / llGetRegionDayLength();
        llSetText(printTimeOfDay(timeOfDay), <1,1,0>, 1);
    }
}
```

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
