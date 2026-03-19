---
name: "at_target"
category: "event"
type: "event"
language: "LSL"
description: "Result of llTarget library function call"
signature: "at_target(integer tnum, vector targetpos, vector ourpos)"
wiki_url: 'https://wiki.secondlife.com/wiki/at_target'
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
deprecated: "false"
parameters: []
---

Result of llTarget library function call


## Signature

```lsl
at_target(integer tnum, vector targetpos, vector ourpos)
{
    // your code here
}
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `integer` | `tnum` | llTarget return |
| `vector` | `targetpos` | llTarget position parameter |
| `vector` | `ourpos` | current position (similar to llGetPos) |


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/at_target)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/at_target) — scraped 2026-03-18_

## Examples

```lsl
integer target_id;
vector target_pos;

default
{
    state_entry()
    {
        target_pos = llGetPos() + <5.0, 0.0, 0.0>;
        target_id = llTarget(target_pos, 0.5);
        llSetStatus(STATUS_PHYSICS, TRUE);
        llMoveToTarget(target_pos, 0.4);
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

- not_at_target
- at_rot_target
- not_at_rot_target

### Functions

- **llTarget** — Setup a target position
- **llTargetRemove** — Stop a target position
- **llRotTarget** — Setup a target rotation
- **llRotTargetRemove** — Stop a target rotation

<!-- /wiki-source -->
