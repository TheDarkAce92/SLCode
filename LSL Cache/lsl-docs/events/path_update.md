---
name: "path_update"
category: "event"
type: "event"
language: "LSL"
description: "Fired by the pathfinding system to report status updates during character movement"
signature: "path_update(integer type, list reserved)"
wiki_url: 'https://wiki.secondlife.com/wiki/path_update'
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
deprecated: "false"
parameters: []
---

Fired by the pathfinding system to report status updates during character movement


## Signature

```lsl
path_update(integer type, list reserved)
{
    // your code here
}
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `integer` | `type` | A PU_*, it's the path event type |
| `list` | `reserved` | Reserved; not currently used. |


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/path_update)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/path_update) — scraped 2026-03-18_

## Caveats

- Note that if wandering, the "stop" (`PU_GOAL_REACHED`) type may never occur as a new goal may be chosen when near (`PU_SLOWDOWN_DISTANCE_REACHED`) the previous goal.
- When the character cannot navigate from the current position (`PU_FAILURE_INVALID_START`) llNavigateTo with the `FORCE_DIRECT_PATH` option may be helpful.

## Examples

```lsl
create_wandering_character()
{
//  Clear any previous character behaviors
    llDeleteCharacter();

//  MAX_SPEED is @ 20 by default
    llCreateCharacter([
        CHARACTER_MAX_SPEED, 25.0,
        CHARACTER_DESIRED_SPEED, 15.0]);

    llWanderWithin(llGetPos(), <10.0, 10.0,  2.0>, []);
}

list get_pathupdate_failure_info(integer type)
{
    if (type == PU_SLOWDOWN_DISTANCE_REACHED)
        return ["Near", FALSE];

    if (type == PU_GOAL_REACHED)
        return ["Stopping", FALSE];

    if (type == PU_FAILURE_INVALID_START)
        return ["Cannot path find from current location! Attempting "
                + "to go to the center of the region.", TRUE];

    if (type == PU_FAILURE_INVALID_GOAL)
        return ["Goal not on navmesh!", FALSE];

    if (type == PU_FAILURE_UNREACHABLE)
        return ["Goal unreachable!", FALSE];

    if (type == PU_FAILURE_TARGET_GONE)
        return ["Target gone!", FALSE];

    if (type == PU_FAILURE_NO_VALID_DESTINATION)
        return ["No place to go!", FALSE];

    if (type ==  PU_EVADE_HIDDEN)
        return ["Hiding from pursuer...", FALSE];

    if (type == PU_EVADE_SPOTTED)
        return ["Switched from hiding to running...", FALSE];

    if (type ==  PU_FAILURE_NO_NAVMESH)
        return ["Region has no nav mesh..", FALSE];

    if (type == PU_FAILURE_DYNAMIC_PATHFINDING_DISABLED)
        return ["Dynamic pathfinding is disabled in this region.", FALSE];

    if (type == PU_FAILURE_PARCEL_UNREACHABLE)
        return ["Parcel entry problem (is the parcel full?).", FALSE];

    if (type == PU_FAILURE_OTHER)
        return ["Hit an unspecified failure", FALSE];

    return ["Unknown failure", FALSE];
}

default
{
    on_rez(integer start_param)
    {
        llResetScript();
    }

    state_entry()
    {
        create_wandering_character();
    }

    path_update(integer type, list reserved)
    {
        list params = get_pathupdate_failure_info(type);
        string info = llList2String(params, 0);
        integer /* boolean */ hasToMove = llList2Integer(params, 1);

        llRegionSayTo(llGetOwner(), 0, info);
        if (hasToMove)
        {
            vector currentPosition = llGetPos();
            llNavigateTo(<128.0, 128.0, llGround(<128.0, 128.0, 0.0> - currentPosition)>, [FORCE_DIRECT_PATH, TRUE]);
        }
    }
}
```

## See Also

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
