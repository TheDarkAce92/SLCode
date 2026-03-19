---
name: "llNavigateTo"
category: "function"
type: "function"
language: "LSL"
description: 'Directs an object to travel to a defined position in the region or adjacent regions.

Adjacent regions can be reached by extending the position vector into the nearby region.'
signature: "void llNavigateTo(vector point, list options)"
return_type: "void"
sleep_time: ""
energy_cost: ""
wiki_url: 'https://wiki.secondlife.com/wiki/llNavigateTo'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llnavigateto"]
---

Directs an object to travel to a defined position in the region or adjacent regions.

Adjacent regions can be reached by extending the position vector into the nearby region.


## Signature

```lsl
void llNavigateTo(vector point, list options);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `vector` | `pos` | position in region coordinates for the character to navigate to. |
| `list (instructions)` | `options` | List of parameters to control the type of pathfinding used. |


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llNavigateTo)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llNavigateTo) — scraped 2026-03-18_

Directs an object to travel to a defined position in the region or adjacent regions.

## Caveats

- Must use llCreateCharacter first or the function will fail with a viewer error.
- Vertical positions specified for any vectors should be chosen to be as close as possible to the actual height of the surface requested. Large difference between the provided vertical position and the actual terrain/object will result in failure of the behavior.
- If you want to chase an agent or object as per the example below, it's much more elegant and less sim resource intensive to use llPursue instead.

## Examples

```lsl
vector last_touched_pos;
key last_touched_key;

default
{
    state_entry()
    {
        llCreateCharacter([CHARACTER_DESIRED_SPEED, 50.0]);
    }

    touch_start(integer total_number)
    {
        last_touched_key = llDetectedKey(0);
        last_touched_pos = llList2Vector(llGetObjectDetails(last_touched_key, [OBJECT_POS]), 0);
        llNavigateTo(last_touched_pos, []);
        llSetTimerEvent(0.2);
    }

    timer()
    {
        vector last_touched_pos_now = llList2Vector(llGetObjectDetails(last_touched_key, [OBJECT_POS]), 0);
        if ( llVecDist(last_touched_pos_now, last_touched_pos) > 1 )
        {
            last_touched_pos = last_touched_pos_now;
            llNavigateTo(last_touched_pos, []);
        }
    }
}
```

## Notes

- FORCE_DIRECT_PATH can be used to rescue characters that have somehow fallen off the navigable zone as it doesn't use the navmesh.

(Needs verification.)

- The position vector can be set outside the current region by using extended range region coordinates: e.g., to go to the SE corner of the region to the East of the current one, you could llNavigateTo(<0.0, 512.0, 0.0>, []);

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
