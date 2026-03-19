---
name: "llGetStaticPath"
category: "function"
type: "function"
language: "LSL"
description: 'Returns a list of position vectors indicating pathfinding waypoints between positions at start and end, for a character of a given radius. The waypoints this function returns are for the 'static' nav mesh, meaning that objects set to 'movable obstacle' or 'movable phantom' are ignored.

This functio'
signature: "list llGetStaticPath(vector start, vector end, float radius, list params)"
return_type: "list"
sleep_time: ""
energy_cost: ""
wiki_url: 'https://wiki.secondlife.com/wiki/llGetStaticPath'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgetstaticpath"]
---

Returns a list of position vectors indicating pathfinding waypoints between positions at start and end, for a character of a given radius. The waypoints this function returns are for the 'static' nav mesh, meaning that objects set to "movable obstacle" or "movable phantom" are ignored.

This function can be used from attachments and other non-character objects. It can also be used in any region, even if dynamic pathfinding is disabled.

The list also always contains an integer in the last element, which is a status code indicating the outcome of the path query:
* If llGetStaticPath() finds a path, it will return waypoint vectors and will return a status code of 0, for success
* If llGetStaticPath() cannot find a path for some reason, it only returns the status code, indicating the sort of error. The error codes correspond to the constants in path_update (e.g. PU_FAILURE_INVALID_START is returned if the start vector is not near the nav mesh)


## Signature

```lsl
list llGetStaticPath(vector start, vector end, float radius, list params);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `vector` | `start` | Starting position |
| `vector` | `end` | End position |
| `float` | `radius` | Radius of the character that we're creating a path for, between 0.125m and 5.0m |
| `list` | `params` | Only takes the parameter CHARACTER_TYPE; the options are identical to those used for llCreateCharacter. The default value is CHARACTER_TYPE_NONE |


## Return Value

Returns `list`.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetStaticPath)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetStaticPath) — scraped 2026-03-18_

Returns a list of position vectors indicating pathfinding waypoints between positions at start and end, for a character of a given radius. The waypoints this function returns are for the 'static' nav mesh, meaning that objects set to "movable obstacle" or "movable phantom" are ignored.

## Examples

```lsl
// llGetStaticPath() test script
// Reports the static path from the object's current position to the object owner's position

// Radius of character to test for
float character_radius = 1.0;

// All defined path_update codes; note that llGetStaticPath() can only return a few of these.
list path_update_codes = [
    "PU_SLOWDOWN_DISTANCE_REACHED ",
    "PU_GOAL_REACHED",
    "PU_FAILURE_INVALID_START",
    "PU_FAILURE_INVALID_GOAL",
    "PU_FAILURE_UNREACHABLE",
    "PU_FAILURE_TARGET_GONE",
    "PU_FAILURE_NO_VALID_DESTINATION",
    "PU_EVADE_HIDDEN",
    "PU_EVADE_SPOTTED",
    "PU_FAILURE_NO_NAVMESH",
    "PU_FAILURE_DYNAMIC_PATHFINDING_DISABLED",
    "PU_FAILURE_PARCEL_UNREACHABLE",
    "PU_FAILURE_OTHER"
];

default
{
    touch_start(integer detected)
    {
        vector agent_pos = llList2Vector(llGetObjectDetails(llGetOwner(), [OBJECT_POS]), 0);
        vector end_pos = llList2Vector(llGetClosestNavPoint(agent_pos, [GCNP_STATIC, TRUE]), 0);
        vector start_pos = llList2Vector(llGetClosestNavPoint(llGetPos(), [GCNP_STATIC, TRUE]), 0);
        if(end_pos == ZERO_VECTOR)
        {
            llOwnerSay("Error: end position undefined - the object owner is either offline or far away from the nav mesh."
                + "\nagent pos is " + (string)agent_pos);
        }
        else if(start_pos == ZERO_VECTOR)
        {
            llOwnerSay("Error: start position undefined - this object is far away from the nav mesh."
                + "\nobject pos is " + (string)llGetPos());
        }
        else
        {
            llOwnerSay("Finding path from " + (string)start_pos
                + " to " + (string)end_pos
                + " for a character of radius " + (string)character_radius);
            list result = llGetStaticPath(start_pos, end_pos, character_radius, []);
            integer result_code = llList2Integer(result, -1);
            //llOwnerSay("Raw llGetStaticPath() result: " + llList2CSV(result));

            // the last element in the list is just the return code;
            // the preceding elements should be waypoint vectors
            if(result_code == 0)
            {
                llOwnerSay("llGetStaticPath found a path: " + llList2CSV(llList2List(result, 0, -2)));
            }
            else
            {
                llOwnerSay("llGetStaticPath failed to find a path, with code " + (string)result_code
                    + " (" + llList2String(path_update_codes, result_code) + ")");
            }
        }
    }
}
```

## See Also

### Events

- path_update

### Functions

- llCreateCharacter

<!-- /wiki-source -->
