---
name: "llGetWallclock"
category: "function"
type: "function"
language: "LSL"
description: 'Returns a float that is the time in seconds since midnight Pacific time (PST/PDT), truncated to whole seconds. That is the same as the time of day in SLT expressed as seconds.

For GMT use llGetGMTclock'
signature: "float llGetWallclock()"
return_type: "float"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetWallclock'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgetwallclock"]
---

Returns a float that is the time in seconds since midnight Pacific time (PST/PDT), truncated to whole seconds. That is the same as the time of day in SLT expressed as seconds.

For GMT use llGetGMTclock


## Signature

```lsl
float llGetWallclock();
```


## Return Value

Returns `float`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetWallclock)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetWallclock) — scraped 2026-03-18_

Returns a float that is the time in seconds since midnight Pacific time (PST/PDT), truncated to whole seconds. That is the same as the time of day in SLT expressed as seconds.

## Examples

```lsl
// Real World Sun
integer Flag;

default
{
    state_entry()
    {
        Flag = -1;
        llSetTimerEvent(0.1);
    }

    timer()
    {
        float time = llGetWallclock();
        if (Flag == -1)
        {
            llSetTimerEvent(60.0);
        }
        if (time < 21600)
        {
            if (Flag)
            {
                llSetText("The Sun is coming! :)", <1,1,0>, 1.0);
                Flag = 0;
            }
        }
        else if (time < 64800)
        {
            if (Flag != 1)
            {
                llSetText("Sun has risen. :(", <1,0,0>, 1.0);
                Flag = 1;
            }
        }
        else if (Flag != 2)
        {
            llSetText("Goodbye Sun. :(", <1,0,0>, 1.0);
            Flag = 2;
        }
    }
}
```

```lsl
// Convert to human-readable HH:MM:SS format
string ConvertWallclockToTime()
{
    integer now = (integer)llGetWallclock();
    integer seconds = now % 60;
    integer minutes = (now / 60) % 60;
    integer hours = now / 3600;
    return llGetSubString("0" + (string)hours, -2, -1) + ":"
        + llGetSubString("0" + (string)minutes, -2, -1) + ":"
        + llGetSubString("0" + (string)seconds, -2, -1);
}

default
{
    touch_start(integer total_number)
    {
        llSay(0, ConvertWallclockToTime());
    }
}
```

```lsl
// Convert to human-readable 12-hour HH:MM:SS (AM/PM) format
string ConvertWallclockToTime()
{
    integer now = (integer)llGetWallclock();
    integer seconds = now % 60;
    integer minutes = (now / 60) % 60;
    integer hours = now / 3600;

    return llGetSubString("0" + (string)(hours % 12), -2, -1) + ":"
           + llGetSubString("0" + (string)minutes, -2, -1) + ":"
           + llGetSubString("0" + (string)seconds, -2, -1) + " "
           + llList2String(["AM", "PM"], (hours > hours % 12));
}

default
{
    touch_start(integer total_number)
    {
        llSay(0, ConvertWallclockToTime());
    }
}
```

## Notes

To determine if the current time returned by this function is PST or PDT, you can look at the difference between llGetGMTclock() and llGetWallclock(). The difference will be either 8 hours or -16 hours for PST, and 7 hours or -17 hours for PDT, that is 28800 or -57600,  or 25200 or -61200 seconds.

## See Also

### Functions

- **llGetGMTclock** — Seconds since midnight GMT

<!-- /wiki-source -->
