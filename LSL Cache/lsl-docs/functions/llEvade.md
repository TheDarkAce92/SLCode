---
name: "llEvade"
category: "function"
type: "function"
language: "LSL"
description: "Characters will (roughly) try to hide from their pursuers if there is a good hiding spot along their fleeing path. Hiding means no direct line of sight from the head of the character (center of the top of its physics bounding box) to the head of its pursuer and no direct path between the two on the "
signature: "void llEvade(key target, list options)"
return_type: "void"
sleep_time: ""
energy_cost: ""
wiki_url: 'https://wiki.secondlife.com/wiki/llEvade'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llevade"]
---

Characters will (roughly) try to hide from their pursuers if there is a good hiding spot along their fleeing path. Hiding means no direct line of sight from the head of the character (center of the top of its physics bounding box) to the head of its pursuer and no direct path between the two on the navmesh.


## Signature

```lsl
void llEvade(key target, list options);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `key` | `target` | group, avatar or object UUID to evade |
| `list (instructions)` | `options` | No options currently available |


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llEvade)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llEvade) — scraped 2026-03-18_

Characters will (roughly) try to hide from their pursuers if there is a good hiding spot along their fleeing path. Hiding means no direct line of sight from the head of the character (center of the top of its physics bounding box) to the head of its pursuer and no direct path between the two on the navmesh.

## Caveats

- Must use llCreateCharacter or script will not compile.
- If the target is an object, it must be unlinked or be the root prim of a linkset.

## Examples

```lsl
vector start_position;

default
{
    on_rez(integer start_param)
    {
        llResetScript();
    }

    state_entry()
    {
        llDeleteCharacter();
        llCreateCharacter([CHARACTER_MAX_SPEED, 25, CHARACTER_DESIRED_SPEED, 15.0]);

        start_position = llGetPos();
        llWanderWithin(start_position, <10.0, 10.0, 2.0>, [] );
    }

    touch_start(integer num_detected)
    {
        llEvade(llDetectedKey(0), []);
        llSetTimerEvent(20.0);
    }

    timer()
    {
    //  do not keep running away...
        llSetTimerEvent(0.0);

        llWanderWithin(start_position, <10.0, 10.0, 2.0>, [] );
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
