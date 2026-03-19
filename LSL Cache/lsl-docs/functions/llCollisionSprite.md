---
name: "llCollisionSprite"
category: "function"
type: "function"
language: "LSL"
description: 'Suppress default collision sprites, replace default impact sprite with impact_sprite

To suppress the collision sprite all together, just use an empty string as the value for impact_sprite'
signature: "void llCollisionSprite(string impact_sprite)"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llCollisionSprite'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
flags: "broken"
---

Suppress default collision sprites, replace default impact sprite with impact_sprite

To suppress the collision sprite all together, just use an empty string as the value for impact_sprite


## Signature

```lsl
void llCollisionSprite(string impact_sprite);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `string` | `impact_sprite` | a texture in the inventory of the prim this script is in, a UUID of a texture or an empty string |


## Caveats

- Energy cost: **10.0**.
- ⚠️ **Marked as broken** in LSL tooling data — verify current behaviour on the SL wiki.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llCollisionSprite)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llCollisionSprite) — scraped 2026-03-18_

Suppress default collision sprites, replace default impact sprite with impact_sprite

## Caveats

- If impact_sprite is not an empty string and...

  - impact_sprite is missing from the prim's inventory  and it is not a UUID or it is not a texture then an error is shouted on DEBUG_CHANNEL.
- If impact_sprite is a UUID then there are no new asset permissions consequences for the object.

  - The resulting object develops no new usage restrictions that might have occurred if the asset had been placed in the prims inventory.

## See Also

### Events

- collision_start
- collision
- collision_end

### Functions

- llCollisionFilter
- llCollisionSound

<!-- /wiki-source -->
