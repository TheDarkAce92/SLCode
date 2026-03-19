---
name: "llGetUnixTime"
category: "function"
type: "function"
language: "LSL"
description: 'Returns an integer that is the number of seconds elapsed since 00:00 hours, Jan 1, 1970 UTC from the system clock.'
signature: "integer llGetUnixTime()"
return_type: "integer"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetUnixTime'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgetunixtime"]
---

Returns an integer that is the number of seconds elapsed since 00:00 hours, Jan 1, 1970 UTC from the system clock.


## Signature

```lsl
integer llGetUnixTime();
```


## Return Value

Returns `integer`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetUnixTime)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetUnixTime) — scraped 2026-03-18_

Returns an integer that is the number of seconds elapsed since 00:00 hours, Jan 1, 1970  UTC from the system clock.

## Caveats

Time codes before the year 1902 or past the end of 2037 are limited due to the size of LSL's 32-bit integers. As of writing (2024) this is just 14 years away now and any scripts relying on this function may have logical errors.

## Examples

```lsl
// Reset tracker
integer BOOT_TIME;
default
{
    state_entry()
    {
        BOOT_TIME = llGetUnixTime();
        llSetTimerEvent(0.1);
    }

    timer()
    {
        llSetText((string)(llGetUnixTime() - BOOT_TIME) + " Seconds since boot.\n\n ", <1,0,0>, 1.0);
        llSetTimerEvent(1);
    }
}
```

## See Also

### Functions

- **llGetTimestamp** — Human Readable UTC Date and time
- **llGetDate** — Human Readable UTC Date
- **llGetTime** — Elapsed script-time.

<!-- /wiki-source -->
