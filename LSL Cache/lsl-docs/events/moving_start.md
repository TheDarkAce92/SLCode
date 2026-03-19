---
name: "moving_start"
category: "event"
type: "event"
language: "LSL"
description: "Triggered when task begins moving"
signature: "moving_start()"
wiki_url: 'https://wiki.secondlife.com/wiki/moving_start'
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
deprecated: "false"
parameters: []
---

Triggered when task begins moving


## Signature

```lsl
moving_start()
{
    // your code here
}
```


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/moving_start)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/moving_start) — scraped 2026-03-18_

## Caveats

- The moving_start and moving_end events require special handling when scripting attachments.

  - After adding or editing a script you must:

  - Take off the attachment and then wear the attachment again.

- This event is also triggered when an object is rezzed (unless, presumably, you happen to rez it in precisely the same spot it was before.)
- This event's behavior is undefined for non-physical movement (llSetPos, movement via build tool, etc.)
- This event is triggered when an object initiates a new keyframed motion, or when motion is resumed via KFM_CMD_PLAY

## Examples

```lsl
//Physical Prim Movement Script
//By Nika Rugani
//With spam work around

vector pos;
float move_time = 5; //Move every 5 seconds
float increment = 5;

float power = 0.5; //The TAU

integer trigger_multiple = FALSE; // This bad boy will prevent spam of moving start event
integer trigger_slave = 1;

setPhysical(integer status_physics)
{
    llSetLinkPrimitiveParamsFast(LINK_THIS, [PRIM_PHYSICS, status_physics]);
}

default
{
    touch_start(integer num_detected)
    {
        if(llGetStatus(STATUS_PHYSICS) == FALSE)
        {
            pos = llGetPos(); //Set the objects default position
            setPhysical(TRUE);
            llSetTimerEvent(move_time);
        }
        else
        {
            setPhysical(FALSE);
            llSetPos(pos);
        }
    }
    moving_start()
    {
        if(trigger_slave == 0)
        {
            llOwnerSay("YEY!! I'm Moving!");
            if(trigger_multiple == FALSE)
            {
                trigger_slave = 1;
            }
        }
    }
    moving_end()
    {
        llSetTimerEvent(move_time);
    }
    timer()
    {
        llSetTimerEvent(0);
        if(llVecDist(pos, llGetPos()) > (increment-2))
        {
            llMoveToTarget(pos, power);
        }
        else
        {
            llMoveToTarget(pos+<0.0,0.0,increment>, power);
        }
        trigger_slave = 0;
    }
}
```

## See Also

### Events

- moving_end

### Functions

- llTarget
- llRotTarget

<!-- /wiki-source -->
