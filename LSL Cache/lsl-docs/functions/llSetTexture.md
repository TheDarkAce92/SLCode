---
name: "llSetTexture"
category: "function"
type: "function"
language: "LSL"
description: 'Sets the Blinn-Phong diffuse texture of this prim's face.

If face is ALL_SIDES then the function works on all sides.'
signature: "void llSetTexture(string texture, integer face)"
return_type: "void"
sleep_time: "0.2"
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llSetTexture'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llsettexture"]
---

Sets the Blinn-Phong diffuse texture of this prim's face.

If face is ALL_SIDES then the function works on all sides.


## Signature

```lsl
void llSetTexture(string texture, integer face);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `string` | `texture` | a texture in the inventory of the prim this script is in or a UUID of a texture |
| `integer` | `face` | face number or ALL_SIDES |


## Caveats

- Forced delay: **0.2 seconds** — the script sleeps after each call.
- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llSetTexture)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llSetTexture) — scraped 2026-03-18_

Sets the Blinn-Phong diffuse texture of this prim's face.

## Caveats

- This function causes the script to sleep for 0.2 seconds.
- The function silently fails if its face value indicates a face that does not exist.
- If texture is missing from the prim's inventory  and it is not a UUID or it is not a texture then an error is shouted on DEBUG_CHANNEL.
- If texture is a UUID then there are no new asset permissions consequences for the object.

  - The resulting object develops no new usage restrictions that might have occurred if the asset had been placed in the prims inventory.
- Inspect does not show texture information (like creator)

## Examples

```lsl
default
{
    state_entry()
    {
        // the first texture alphabetically inside the same prim's inventory
        string texture = llGetInventoryName(INVENTORY_TEXTURE, 0);

        // set it on all sides of the prim containing the script
        llSetTexture(texture, ALL_SIDES);
    }
}
```

## See Also

### Functions

- llSetLinkTexture
- llGetTexture
- llSetPrimitiveParams
- llSetLinkPrimitiveParams

### Articles

- Internal Textures

<!-- /wiki-source -->
