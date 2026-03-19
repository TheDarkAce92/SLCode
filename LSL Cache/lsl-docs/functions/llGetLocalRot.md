---
name: "llGetLocalRot"
category: "function"
type: "function"
language: "LSL"
description: 'Returns the rotation of the prim relative to the root.

If called from the root prim, it returns the objects rotation.'
signature: "rotation llGetLocalRot()"
return_type: "rotation"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetLocalRot'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgetlocalrot"]
---

Returns the rotation of the prim relative to the root.

If called from the root prim, it returns the objects rotation.


## Signature

```lsl
rotation llGetLocalRot();
```


## Return Value

Returns `rotation`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetLocalRot)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetLocalRot) — scraped 2026-03-18_

Returns the rotation of the prim relative to the root.

## Examples

```lsl
 //--// Door Script - Works At ANY Angle //--//

//-- works in ANY single prim door, linked or un-linked
//-- works in muti prim doors NOT linked to a larger structure
//-- REQUIREMENTS: a cut root prim. Suggest cube, pathcut start=.125, end=.625
//-- CAVEAT: single prim doors are limited to 5m width

 //--// USERS MODIFY HERE v
integer vgIntDoorSwing = 90;
//-- use -# to reverse the direction of swing, eg. -90;

rotation gRotDoorSwing;

default{
  state_entry(){
    gRotDoorSwing = llEuler2Rot( <0.0, 0.0, vgIntDoorSwing> * DEG_TO_RAD );
  }

  touch_start( integer vIntTouched ){
    llSetLocalRot( (gRotDoorSwing = ZERO_ROTATION / gRotDoorSwing) * llGetLocalRot() );
  }
}
```

## Notes

Returns the region relative rotation of the object if called from the root

## See Also

### Functions

- llGetRot
- llGetRootRotation
- llGetPrimitiveParams
- llGetLinkPrimitiveParams
- llSetRot
- llSetLocalRot
- llSetPrimitiveParams
- llSetLinkPrimitiveParams
- llSetLinkPrimitiveParamsFast

<!-- /wiki-source -->
