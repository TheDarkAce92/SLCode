---
name: "llMoveToTarget"
category: "example"
type: "example"
language: "LSL"
description: "Critically damp to target in tau seconds (if the script is physical)"
wiki_url: "https://wiki.secondlife.com/wiki/LlMoveToTarget"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

/LSL


MoveToTargetllMoveToTarget

- 1 Summary
- 2 Caveats
- 3 Examples
- 4 See Also

  - 4.1 Functions
- 5 Deep Notes

  - 5.1 Signature

## Summary

1 Bug  Function:  **llMoveToTarget**( vector target, float tau );

0.0

Forced Delay

10.0

Energy

Critically damp to target in tau seconds (if the script is physical)

• vector

target

–

position in region coordinates

• float

tau

–

seconds to critically damp in

To stop the object from maintaining the target positions use llStopMoveToTarget

To change the rotation in the same manner use llLookAt or llRotLookAt.

## Caveats

- Only works in attachments and physics-enabled objects.
- When slowly moving to a lower Z value, beware of [SVC-2441](https://jira.secondlife.com/browse/SVC-2441) - the sim will incorrectly move the object down faster than it should. That is, if you try moving to llGetPos() + <10, 10, -10>, you can end up at .z-10 several meters before getting to .x-10 and .y-10. There is a demo object in the JIRA which shows this effect.
- A llMoveToTarget call seems to persist even if physics is turned off. This is a useful trick on sluggish sims where the object can drop a bit between the call to enable physics and the call to llMoveToTarget - just do the llMoveToTarget before setting the object to physical.
- `llVecDist(llGetPos(), target)` must be *less than* 65, or no movement will occur.
- Calling llMoveToTarget with a tau of 0.0 or less will silently fail, and do nothing. The smallest functional tau is 0.044444444 (two physics frames, 2/45).

## Examples

Drop this script in a prim to have it follow the prim owner.

```lsl
default
{
    state_entry()
    {
        vector pos = llGetPos();
        llSetStatus(STATUS_PHYSICS, TRUE);
        // Little pause to allow server to make potentially large linked object physical.
        llSleep(0.1);
        llMoveToTarget(pos,0.4);
        // Look for owner within 20 meters in 360 degree arc every 1 seconds.
        llSensorRepeat("", llGetOwner(), AGENT, 20.0, PI,1.0);
    }
    sensor(integer total_number)
    {
        // Get position of detected owner
        vector pos = llDetectedPos(0);
        // Offset back one meter in X and up one meter in Z based on world coordinates.
        vector offset =<-1,0,1>;
//        offset = offset*llDetectedRot(0);  //Adding this line will orient the follower relative to the owner's position.
        pos+=offset;
        llMoveToTarget(pos,0.4);
    }
}
```

## See Also

### Functions

•

llStopMoveToTarget

•

llLookAt

•

llRotLookAt

•

llTarget

## Deep Notes

#### Signature

```lsl
function void llMoveToTarget( vector target, float tau );
```