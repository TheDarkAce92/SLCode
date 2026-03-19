---
name: "llCreateCharacter"
category: "function"
type: "function"
language: "LSL"
description: 'Creates a pathfinding entity, known as a 'character', from the object containing the script. Required to activate use of pathfinding functions.

By default, the character's shape will be an upright capsule approximately the size of the linkset, adjustable via the options list. The linkset must use t'
signature: "void llCreateCharacter(list options)"
return_type: "void"
sleep_time: ""
energy_cost: ""
wiki_url: 'https://wiki.secondlife.com/wiki/llCreateCharacter'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llcreatecharacter"]
---

Creates a pathfinding entity, known as a "character", from the object containing the script. Required to activate use of pathfinding functions.

By default, the character's shape will be an upright capsule approximately the size of the linkset, adjustable via the options list. The linkset must use the land impact accounting system introduced with the mesh project.
If called on an existing character, all unspecified parameters other than character size will revert to their defaults (if not specified, character size will not change). This is STRONGLY preferred over calling llDeleteCharacter() followed by llCreateCharacter() as it is much, much less taxing on the server.


## Signature

```lsl
void llCreateCharacter(list options);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `list (instructions)` | `options` | Character configuration options. |


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llCreateCharacter)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llCreateCharacter) — scraped 2026-03-18_

Creates a pathfinding entity, known as a "character", from the object containing the script. Required to activate use of pathfinding functions.

## Caveats

(subject to change)

- You only need to use one llCreateCharacter call per object, calling multiple times has no effect.
- One script can contain an llCreateCharacter call and other scripts can exploit that with other path functions that require it.
- llCreateCharacter status survives state changes, script resets, and rezzing.
- llCreateCharacter is always required for all pathing functions.
- When an object becomes a character, its physics weight becomes fixed at 15.
- If we have multiple scripts containing llCreateCharacter in the same object nothing untoward happens.
- If multiple scripts use conflicting path functions in the same object (different prims or the same prim) one will take precedence randomly (apparently).
- CHARACTER_MAX_SPEED - See [PATHBUG-42](https://jira.secondlife.com/browse/PATHBUG-42) - In testing, we have found a desired speed of 10m/s to be plenty fast most uses and that higher speeds may produce unexpected results (particularly when navigating tight spaces or making sharp turns). March 15, 2012
- CHARACTER_MAX_ANGULAR_ACCEL min = 1.5708
- The character's shape is a capsule (cylinder with spherical ends) with a length (from tip to tip) and a circular cross section of some radius. These two size parameters are what is controlled by the CHARACTER_LENGTH and CHARACTER_RADIUS params respectively.
- Note that the character's true "length" cannot be smaller than twice the radius plus 0.1m; however, you're welcome to specify a value lower than that (but more than zero) -- the script shouldn't complain.
- The capsule is usually oriented vertically. Use [CHARACTER_ORIENTATION, HORIZONTAL] if you need your character to be horizontal.

  - Use a vertical capsule whenever possible; horizontal capsules may become stuck more easily than vertical capsules.
- Removing the script from a prim will not stop pathing behavior, in the same way that particles and hover text remain. However, if the character encounters an error state, it will be unable to recover since there is no original script to get error handling from. Removing scripts from actively used characters is NOT recommended.  To stop a pathing command use `llExecCharacterCmd(CHARACTER_CMD_STOP, [])`.
- The root prim's position determines the characters height above the surface; if your character sinks under the surface or is too high above it adjust the relative position of the root prim to the rest of the linkset (or create a new root prim, which you might texture invisible, to control your character's apparent height).
- The default value of CHARACTER_STAY_WITHIN_PARCEL depends on the CHARACTER_TYPE.

  - If CHARACTER_TYPE is set to anything other than CHARACTER_TYPE_NONE, then CHARACTER_STAY_WITHIN_PARCEL will default to TRUE, so always explicitly set CHARACTER_STAY_WITHIN_PARCEL to FALSE if you don't want the character to stop at parcel borders.

## Examples

```lsl
create_character()
{
//  Clear any previous character behaviors
    llDeleteCharacter();

//  MAX_SPEED is @ 20 by default
    llCreateCharacter([ CHARACTER_MAX_SPEED, 25,
                        CHARACTER_DESIRED_SPEED, 15.0]);
}

patrol_around(vector targetPos)
{
    list points = [targetPos + <5, 0, 0>, targetPos - <5, 0, 0>];
    llPatrolPoints(points, []);
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
        patrol_around(llGetPos());
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
- llGetStaticPath
- llFleeFrom
- llNavigateTo
- llPatrolPoints
- llPursue
- llUpdateCharacter
- llWanderWithin

<!-- /wiki-source -->
