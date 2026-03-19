---
name: "llFleeFrom"
category: "function"
type: "function"
language: "LSL"
description: "Directs a character to keep a specific distance from a specific position in the region or adjacent regions."
signature: "void llFleeFrom(vector source, float radius, list options)"
return_type: "void"
sleep_time: ""
energy_cost: ""
wiki_url: 'https://wiki.secondlife.com/wiki/llFleeFrom'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llfleefrom"]
---

Directs a character to keep a specific distance from a specific position in the region or adjacent regions.


## Signature

```lsl
void llFleeFrom(vector source, float radius, list options);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `vector` | `position` | position in region coordinates from which to flee. |
| `float` | `distance` | Distance in meters to flee from position. |
| `list (instructions)` | `options` | No options available at this time. |


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llFleeFrom)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llFleeFrom) — scraped 2026-03-18_

Directs a character to keep a specific distance from a specific position in the region or adjacent regions.

## Caveats

- Must use llCreateCharacter or script won't compile.
- The position to flee from must be near the nav mesh; otherwise, this behavior will fail and trigger path update with PU_FAILURE_INVALID_GOAL.
- If you want to avoid an agent or object as per the example below, it's much more elegant and less sim resource intensive to use llEvade instead.

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
	last_touched_pos = llDetectedPos(0);
	llFleeFrom(last_touched_pos, 10, []);
	llSetTimerEvent(0.2);
    }

    timer()
    {
	vector last_touched_pos_now = llList2Vector(llGetObjectDetails(last_touched_key, [OBJECT_POS]), 0);
	if ( llVecDist(last_touched_pos, last_touched_pos_now) > 1 )
	{
	    last_touched_pos = last_touched_pos_now;
	    llFleeFrom(last_touched_pos, 10, []);
	}
    }
}
```

## Notes

The position vector can be set outside the current region by using extended range region coordinates: e.g., to avoid the SE corner of the region to the East of the current one, you could

```lsl
llFleeFrom(<0.0, 512.0, 0.0>, 20.0, []);
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
