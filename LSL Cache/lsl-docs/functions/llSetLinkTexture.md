---
name: "llSetLinkTexture"
category: "function"
type: "function"
language: "LSL"
description: 'If a prim exists in the link set at link, set Blinn-Phong diffuse texture on face of that prim.

If face is ALL_SIDES then the function works on all sides.'
signature: "void llSetLinkTexture(integer linknumber, string texture, integer face)"
return_type: "void"
sleep_time: "0.2"
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llSetLinkTexture'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llsetlinktexture"]
---

If a prim exists in the link set at link, set Blinn-Phong diffuse texture on face of that prim.

If face is ALL_SIDES then the function works on all sides.


## Signature

```lsl
void llSetLinkTexture(integer linknumber, string texture, integer face);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `integer` | `link` | Link number (0: unlinked, 1: root prim, >1: child prims and seated avatars) or a LINK_* flag |
| `string` | `texture` | a texture in the inventory of the prim this script is in or a UUID of a texture |
| `integer` | `face` | face number or ALL_SIDES |


## Caveats

- Forced delay: **0.2 seconds** — the script sleeps after each call.
- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llSetLinkTexture)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llSetLinkTexture) — scraped 2026-03-18_

If a prim exists in the link set at link, set Blinn-Phong diffuse texture on face of that prim.

## Caveats

- This function causes the script to sleep for 0.2 seconds.
- If texture is missing from the prim's inventory or not full permissions and it is not a UUID or it is not a texture then an error is shouted on DEBUG_CHANNEL.
- If texture is a UUID then there are no new asset permissions consequences for the object.

  - The resulting object develops no new usage restrictions that might have occurred if the asset had been placed in the prims inventory.
- The function silently fails if its face value indicates a face that does not exist.

## Examples

Cover a link set in the texture "bark" (from the library)

```lsl
default
{
    touch_start(integer detected)
    {
        llSetLinkTexture(LINK_SET, "66bf4030-04f9-a808-43ab-b48b6aeb6456", ALL_SIDES);
    }
}
```

## Notes

### Link Numbers

Each prim that makes up an object has an address, a link number. To access a specific prim in the object, the prim's link number must be known. In addition to prims having link numbers, avatars seated upon the object do as well.

- If an object consists of only one prim, and there are no avatars seated upon it, the (root) prim's link number is zero.
- However, if the object is made up of multiple prims or there is an avatar seated upon the object, the root prim's link number is one.

When an avatar sits on an object, it is added to the end of the link set and will have the largest link number. In addition to this, while an avatar is seated upon an object, the object is unable to link or unlink prims without unseating all avatars first.

#### Counting Prims & Avatars

There are two functions of interest when trying to find the number of prims and avatars on an object.

- `llGetNumberOfPrims()` - Returns the number of prims and seated avatars.
- `llGetObjectPrimCount(llGetKey())` - Returns only the number of prims in the object but will return zero for attachments.

```lsl
integer GetPrimCount() { //always returns only the number of prims
    if(llGetAttached())//Is it attached?
        return llGetNumberOfPrims();//returns avatars and prims but attachments can't be sat on.
    return llGetObjectPrimCount(llGetKey());//returns only prims but won't work on attachments.
}
```

See llGetNumberOfPrims for more about counting prims and avatars.

#### Errata

If a script located in a child prim erroneously attempts to access link 0, it will get or set the property of the linkset's root prim.  This bug ([BUG-5049](https://jira.secondlife.com/browse/BUG-5049)) is preserved for broken legacy scripts.

## See Also

### Functions

- **llGetLinkNumber** — prim
- **llGetLinkNumberOfSides** — Returns the number of faces of the linked prim.
- llSetLinkAlpha
- llSetLinkColor
- llSetLinkPrimitiveParams

### Articles

- Internal Textures

<!-- /wiki-source -->
