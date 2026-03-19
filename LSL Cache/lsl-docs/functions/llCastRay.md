---
name: "llCastRay"
category: "function"
type: "function"
language: "LSL"
description: 'Cast a line from start to end and report collision data for intersections with objects.

Returns a list of strided values on a successful hit, with an additional integer status_code at the end.

Each stride consists of two mandatory values {key uuid, vector position} and optionally {integer link_num'
signature: "list llCastRay(vector start, vector end, list params)"
return_type: "list"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llCastRay'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llcastray"]
---

Cast a line from start to end and report collision data for intersections with objects.

Returns a list of strided values on a successful hit, with an additional integer status_code at the end.

Each stride consists of two mandatory values {key uuid, vector position} and optionally {integer link_number, vector normal}. (See RC_DATA_FLAGS for details.)

A negative status_code is an error code, otherwise it is the number of hits (and strides) returned.

Example return of successful raycast, using the default options:
[key object_uuid, vector hit_position, integer status_code]

In the case of an error, or if the ray hits nothing, the resulting list only contains the status code:
[integer status_code]


## Signature

```lsl
list llCastRay(vector start, vector end, list params);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `vector` | `start` | starting location |
| `vector` | `end` | ending location |
| `list (instructions)` | `options` | can consists of any number of option flags and their parameters. |


## Return Value

Returns `list`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llCastRay)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llCastRay) — scraped 2026-03-18_

Cast a line from start to end and report collision data for intersections with objects.Returns a list of strided values on a successful hit, with an additional integer status_code at the end.

## Caveats

- Depending upon the value of flags (provided via RC_DATA_FLAGS), the number and types of values in the strides will vary. See RC_DATA_FLAGS for details.
- llGetRot will not return an avatar's exact visual rotation because the viewer doesn't update the avatar's rotation under a threshold (see [VWR-1331](https://jira.secondlife.com/browse/VWR-1331)). To get an avatar's exact looking direction while in mouselook, use llGetCameraRot instead.
- llCastRay will not detect prims having no physics shape (PRIM_PHYSICS_SHAPE_TYPE = PRIM_PHYSICS_SHAPE_NONE).
- llCastRay will not detect a prim if the line starts inside the prim. This makes it safe to use the prim position as the start location.
- llCastRay can detect the prim the script is in, if the start location is outside the prim.
- The result of this function has been noted to be **unreliable when the end point is out-of-bounds** (Occasionally returns status code 0 regardless of amount of objects hit). (See [this forum post](https://community.secondlife.com/forums/topic/486603-llcastray-returning-zero-hits-seemingly-at-random/))

  - The random failures seem to happen if the ray begins or ends more than 8 meters outside of current region bounds. Changes in only the ray's angle, or only in its position, may change the result. The result does not change if the exact same ray is cast again.

## Examples

This basic example will cast a ray from the center of the object, 10 meters forward, depending on the object's rotation.

```lsl
default
{
    touch_start(integer total_number)
    {
        vector start = llGetPos();
        vector end = start + <10,0,0> * llGetRot();

        list data = llCastRay(start, end, []);
        llOwnerSay(llList2CSV(data));
    }
}
```

This is an example attachment that casts a ray based on the owner's camera in mouselook. It has many applications for things like weapons, scripted interactions with the world (like allowing a HUD to display information about things the user is looking at), etc.

```lsl
integer gTargetChan = -9934917;

default
{
    attach(key id)
    {
        if (id != NULL_KEY)
        {
            llRequestPermissions(id,PERMISSION_TAKE_CONTROLS|PERMISSION_TRACK_CAMERA);
        }
    }

    run_time_permissions (integer perm)
    {
        if (perm & PERMISSION_TAKE_CONTROLS|PERMISSION_TRACK_CAMERA)
        {
            llTakeControls(CONTROL_LBUTTON|CONTROL_ML_LBUTTON,TRUE,FALSE);
        }
    }

    control (key id, integer level, integer edge)
    {
        // User must be in mouselook to aim the weapon
        if (level & edge & CONTROL_LBUTTON)
        {
            llSay(0,"You must be in Mouselook to shoot.  Type \"CTRL + M\" or type \"Esc\" and scroll your mouse wheel forward to enter Mouselook.");
        }
        // User IS in mouselook
        if (level & edge & CONTROL_ML_LBUTTON)
        {
            vector start = llGetCameraPos();
            // Detect only a non-physical, non-phantom object. Report its root prim's UUID.
            list results = llCastRay(start, start+<60.0,0.0,0.0>*llGetCameraRot(),[RC_REJECT_TYPES,RC_REJECT_PHYSICAL|RC_REJECT_AGENTS|RC_REJECT_LAND,RC_DETECT_PHANTOM,FALSE,RC_DATA_FLAGS,RC_GET_ROOT_KEY,RC_MAX_HITS,1]);
            llTriggerSound(llGetInventoryName(INVENTORY_SOUND,0),1.0);
            llSleep(0.03);
            key target = llList2Key(results,0);
            // Tell target that it has been hit.
            llRegionSayTo(target,gTargetChan,"HIT");
            // Target, scripted to listen on gTargetChan, can explode, change color, fall over .....
        }
    }
}
```

This example handles the caveat about rays extending outside of region bounds by calculating the point where the ray intersects with the region's edge.

```lsl
vector GetRegionEdge(vector start, vector dir)
{
    float scaleGuess;
    float scaleFactor = 4095.99;
    if (dir.x)
    {
        scaleFactor = ((dir.x > 0) * 255.99 -start.x) / dir.x;
    }
    if (dir.y)
    {
        scaleGuess = ((dir.y > 0) * 255.99 - start.y) / dir.y;
        if (scaleGuess < scaleFactor) scaleFactor = scaleGuess;
    }
    if (dir.z)
    {
        scaleGuess = ((dir.z > 0) * 4095.99 - start.z) / dir.z;
        if (scaleGuess < scaleFactor) scaleFactor = scaleGuess;
    }
    return start + dir * scaleFactor;
}

default
{
    touch_start(integer total_number)
    {
        vector start = llGetPos();
        vector direction = <1,0,0> * llGetRot();
        vector end = GetRegionEdge(start, direction);

        list data = llCastRay(start, end, []);
        llOwnerSay(llList2CSV(data));
    }
}
```

This example casts a ray from the center of the object, 25 meters north, while applying different RC_REJECT_TYPES each time.

```lsl
integer filter;// default is 0

default
{
    state_entry()
    {
        string ownerName = llKey2Name(llGetOwner());
        llOwnerSay("Hello, " + ownerName + "!");
    }

    touch_start(integer total_number)
    {
        vector start = llGetPos();
        vector end = start - <0.0, -25.0, 0.0>;

        if ( filter > 8 )
            filter = 0;

        llOwnerSay("Filter " + (string)filter);

        list results = llCastRay(start, end, [RC_REJECT_TYPES, filter, RC_MAX_HITS, 4] );

        integer hitNum = 0;
        // Handle error conditions here by checking llList2Integer(results, -1) >= 0
        while (hitNum < llList2Integer(results, -1))
        {
            // Stride is 2 because we didn't request normals or link numbers
            key uuid = llList2Key(results, 2*hitNum);

            string name = "Land"; // if (uuid == NULL_KEY)

            if (uuid != NULL_KEY)
                name = llKey2Name(uuid);

            llOwnerSay("Hit " + name + ".");

            ++hitNum;
        }

        ++filter;
    }
}
```

## Notes

Use llDumpList2String to see what the output looks like when you try a new set of flags.

To quickly get the status code use `llList2Integer(result, -1)`.

**Ideas for uses**:

- **Weapons** - Raycasts are the traditional tool used in game development for simulating projectile weapons. They are orders of magnitude more efficient than rezzing a prim and launching it from a weapon.
- **AI Objects** - Line-of-sight detection of avatars and other objects, or for navigating an environment by tracing rays about themselves. For example; casting rays directly downwards to determine the height and angle (normal) of the current floor surface, useful for non-physical object movement.
- **Intelligent Object Placement** - Static objects can be placed in-scene, but adjust themselves to their environment. For example; an object rezzed too high up may adjust its height to floor-level, or a computer console placed low down may cause an avatar to kneel to use it rather than standing.
- **Environment Analysis** - Can be used to determine the limitations of a surrounding area, such as determining if an object has been placed within a closed room. Not a test to be performed frequently due to quantity of rays required, but could be used by objects to switch off effects if unobserved (no-one within the room). Auto-adjusting furniture or objects to snap to walls, floors, and ceilings.

<!-- /wiki-source -->
