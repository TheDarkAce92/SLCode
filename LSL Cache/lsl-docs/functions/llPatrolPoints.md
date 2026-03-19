---
name: "llPatrolPoints"
category: "function"
type: "function"
language: "LSL"
description: "Sets the object patrolling between the points specified in patrolPoints."
signature: "void llPatrolPoints(list points, list options)"
return_type: "void"
sleep_time: ""
energy_cost: ""
wiki_url: 'https://wiki.secondlife.com/wiki/llPatrolPoints'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llpatrolpoints"]
---

Sets the object patrolling between the points specified in patrolPoints.


## Signature

```lsl
void llPatrolPoints(list points, list options);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `list` | `patrolPoints` | A list of vectors for the character to travel through sequentially. The list must contain at least two entries. |
| `list (instructions)` | `options` | PATROL_* flags and their parameters |


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llPatrolPoints)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llPatrolPoints) — scraped 2026-03-18_

Sets the object patrolling between the points specified in patrolPoints.

## Caveats

- Must use llCreateCharacter or script won't compile
- Vertical positions specified for any vectors should be chosen to be as close as possible to the actual height of the terrain requested. Large difference between the provided vertical position and the actual terrain/object will result in failure of the behavior.
- The patrolPoints list requires a minimum of two valid vectors.

  - If a vector in the list is outside the nav volume (e.g.: too high,) it will be ignored.

## Examples

```lsl
default
{
    state_entry()
    {
        llCreateCharacter([CHARACTER_MAX_SPEED, 25, CHARACTER_DESIRED_SPEED, 15.0]);
        //MAX_SPEED is @ 20 by default
    }

    touch_start(integer total_number)
    {
        list points = [llGetPos() + <5,0,0>, llGetPos() - <5,0,0>];
        llPatrolPoints(points, [PATROL_PAUSE_AT_WAYPOINTS, TRUE]);
    }
}
```

## See Also

### Events

- path_update

### Functions

- llCreateCharacter
- llDeleteCharacter
- llEvade
- llExecCharacterCmd
- llGetClosestNavPoint
- llFleeFrom
- llNavigateTo
- llPatrolPoints
- llPursue
- llUpdateCharacter
- llWanderWithin

<!-- /wiki-source -->
