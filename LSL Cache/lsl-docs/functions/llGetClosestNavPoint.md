---
name: "llGetClosestNavPoint"
category: "function"
type: "function"
language: "LSL"
description: 'Used to get a point on the navmesh that is the closest point to point.

Returns a list containing a single vector which is the closest point on the navmesh to the point provided or an empty list.'
signature: "list llGetClosestNavPoint(vector point, list options)"
return_type: "list"
sleep_time: ""
energy_cost: ""
wiki_url: 'https://wiki.secondlife.com/wiki/llGetClosestNavPoint'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgetclosestnavpoint"]
---

Used to get a point on the navmesh that is the closest point to point.

Returns a list containing a single vector which is the closest point on the navmesh to the point provided or an empty list.


## Signature

```lsl
list llGetClosestNavPoint(vector point, list options);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `vector` | `point` | A point in region-local space |
| `list (instructions)` | `options` | GCNP_* and other flags with their parameters. See options table |


## Return Value

Returns `list`.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetClosestNavPoint)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetClosestNavPoint) — scraped 2026-03-18_

Used to get a point on the navmesh that is the closest point to point.Returns a list containing a single vector which is the closest point on the navmesh to the point provided or an empty list.

## Caveats

- This function causes the script to sleep for 1 frame.
- There is no guarantee that a path exists from your current location to the returned point.

## Examples

```lsl
create_character()
{
//  Clear any previous character behaviors
    llDeleteCharacter();

//  default speed is 20
    llCreateCharacter([CHARACTER_DESIRED_SPEED, 10.0]);
    llWanderWithin(llGetPos(), <64.0, 64.0, 2.0>, []);
}

default
{
    on_rez(integer start_param)
    {
        llResetScript();
    }

    state_entry()
    {
        create_character();
    }

    touch_start(integer num_detected)
    {
        vector currentPos = llGetPos();
        list points = llGetClosestNavPoint(currentPos, [GCNP_RADIUS, 10.0] );

        if (!llGetListLength(points))
            return;

        llSay(0, "current position " + (string)currentPos
            + " and closest nav point " + (string)llList2Vector(points, 0) );
    }
}
```

## Notes

Using the method incurs a one frame script sleep and the call can be extremely expensive. It is intended to be used in response to a path_update message indicating an inability to reach a requested destination (e.g., because the character or the destination is off the mesh).

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
