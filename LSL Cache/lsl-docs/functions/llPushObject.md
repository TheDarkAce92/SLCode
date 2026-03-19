---
name: "llPushObject"
category: "function"
type: "function"
language: "LSL"
description: "Applies impulse and ang_impulse to object target"
signature: "void llPushObject(key id, vector impulse, vector ang_impulse, integer local)"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llPushObject'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llpushobject"]
---

Applies impulse and ang_impulse to object target


## Signature

```lsl
void llPushObject(key id, vector impulse, vector ang_impulse, integer local);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `key` | `target` | avatar or object UUID that is in the same region |
| `vector` | `impulse` | Direction and force of push. Direction is affected by local. |
| `vector` | `ang_impulse` | Rotational force. |
| `integer` | `local` | boolean, if TRUE uses the local axis of target, if FALSE uses the region axis. |


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llPushObject)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llPushObject) — scraped 2026-03-18_

Applies impulse and ang_impulse to object target

## Caveats

- Only works on land where Push is not restricted or where the script is owned by the land owner.

  - If the land is owned by a group, the scripted object must be deeded to the same group.
  - In no-push areas an object can only push its owner or itself.
- The effectiveness of Push is modulated by the amount of script energy available.

  - There is a simplified code snippet describing how Push is implemented in the Havok4 project and reveals some of the details of how the energy budget affects the final Push magnitude.
- ang_impulse is ignored when applying to agents or their attachments.
- Energy is fully depleted by this function when either impulse or ang_impulse is nonzero.  If impulse is nonzero, it will drain all energy in the object before ang_impulse is processed, causing the push to be purely linear.
- The push impact is diminished with distance by a factor of distance cubed.

## Examples

```lsl
// Pushes the collided object or avatar.
default
{
    collision_start(integer num_detected)
    {
        llPushObject(llDetectedKey(0),<0,0,100>, <0,0,100>, TRUE);
    }
}
```

<!-- /wiki-source -->
