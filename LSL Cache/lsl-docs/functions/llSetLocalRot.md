---
name: "llSetLocalRot"
category: "function"
type: "function"
language: "LSL"
description: "Sets the rotation of a child prim relative to the root prim"
signature: "void llSetLocalRot(rotation rot)"
return_type: "void"
sleep_time: "0.2"
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llSetLocalRot'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llsetlocalrot"]
---

Sets the rotation of a child prim relative to the root prim


## Signature

```lsl
void llSetLocalRot(rotation rot);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `rotation` | `rot` |  |


## Caveats

- Forced delay: **0.2 seconds** — the script sleeps after each call.
- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llSetLocalRot)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llSetLocalRot) — scraped 2026-03-18_

Sets the rotation of a child prim relative to the root prim

## Caveats

- This function causes the script to sleep for 0.2 seconds.

## Examples

Drop this script into a *child* prim to rotate it in 1 degree increments on each touch.

```lsl
rotation rot_xyzs;

default
{
    state_entry()
    {
        vector xyz_angles = <0,1.0,0>; // This defines a 1 degree change on the Y axis
        vector angles_in_radians = xyz_angles*DEG_TO_RAD; // Change to radians
        rot_xyzs = llEuler2Rot(angles_in_radians); // Convert to a rotation
    }

    touch_start(integer s)
    {
        llSetLocalRot(llGetLocalRot()*rot_xyzs); // Apply the increment rotation to the prim's current rotation ...

    }
}
```

## See Also

### Functions

- llGetRot
- llGetLocalRot
- llGetRootRotation
- llGetPrimitiveParams
- llGetLinkPrimitiveParams
- llSetRot
- llSetPrimitiveParams
- llSetLinkPrimitiveParams
- llSetLinkPrimitiveParamsFast

<!-- /wiki-source -->
