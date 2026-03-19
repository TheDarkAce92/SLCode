---
name: "llWanderWithin"
category: "function"
type: "function"
language: "LSL"
description: "Sets a character to wander about a central spot within a specified radius."
signature: "void llWanderWithin(vector center, vector radius, list options)"
return_type: "void"
sleep_time: ""
energy_cost: ""
wiki_url: 'https://wiki.secondlife.com/wiki/llWanderWithin'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llwanderwithin"]
---

Sets a character to wander about a central spot within a specified radius.


## Signature

```lsl
void llWanderWithin(vector center, vector radius, list options);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `vector` | `origin` | Central point to wander about |
| `vector` | `dist` | Sets how far the character may wander from origin, along each world-aligned axis |
| `list (instructions)` | `options` | WANDER_* flags and their parameters |


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llWanderWithin)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llWanderWithin) — scraped 2026-03-18_

Sets a character to wander about a central spot within a specified radius.

## Caveats

- Must use llCreateCharacter or script won't compile.
- Wander area is a rough area based on the specified origin, to a specified scale on each axis. So, if `<20, 10, 2>` is specified the object will wander within 20m along the world x-axis, 10m along the world y-axis, and 2m along the world z-axis.

  - if **dist** has any dimension less than 1.0, an error is shouted on DEBUG_CHANNEL. **Scale too small. All dimensions must be at least 1.0.**
- When WANDER_PAUSE_AT_WAYPOINTS is enabled, PU_GOAL_REACHED and PU_SLOWDOWN_DISTANCE_REACHED path_update events will be trigged when approaching each waypoint.  When this flag is disabled, the aforementioned path_update events will not be triggered when arriving at waypoints.
- Wander area can be limited to a smaller area by introducing obstacles such as walls.
- Vertical positions specified for any vectors should be chosen to be as close as possible to the actual height of the terrain requested. Large difference between the provided vertical position and the actual terrain/object will result in failure of the behavior.
- As for all pathfinding behaviors, DO NOT rely on the detailed implementation here. The wander distance is just a rough estimate. We may change the exact shape on a whim. For fun. Or because it seems better that way. Or to ensure that you aren't relying on the detailed implementation. Don't make this another [PATHBUG-69](https://jira.secondlife.com/browse/PATHBUG-69). :)

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
        llWanderWithin(llGetPos(), <10.0, 10.0, 5.0>, [WANDER_PAUSE_AT_WAYPOINTS, TRUE]);
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
