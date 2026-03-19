---
name: "llCollisionSound"
category: "function"
type: "function"
language: "LSL"
description: 'Suppress default collision sounds, replace default impact sounds with impact_sound at the volume impact_volume

If impact_sound is an empty string then the collision sound is suppressed.
If impact_volume is set to zero the collision particles are suppressed.'
signature: "void llCollisionSound(string impact_sound, float impact_volume)"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llCollisionSound'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llcollisionsound"]
---

Suppress default collision sounds, replace default impact sounds with impact_sound at the volume impact_volume

If impact_sound is an empty string then the collision sound is suppressed.
If impact_volume is set to zero the collision particles are suppressed.


## Signature

```lsl
void llCollisionSound(string impact_sound, float impact_volume);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `string` | `impact_sound` | a sound in the inventory of the prim this script is in, a UUID of a sound or an empty string |
| `float` | `impact_volume` | between 0.0 (silent) and 1.0 (loud) (0.0 <= impact_volume <= 1.0) |


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llCollisionSound)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llCollisionSound) — scraped 2026-03-18_

Suppress default collision sounds, replace default impact sounds with impact_sound at the volume impact_volume

## Caveats

- If impact_sound is not an empty string and...

  - impact_sound is missing from the prim's inventory  and it is not a UUID or it is not a sound then an error is shouted on DEBUG_CHANNEL.
- If impact_sound is a UUID then there are no new asset permissions consequences for the object.

  - The resulting object develops no new usage restrictions that might have occurred if the asset had been placed in the prims inventory.
- If this function is used to suppress collision sounds, NO sound will be generated even if the suppressed object collides with an unsuppressed object (there will be no sound from the unsuppressed object either).

## Examples

```lsl
//Play Sound When Collision Occurs With Other Object Or An AGENT
//Creator: TonyH Wrangler

string sound = "ed124764-705d-d497-167a-182cd9fa2e6c"; //uuid or name of item in inventory

default
{
    state_entry()
    {
        llCollisionSound(sound, 1.0);
    }
}
```

## See Also

### Events

- collision_start
- collision
- collision_end

### Functions

- llCollisionFilter
- llCollisionSprite

<!-- /wiki-source -->
