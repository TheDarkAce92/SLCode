---
name: "llSetLinkColor"
category: "function"
type: "function"
language: "LSL"
description: 'If a prim exists in the link set at link, set the Blinn-Phong color on face of that prim.

If face is ALL_SIDES then the function works on all sides.'
signature: "void llSetLinkColor(integer linknumber, vector color, integer face)"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llSetLinkColor'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llsetlinkcolor"]
---

If a prim exists in the link set at link, set the Blinn-Phong color on face of that prim.

If face is ALL_SIDES then the function works on all sides.


## Signature

```lsl
void llSetLinkColor(integer linknumber, vector color, integer face);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `integer (link)` | `link` | Link number (0: unlinked, 1: root prim, >1: child prims and seated avatars) or a LINK_* flag |
| `vector` | `color` | color in RGB <R, G, B> (<0.0, 0.0, 0.0> = black, <1.0, 1.0, 1.0> = white) |
| `integer` | `face` | face number or ALL_SIDES |


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llSetLinkColor)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llSetLinkColor) — scraped 2026-03-18_

If a prim exists in the link set at link, set the Blinn-Phong color on face of that prim.

## Caveats

- The function silently fails if its face value indicates a face that does not exist.
- llSetLinkColor will have no visible effect on faces with a PBR material. To work on faces both with and without a PBR material, use this snippet:

```lsl
llSetLinkColor(LINK_THIS, color, ALL_SIDES);
llSetLinkPrimitiveParamsFast(LINK_THIS, [PRIM_GLTF_BASE_COLOR, ALL_SIDES, "", "", "", "", llsRGB2Linear(color), "", "", "", ""]);
```

## Examples

Turn a link set green

```lsl
default
{
    touch_start(integer detected)
    {
        llSetLinkColor(LINK_SET, <0.0, 1.0, 0.0>, ALL_SIDES);
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

### Events

- **changed** — CHANGED_COLOR

### Functions

- **llGetLinkNumber** — prim
- **llGetLinkNumberOfSides** — Returns the number of faces of the linked prim.
- **llGetAlpha** — Gets the prim's alpha
- **llSetAlpha** — Sets the prim's alpha
- **llGetColor** — Gets the prim's color
- **llSetColor** — Sets the prim's color
- llSetLinkAlpha
- llSetLinkTexture
- llSetLinkPrimitiveParams
- **PRIM_COLOR** — llSetPrimitiveParams
- **PRIM_GLTF_BASE_COLOR** — llSetPrimitiveParams

### Articles

- Color in LSL
- Color and Scripting

<!-- /wiki-source -->
