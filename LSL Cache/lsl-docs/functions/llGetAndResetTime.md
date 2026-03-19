---
name: "llGetAndResetTime"
category: "function"
type: "function"
language: "LSL"
description: "Returns a float that is script time in seconds and then resets the script time to zero."
signature: "float llGetAndResetTime()"
return_type: "float"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetAndResetTime'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgetandresettime"]
---

Returns a float that is script time in seconds and then resets the script time to zero.


## Signature

```lsl
float llGetAndResetTime();
```


## Return Value

Returns `float`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetAndResetTime)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetAndResetTime) — scraped 2026-03-18_

Returns a float that is script time in seconds and then resets the script time to zero.

## Caveats

- Script time is the amount of real-world time that the script has been in a running state. It is unaffected by time dilation, but it does not count time while the script is suspended, the user is offline (when in an attachment), the object is in inventory rather than rezzed, etc.
- Script time resets when...

  - Script reset (user or llResetScript or llResetOtherScript)
  - Call to either llResetTime or llGetAndResetTime
- Due to (32 bit) floating point number limitations, the accuracy of this function is 1/32sec up to ~3 days, 1/16sec up to ~6 days, etc... doubling each time, e.g. it's only 1 second at ~194 days. Use llResetTime or llGetAndResetTime whenever practical to maintain the accuracy you require.

## Examples

```lsl
default
{
    touch_start(integer num_touch)
    {
        // This is equivalent to calling llGetTime(), then llResetTime()
        float time = llGetAndResetTime();

        llSay(0, (string)time + " seconds have elapsed since the last touch or script start.");
    }
}
```

## See Also

### Functions

- llResetTime
- llGetTime
- llGetRegionTimeDilation

<!-- /wiki-source -->
