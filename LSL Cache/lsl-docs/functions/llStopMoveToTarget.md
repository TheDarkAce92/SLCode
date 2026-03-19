---
name: "llStopMoveToTarget"
category: "function"
type: "function"
language: "LSL"
description: 'Stops critically damped motion

Use in conjunction with llMoveToTarget
To stop rotation movement use llStopLookAt'
signature: "void llStopMoveToTarget()"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llStopMoveToTarget'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llstopmovetotarget"]
---

Stops critically damped motion

Use in conjunction with llMoveToTarget
To stop rotation movement use llStopLookAt


## Signature

```lsl
void llStopMoveToTarget();
```


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llStopMoveToTarget)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llStopMoveToTarget) — scraped 2026-03-18_

Stops critically damped motion

## Examples

```lsl
integer gLockPrimInPlace;

default
{

    on_rez(integer sp)
    {
        llResetScript();
    }

    state_entry()
    {
        llStopMoveToTarget();
        llSetStatus(STATUS_PHYSICS, TRUE);
    }

    touch_start(integer total_number)
    {

        if (llDetectedKey(0) != llGetOwner())
        {
            return;
        }

        if (!llGetStatus(STATUS_PHYSICS))
        {
            llOwnerSay("Locking or unlocking position works only for physical objects.");
            return;
        }

        gLockPrimInPlace = !gLockPrimInPlace;
        if (gLockPrimInPlace)
        {
            llMoveToTarget(llGetPos(), 0.05);
            llOwnerSay("Locked in place.");
        }
        else
        {
            llStopMoveToTarget();
            llOwnerSay("Unlocked.");
        }

    }

}
```

<!-- /wiki-source -->
