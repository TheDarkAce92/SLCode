---
name: "llRezAtRoot"
category: "function"
type: "function"
language: "LSL"
description: 'Instantiate inventory object rotated to rot with its root at position, moving at velocity, using param as the start parameter.

To rez an object so its center is at position (instead of the root) use llRezObject instead.'
signature: "void llRezAtRoot(string inventory, vector pos, vector vel, rotation rot, integer param)"
return_type: "void"
sleep_time: "0.1"
energy_cost: "200.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llRezAtRoot'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llrezatroot"]
---

Instantiate inventory object rotated to rot with its root at position, moving at velocity, using param as the start parameter.

To rez an object so its center is at position (instead of the root) use llRezObject instead.


## Signature

```lsl
void llRezAtRoot(string inventory, vector pos, vector vel, rotation rot, integer param);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `string` | `inventory` | an object in the inventory of the prim this script is in |
| `vector` | `position` | position in region coordinates to place the object |
| `vector` | `velocity` | initial velocity |
| `rotation` | `rot` | initial rotation |
| `integer` | `param` | on_rez event parameter and value returned by llGetStartParameter in the rezzed object (or by each of the items in a coalesced object). |


## Caveats

- Forced delay: **0.1 seconds** — the script sleeps after each call.
- Energy cost: **200.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llRezAtRoot)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llRezAtRoot) — scraped 2026-03-18_

Instantiate inventory object rotated to rot with its root at position, moving at velocity, using param as the start parameter

## Caveats

- This function causes the script to sleep for 0.1 seconds.
- If inventory is missing from the prim's inventory   or it is not an object then an error is shouted on DEBUG_CHANNEL.
- Silently fails to rez inventory if position is more than 10 meters away from the prim trying to rez inventory. (Note: the max distance is actually 10.0 + llVecMag(llGetScale()/2))
- If the object is unattached and the owner of the object does not have copy permission  on inventory, the object will no longer be present in inventory after it is rezzed (so another attempt to rez (the same object) will fail); if the owner does have copy permission, then a copy is rezzed, and the original inventory remains in inventory.
- If the object is attached and the owner of the object does not have copy permission  on inventory, an error is shouted on DEBUG_CHANNEL: "Cannot rez no copy objects from an attached object."
- Silently fails if you don't have offline building rights on the land. To have the right, your objects needs to *either*:

  - Be on land you own yourself.
  - Be on land where anyone is allowed to build, e.g. a sandbox.
  - Be deeded to the group that owns the land.
  - Be set to the same group that owns the land and the land have the parcel flag 'allow group to build' set.
- The group role "Always allow 'Create Objects'" will only work to override this when you are online, in the region, or have a child agent in the region. See the issues under Deep Notes for more information.
- See object_rez for examples on how to establish communications between the rezzing object and the new prim.

## Examples

```lsl
//Rez an object on touch
string object = "Object";//Object in inventory
integer start_param = 10;
rotation rot;

default
{
    state_entry()
    {
        rot = llEuler2Rot(< 0, 90, 90> * DEG_TO_RAD);
    }
    touch_start(integer a)
    {
        vector vec = llGetPos() + < 0.0, 0.0, 5.0>; // 5 meter above this
        vector speed = llGetVel();
        llRezAtRoot(object, vec, speed, rot, start_param);
    }
}
```

```lsl
//Rez an object on touch, with relative position, rotation, and velocity all described in the rezzing prim's coordinate system.
string object = "Object"; // Name of object in inventory
vector relativePosOffset = <2.0, 0.0, 1.0>; // "Forward" and a little "above" this prim
vector relativeVel = <1.0, 0.0, 0.0>; // Traveling in this prim's "forward" direction at 1m/s
rotation relativeRot = <0.707107, 0.0, 0.0, 0.707107>; // Rotated 90 degrees on the x-axis compared to this prim
integer startParam = 10;

default
{
    touch_start(integer a)
    {
        vector myPos = llGetPos();
        rotation myRot = llGetRot();

        vector rezPos = myPos+relativePosOffset*myRot;
        vector rezVel = relativeVel*myRot;
        rotation rezRot = relativeRot*myRot;

        llRezAtRoot(object, rezPos, rezVel, rezRot, startParam);
    }
}
```

```lsl
/*
    NO COPY Rezzer Example by Daemonika Nightfire
    Always rez the first object at touch, removing it from the content,
    when the first one is removed, the next object automatically moves to the first position.

    Content example:
    object (no copy)
    object 1 (no copy)
    object 2 (no copy)
    object 3 (no copy)
    object 4 (no copy)
    ...

*/

vector relativePosOffset = <2.0, 0.0, 1.0>; // "Forward" and a little "above" this prim
vector relativeVel = <1.0, 0.0, 0.0>; // Traveling in this prim's "forward" direction at 1m/s
vector relativeRot = <90, 0, 0>; // Rotated 90 degrees on the x-axis compared to this prim
integer startParam = 10;

default
{
    touch_start(integer a)
    {
        if(llGetInventoryNumber(INVENTORY_OBJECT) > 0) // checks if at least 1 object is present.
        {
            string object = llGetInventoryName(INVENTORY_OBJECT, 0); // name of the first object in inventory
            vector myPos = llGetPos();
            rotation myRot = llGetRot();

            vector rezPos = myPos+relativePosOffset*myRot;
            vector rezVel = relativeVel*myRot;
            rotation rezRot = llEuler2Rot(relativeRot*DEG_TO_RAD)*myRot;

            llRezAtRoot(object, rezPos, rezVel, rezRot, startParam);
        }
        else
        {
            llSay(0, "This rezzer is empty");
        }
    }
}
```

## See Also

### Constants

- PRIM_TEMP_ON_REZ

### Events

- **object_rez** — triggered when this object rezzes an object from inventory

### Functions

- llRezObject
- llGetStartParameter
- llGodLikeRezObject

<!-- /wiki-source -->
