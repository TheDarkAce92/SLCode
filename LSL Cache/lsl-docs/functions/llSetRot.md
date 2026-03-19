---
name: "llSetRot"
category: "function"
type: "function"
language: "LSL"
description: "Sets the rotation of the prim to rot."
signature: "void llSetRot(rotation rot)"
return_type: "void"
sleep_time: "0.2"
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llSetRot'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llsetrot"]
---

Sets the rotation of the prim to rot.


## Signature

```lsl
void llSetRot(rotation rot);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `rotation` | `rot` |  |


## Caveats

- Forced delay: **0.2 seconds** — the script sleeps after each call.
- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llSetRot)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llSetRot) — scraped 2026-03-18_

Sets the rotation of the prim to rot.

## Caveats

- This function causes the script to sleep for 0.2 seconds.
- If the prim is attached, then this function offsets the rotation by the avatar's rotation.
- If the prim is not the root prim it is offset by the root's rotation.

  - If you are trying to set the rotation of a child prim relative to the root prim then divide the rotation by the root rotation.
  - If you are trying to set the rotation of a child prim to a global rotation then you need to divide the global rotation by the root rotation **twice**.
  - It is better to use llSetLocalRot to set the rotation of child prims, even if you are setting it to a global rotation (just divide by the root rotation in that case).
  - Alternatively see the Useful Snippets for generalized workarounds that work with llSetPrimitiveParams, llSetLinkPrimitiveParams, and llSetLinkPrimitiveParamsFast
- For small rotation changes, there is an update threshold depending on the time duration between changes. It does not appear to be limited to the 6deg rule any longer.
- For "static objects" (type of pathfinding), the script fails with the error in debug channel:

  - "Unable to set prim rotation: object contributes to the navmesh."

## Examples

Drop this script in the root prim of an object to have it rotate in 1 degree increments. Note that it won't work on child prims if the root is rotated.

```lsl
rotation rot_xyzq;

default
{
    state_entry()
    {
        vector xyz_angles = <0,1.0,0>; // This is to define a 1 degree change
        vector angles_in_radians = xyz_angles*DEG_TO_RAD; // Change to Radians
        rot_xyzq = llEuler2Rot(angles_in_radians); // Change to a Rotation
    }

    touch_start(integer s)
    {
        llSetRot(llGetRot()*rot_xyzq); //Do the Rotation...
    }
}
```

Drop this one in a child prim to have it rotate around the world's Y axis in 1 degree increments. It won't work in the root if it is rotated.

```lsl
rotation rot_xyzq;

default
{
    state_entry()
    {
        vector xyz_angles = <0,1.0,0>; // This is to define a 1 degree change
        vector angles_in_radians = xyz_angles*DEG_TO_RAD; // Change to Radians
        rot_xyzq = llEuler2Rot(angles_in_radians); // Change to a Rotation
    }

    touch_start(integer s)
    {
        llSetRot(llGetRot()*rot_xyzq/llGetRootRotation()/llGetRootRotation()); //Do the Rotation...
    }
}
```

## See Also

### Functions

- llGetRot
- llGetLocalRot
- llGetPrimitiveParams
- llGetLinkPrimitiveParams
- llSetLocalRot
- llSetPrimitiveParams
- llSetLinkPrimitiveParams
- llSetLinkPrimitiveParamsFast
- llTargetOmega

<!-- /wiki-source -->
