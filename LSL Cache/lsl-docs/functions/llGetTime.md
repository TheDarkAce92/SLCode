---
name: "llGetTime"
category: "function"
type: "function"
language: "LSL"
description: "Returns the time elapsed in seconds since the script was started or last reset via llResetTime"
wiki_url: "https://wiki.secondlife.com/wiki/llGetTime"
first_fetched: "2026-03-09"
last_updated: "2026-03-09"
signature: "float llGetTime()"
parameters: []
return_type: "float"
energy_cost: "0.0"
sleep_time: "0.0"
patterns: ["llgettime"]
deprecated: "false"
---

# llGetTime

```lsl
float llGetTime()
```

Returns the time elapsed in seconds since the script was last started or since `llResetTime` was last called.

## Return Value

`float` — elapsed seconds.

## Example

```lsl
default
{
    state_entry()
    {
        llResetTime();
    }

    timer()
    {
        llOwnerSay("Elapsed: " + (string)llGetTime() + "s");
    }
}
```

## See Also

- `llResetTime` — reset the script clock to 0
- `llGetUnixTime` — Unix epoch timestamp
- `llGetTimestamp` — ISO 8601 formatted timestamp
- `llGetWallclock` — seconds elapsed in the current day (UTC)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetTime) — scraped 2026-03-18_

Returns a float that is script time in seconds with subsecond precision since the script started, was last reset, or call to either llResetTime or llGetAndResetTime.

## Caveats

- Script time is the amount of real-world time that the script has been in a running state. It is unaffected by time dilation, but it does not count time while the script is suspended, the user is offline (when in an attachment), the object is in inventory rather than rezzed, etc.
- Script time resets when...

  - Script reset (user or llResetScript or llResetOtherScript)
  - Call to either llResetTime or llGetAndResetTime
- Due to (32 bit) floating point number limitations, the accuracy of this function is 1/64sec up to ~3 days, 1/32sec up to ~6 days, etc... doubling each time, e.g. it's only 1 second at ~194 days. Use llResetTime or llGetAndResetTime whenever practical to maintain the accuracy you require:

| Precision | Up to Seconds | Hours | Days |
| --- | --- | --- | --- |
| 0.016=2-6 | 262144=218 | 72.82 | 3.03 |
| 0.022=1/45 | 1 simulator frame |  |  |
| 0.031=2-5 | 524288=219 | 145.63 | 6.06 |
| 0.063=2-4 | 1048576=220 | 291.27 | 12.13 |
| 0.125=2-3 | 2097152=221 | 582.54 | 24.27 |
| 0.250=2-2 | 4194304=222 | 1165.08 | 48.54 |
| 0.500=2-1 | 8388608=223 | 2330.16 | 97.09 |
| 1.000=2-0 | 16777216=224 | 4660.33 | 194.18 |

- Note that this precision caveat does not apply to scripts written in SLua, only to LSL scripts. In SLua:

  - the timer precision is 64-bit, and will maintain 1/64sec precision for ~4.4million years.
  - llResetTime and llGetAndResetTime have been removed

## Examples

```lsl
default {
    state_entry()
    {
        llResetTime();
    }
    touch_start(integer num_touch)
    {
        float time = llGetTime(); //Instead getting, and then resetting the time, we could use llGetAndResetTime() to accomplish the same thing.
        llResetTime();
        llSay(0,(string)time + " seconds have elapsed since the last touch." );
    }
}
```

```lsl
// Distinguish between a single click and a double click

float gHoldTime;

default
{
    touch_start(integer total_number)
    {
        float now = llGetTime();
        if (now - gHoldTime < 0.3)
        {
            llSay(PUBLIC_CHANNEL,"Double clicked");
            // Trigger one sequence of actions
        }
        else
        {
            llSetTimerEvent(0.32);
        }
        gHoldTime = now;
    }

    timer()
    {
        llSetTimerEvent(0.0);
        if (llGetTime()-gHoldTime > 0.3)
        {
            llSay(PUBLIC_CHANNEL,"Single clicked.");
            // Trigger a different sequence of actions
        }
    }
}
```

```lsl
//  To do time-dependant loops of whatever:
//  for example move 2 meters within 5.0 seconds

float time = 5.0;
float i;
llResetTime();
do
{
    i = llGetTime()/time;
    // move2meters*i
}
while (llGetTime() < time);
```

## See Also

### Functions

- llResetTime
- llGetAndResetTime
- llGetRegionTimeDilation

<!-- /wiki-source -->
