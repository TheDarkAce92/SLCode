---
name: "llGetRot"
category: "function"
type: "function"
language: "LSL"
description: "Returns a rotation that is the prim's rotation relative to the region's axes."
signature: "rotation llGetRot()"
return_type: "rotation"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetRot'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgetrot"]
---

Returns a rotation that is the prim's rotation relative to the region's axes.


## Signature

```lsl
rotation llGetRot();
```


## Return Value

Returns `rotation`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetRot)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetRot) — scraped 2026-03-18_

Returns a rotation that is the prim's rotation relative to the region's axes.

## Caveats

- llGetRot incorrectly reports the avatars rotation when called from the root of an attached object, use llGetLocalRot for root prims, instead

  - llGetRot will return an accurate facing for Avatars seated or in mouselook, but only a rough direction otherwise when called from an attached prim.
  - When called in an attachment's child prim, the reported rotation will only be visually correct if the object's root is attached to ATTACH_AVATAR_CENTER, at ZERO_ROTATION. Moving the attachment's root or changing the attachment point will not affect the reported rotation. Avatar animation is invisible to the simulator, so it also does not affect the reported rotation. Also see Single or Root Prims vs Linked Prims vs Attachments.

## Examples

```lsl
 //-- rotates an object to face the nearest cardinal direction (N,E,S,W)
 //-- assumes build is aligned to root object facing

default{
  state_entry()
  {
    llSay( 0, "Rotate me in edit, then touch to make me face the nearest compass point" );
  }

  touch_start( integer vIntTouches )
  {
     //-- convert our rotation to x/y/z radians
    vector vRadBase = llRot2Euler( llGetRot() );
     //-- round the z-axis to the nearest 90deg (PI_BY_TWO = 90deg in radians)
    llSetRot( llEuler2Rot( <0.0, 0.0, llRound( vRadBase.z / PI_BY_TWO ) * PI_BY_TWO > ) );
  }
}
```

## See Also

### Functions

- llGetLocalRot
- llGetRootRotation
- llGetPrimitiveParams
- llSetRot
- llSetLocalRot
- llSetPrimitiveParams
- llSetLinkPrimitiveParams
- llSetLinkPrimitiveParamsFast

<!-- /wiki-source -->
