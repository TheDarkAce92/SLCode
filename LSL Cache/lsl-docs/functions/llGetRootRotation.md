---
name: "llGetRootRotation"
category: "function"
type: "function"
language: "LSL"
description: "Returns a rotation that is the region rotation of the root prim of the object."
signature: "rotation llGetRootRotation()"
return_type: "rotation"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetRootRotation'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgetrootrotation"]
---

Returns a rotation that is the region rotation of the root prim of the object.


## Signature

```lsl
rotation llGetRootRotation();
```


## Return Value

Returns `rotation`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetRootRotation)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetRootRotation) — scraped 2026-03-18_

Returns a rotation that is the region rotation of the root prim of the object.

## Caveats

- Returns an accurate facing for Avatars seated or in mouselook, but only a rough direction otherwise when called from an attached prim.
- When a seated avatar is in mouselook, its rotation is affected by the camera's rotation. There is no way to get the actual rotation of an avatar while seated in mouselook.
- This function incorrectly (but usefully) returns the avatars region rotation when called in an attachment, use the following instead:

```lsl
//  if called only from the root
    llGetLocalRot();
//  if called from in a linked object
    llList2Rot( llGetLinkPrimitiveParams( LINK_ROOT, [PRIM_ROT_LOCAL] ), 0 );
//  this alternative works correctly in all scenarios
    llList2Rot( llGetLinkPrimitiveParams( !!llGetLinkNumber(), [PRIM_ROT_LOCAL] ), 0 );
```

## Examples

Simple example to set region rotation of child prim in unattached link set

```lsl
default
{
  state_entry()
  {
    //Rotate 45 degrees about Y-axis
    rotation globalRot = llEuler2Rot(<0.0, 45.0, 0.0> * DEG_TO_RAD);
    llSetLocalRot(globalRot / llGetRootRotation());
  }
}
```

## Notes

In an attached object, returns region rotation of avatar NOT of the object's root prim.  See special cases of rotation.

## See Also

### Functions

- llGetRot
- llGetLocalRot
- llGetPrimitiveParams
- llGetLinkPrimitiveParams

<!-- /wiki-source -->
