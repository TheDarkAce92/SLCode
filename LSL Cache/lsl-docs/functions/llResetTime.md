---
name: "llResetTime"
category: "function"
type: "function"
language: "LSL"
description: "Resets the script-time timer to zero."
signature: "void llResetTime()"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llResetTime'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llresettime"]
---

Resets the script-time timer to zero.


## Signature

```lsl
void llResetTime();
```


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llResetTime)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llResetTime) — scraped 2026-03-18_

Resets the script-time timer to zero.

## Caveats

- Script time resets when...

  - Script reset (user or llResetScript or llResetOtherScript)
  - Call to either llResetTime or llGetAndResetTime
- Script time measures real world time, it is unaffected by time dilation.

## Examples

```lsl
default {
    state_entry()
    {
        llResetTime();
    }
    touch_start(integer num_touch)
    {
        float time = llGetTime(); //Instead getting, and then resetting the time, we could use llGetAndReset() to accomplish the same thing.
        llResetTime();
        llSay(0,(string)time + " seconds have elapsed since the last touch." );
    }
}
```

## See Also

### Functions

- llGetTime
- llGetAndResetTime

<!-- /wiki-source -->
