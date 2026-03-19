---
name: "llRezObject"
category: "function"
type: "function"
language: "LSL"
description: 'Instantiate inventory object at pos with velocity vel and rotation rot with start parameter param

The root of inventory is not at pos but the center of inventory is.
To have the root prim at pos use llRezAtRoot instead.'
signature: "void llRezObject(string inventory, vector pos, vector vel, rotation rot, integer param)"
return_type: "void"
sleep_time: "0.1"
energy_cost: "200.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llRezObject'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llrezobject"]
---

Instantiate inventory object at pos with velocity vel and rotation rot with start parameter param

The root of inventory is not at pos but the center of inventory is.
To have the root prim at pos use llRezAtRoot instead.


## Signature

```lsl
void llRezObject(string inventory, vector pos, vector vel, rotation rot, integer param);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `string` | `inventory` | an object in the inventory of the prim this script is in |
| `vector` | `pos` | position in region coordinates |
| `vector` | `vel` | velocity (max magnitude is approximately 200m/s) |
| `rotation` | `rot` | rotation |
| `integer` | `param` | on_rez event parameter and value returned by llGetStartParameter in the rezzed object (or by each of the items in a coalesced object). |


## Caveats

- Forced delay: **0.1 seconds** — the script sleeps after each call.
- Energy cost: **200.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llRezObject)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llRezObject) — scraped 2026-03-18_

Instantiate inventory object at pos with velocity vel and rotation rot with start parameter param

## Caveats

- This function causes the script to sleep for 0.1 seconds.
- If inventory is missing from the prim's inventory   or it is not an object then an error is shouted on DEBUG_CHANNEL.
- Silently fails to rez inventory (to have it's geometric center at pos) if pos is too far from the geometric center of the object trying to rez inventory.

  - If your script is mysteriously failing to rez things, make sure you haven't (say) written "`<0.0,0.0,1.0>`" for the pos parameter rather than (say) `llGetPos() + <0.0,0.0,1.0>`".
- When scripting attachments meant to rez objects, remember that when used in the root of an (attached) attachment `llGetPos` doesn't return the position of the attachment but instead returns the position of the avatar's bounding box geometric center. Read llGetPos and llParticleSystem Caveats for more information.
- If the object is unattached and the owner of the object does not have copy permission  on inventory, the object will no longer be present in inventory after it is rezzed (so another attempt to rez (the same object) will fail); if the owner does have copy permission, then a copy is rezzed, and the original inventory remains in inventory.
- If the object is attached and the owner of the object does not have copy permission  on inventory, an error is shouted on DEBUG_CHANNEL: "Cannot rez no copy objects from an attached object."
- Silently fails if you don't have offline building rights on the land. To have the right, your objects needs to *either*:

  - Be on land you own yourself.
  - Be on land where anyone is allowed to build, e.g. a sandbox.
  - Be deeded to the group that owns the land.
  - Be set to the same group that owns the land and the land have the parcel flag 'allow group to build' set.
  - The group role "Always allow 'Create Objects'" will only work to override this when you are online, in the region, or have a child agent in the region. See SVC-3145 in the Issues subsection of Deep Notes for more information.
- See object_rez for examples on how to establish communications between the rezzing object and the new prim.

## Examples

```lsl
default
{
     touch_start(integer param)
     {
          llRezObject("Object", llGetPos() + <0.0,0.0,1.0>, <0.0,0.0,0.0>, <0.0,0.0,0.0,1.0>, 0);
     }
}
```

```lsl
// Rez an object on touch, with relative position, rotation, and velocity all described in the rezzing prim's coordinate system.
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

        llRezObject(object, rezPos, rezVel, rezRot, startParam);
    }
}
```

## Notes

**Maximum rez distance**

- After tests on server 1.38, these figures were measured - (on some earlier server versions the same *further-than-10-meter* rezzes have been possible).
- The distance measured is between the center of the rezzing prim and the center of the prim that is rezzed.

  - The tests did not include rezzing from or the rezzing of link_set objects.
  - A `10.0` meter cube could rez a `0.5` meter cube just beyond `18.6` meters away.
  - A `0.01` cube could rez a `0.5` meter cube just beyond `10.0` meters away.

## See Also

### Constants

- PRIM_TEMP_ON_REZ

### Events

- **object_rez** — triggered when this object rezzes an object from inventory

### Functions

- **llRezAtRoot** — Rezzes the object at the requested position
- llGetStartParameter
- llGodLikeRezObject
- **LlGetParcelFlags#Examples** — Test if the parcel allows this script to rez

<!-- /wiki-source -->
