---
name: "llTarget"
category: "function"
type: "function"
language: "LSL"
description: 'This function is to have the script know when it has reached a position.
It registers a position with a range that triggers at_target and not_at_target events continuously until unregistered.

Returns a handle (an integer) to unregister the target with llTargetRemove.

A similar function exists for '
signature: "integer llTarget(vector position, float range)"
return_type: "integer"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llTarget'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["lltarget"]
---

This function is to have the script know when it has reached a position.
It registers a position with a range that triggers at_target and not_at_target events continuously until unregistered.

Returns a handle (an integer) to unregister the target with llTargetRemove.

A similar function exists for rotations: llRotTarget
This function does not move the object, to do that use llSetPos or llMoveToTarget.


## Signature

```lsl
integer llTarget(vector position, float range);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `vector` | `position` | position in region coordinates |
| `float` | `range` |  |


## Return Value

Returns `integer`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llTarget)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llTarget) — scraped 2026-03-18_

This function is to have the script know when it has reached a position.It registers a position with a range that triggers at_target and not_at_target events continuously until unregistered.Returns a handle (an integer) to unregister the target with llTargetRemove.

## Caveats

- The position always references the current region. If you set llTarget to <100, 100, 100> while in Region A and then move the object to region B, the target automatically becomes <100, 100, 100> in Region B.
- The position can be set outside the region boundaries, but at_target can only happen if the range extends into the current region.  The part of the range outside the current region will not activate at_target.
- Only 8 targets can be active to a script. Additional llTarget will remove the oldest target set.

## Examples

```lsl
integer target_id;
vector target_pos;

default
{
    state_entry()
    {
        target_pos = llGetPos() + <1.0, 0.0, 0.0>;
        target_id = llTarget(target_pos, 0.5);
    }
    at_target(integer tnum, vector targetpos, vector ourpos)
    {
        if (tnum == target_id)
        {
            llOwnerSay("object is within range of target");
            llOwnerSay("target position: " + (string)targetpos + ", object is now at: " + (string)ourpos);
            llOwnerSay("this is " + (string)llVecDist(targetpos, ourpos) + " meters from the target");
            llTargetRemove(target_id);
        }
    }
    not_at_target()
    {
        llOwnerSay(
            "not there yet - object is at " + (string)llGetPos() +
            ", which is " + (string)llVecDist(target_pos, llGetPos()) +
            " meters from the target (" + (string)target_pos + ")"
        );
    }
}
```

## See Also

### Events

| • at_target | not_at_target | – | positional target events |  |
| --- | --- | --- | --- | --- |
| • at_rot_target | not_at_rot_target | – | rotational target events |  |

### Functions

- **llTargetRemove** — Cancel a target position
- **llRotTarget** — Register a target rotation
- **llRotTargetRemove** — Cancel a target rotation

<!-- /wiki-source -->
