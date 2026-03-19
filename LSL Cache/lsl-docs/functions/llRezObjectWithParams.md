---
name: "llRezObjectWithParams"
category: "function"
type: "function"
language: "LSL"
description: 'Instantiate inventory object at pos with an initial set of parameters specified in params.

pos will default to the position of the object containing the script, unless REZ_POS is specified. (see below)Returns a key which will be the key of the object when it is successfully rezzed in the world.'
signature: "key llRezObjectWithParams(string itemname, list params)"
return_type: "key"
sleep_time: "0.1"
energy_cost: "200.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llRezObjectWithParams'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
---

Instantiate inventory object at pos with an initial set of parameters specified in params.

pos will default to the position of the object containing the script, unless REZ_POS is specified. (see below)Returns a key which will be the key of the object when it is successfully rezzed in the world.


## Signature

```lsl
key llRezObjectWithParams(string itemname, list params);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `string` | `inventory` | an object in the inventory of the prim this script is in |
| `list` | `params` |  |


## Return Value

Returns `key`.


## Caveats

- Forced delay: **0.1 seconds** — the script sleeps after each call.
- Energy cost: **200.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llRezObjectWithParams)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llRezObjectWithParams) — scraped 2026-03-18_

Instantiate inventory object at pos with an initial set of parameters specified in params.

## Caveats

- This function causes the script to sleep for 0.1 seconds.
- If inventory is missing from the prim's inventory   or it is not an object then an error is shouted on DEBUG_CHANNEL.
- Silently fails to rez inventory if REZ_POS is too far from the geometric center of the object trying to rez inventory (generally 10 meters; see llRezObject).
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

The list of parameters is entirely optional. If you want to rez an object exactly where the rezzer is, you may call the function with an empty list.

```lsl
default
{
    touch_start(integer total_number)
    {
        llRezObjectWithParams("Object", []);
    }
}
```

The below example rezzes an object slightly above the rezzer, slowly spinning and with automatic cleanup. See Temporary

```lsl
default
{
    touch_start(integer total_number)
    {
        llRezObjectWithParams("Object", [
            REZ_FLAGS, REZ_FLAG_TEMP | REZ_FLAG_PHANTOM,
            REZ_POS, <0,0,1>, TRUE, TRUE,
            REZ_OMEGA, <0,0,1>, TRUE, 0.5, PI
        ]);
    }
}
```

The below is a basic example of firing a typical bullet from a worn attachment. The bullet is fired with a left-click during mouselook.

```lsl
default
{
    control(key id, integer level, integer edge)
    {
        integer click = level & edge;

        if (click & CONTROL_ML_LBUTTON) {
            llRezObjectWithParams("Bullet", [
                REZ_POS, <2,0,0>, TRUE, TRUE, // Relative offset 2 meters forward
                REZ_ROT, ZERO_ROTATION, TRUE, // Relative rotation
                REZ_VEL, <100,0,0>, TRUE, FALSE, // Relative velocity 100m/s forward
                REZ_DAMAGE, 40,
                REZ_LOCK_AXES, <1,1,1>, // Disable all rotation
                REZ_FLAGS, 0
                | REZ_FLAG_PHYSICAL
                | REZ_FLAG_TEMP
                | REZ_FLAG_DIE_ON_COLLIDE
                | REZ_FLAG_DIE_ON_NOENTRY
                | REZ_FLAG_NO_COLLIDE_OWNER
                | REZ_FLAG_NO_COLLIDE_FAMILY
                | REZ_FLAG_BLOCK_GRAB_OBJECT
            ]);
        }
    }

    run_time_permissions(integer perm)
    {
        if (perm) {
            llTakeControls(CONTROL_ML_LBUTTON, TRUE, FALSE);
        }
    }

    attach(key id)
    {
        if (id) {
            llRequestPermissions(llGetOwner(), PERMISSION_TAKE_CONTROLS);
        }
    }

    state_entry()
    {
        if (llGetAttached()) {
            llRequestPermissions(llGetOwner(), PERMISSION_TAKE_CONTROLS);
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

- **llRezAtRoot** — Rezzes the object at the requested position
- **llRezObject** — Rezzes the object at the requested position
- llGetStartParameter
- llGodLikeRezObject
- **LlGetParcelFlags#Examples** — Test if the parcel allows this script to rez

<!-- /wiki-source -->
