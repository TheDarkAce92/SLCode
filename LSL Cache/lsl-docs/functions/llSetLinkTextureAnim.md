---
name: "llSetLinkTextureAnim"
category: "function"
type: "function"
language: "LSL"
description: 'Animate the texture on the specified face/faces of the specified prim/prims by setting the texture scale and offset.

Identical to llSetTextureAnim except able to modify any prim in the link set.

If face is ALL_SIDES then the function works on all sides.
start supports negative indexes.
Frames are '
signature: "void llSetLinkTextureAnim(integer link, integer mode, integer face, integer sizex, integer sizey, float start, float length, float rate)"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llSetLinkTextureAnim'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llsetlinktextureanim"]
---

Animate the texture on the specified face/faces of the specified prim/prims by setting the texture scale and offset.

Identical to llSetTextureAnim except able to modify any prim in the link set.

If face is ALL_SIDES then the function works on all sides.
start supports negative indexes.
Frames are numbered from left to right, top to bottom, starting at 0.
If rate is negative, it has the same effect as using the REVERSE flag.
If length is 0, it is considered to be sizex*sizey if both are above 0, otherwise 1.


## Signature

```lsl
void llSetLinkTextureAnim(integer link, integer mode, integer face, integer sizex, integer sizey, float start, float length, float rate);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `integer (link)` | `link` | Link number (0: unlinked, 1: root prim, >1: child prims and seated avatars) or a LINK_* flag to effect |
| `integer (texture_anim)` | `mode` | bit field of Mode flags |
| `integer` | `face` | face number or ALL_SIDES |
| `integer` | `sizex` | horizontal frames (ignored for ROTATE and SCALE) |
| `integer` | `sizey` | vertical frames (ignored for ROTATE and SCALE) |
| `float` | `start` | Start position/frame number (or radians for ROTATE) |
| `float` | `length` | number of frames to display (or radians for ROTATE) |
| `float` | `rate` | Frames per second, or radians per second when ROTATE is set, or UV coordinates when SMOOTH is set (must not be zero) |


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llSetLinkTextureAnim)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llSetLinkTextureAnim) — scraped 2026-03-18_

Animate the texture on the specified face/faces of the specified prim/prims by setting the texture scale and offset. Identical to llSetTextureAnim except able to modify any prim in the link set.

## Caveats

- The function silently fails if its face value indicates a face that does not exist.
- If start is out of bounds  the script continues to execute without an error message.
- You can only have one texture animation on a prim.

  - Calling llSetLinkTextureAnim more than once on a prim will reset it.
  - Calling llSetLinkTextureAnim again with exact same values will not reset animation (a small difference in rate will suffice).
- You cannot combine ROTATE and SCALE flags.
- sizex and sizey are both limited to a range of 0 to 255

  - Negative sizes behave as if texture repeats were set to 0, and cannot be used to mirror frames.
- Different animation modes override some of the prim's texture parameters, but others can still be used:

  - Texture offsets are ignored in frame-based and SMOOTH scrolling modes.

  - Repeats are ignored if sizex and sizey are not 0.
  - With either of the sizes set to 0, SMOOTH scrolling will use the prim's texture repeats. In frame-based animation, there is no meaningful effect.
  - The texture rotation is ignored in ROTATE mode.
  - Texture repeats are ignored in SCALE mode
- Selecting and un-selecting a prim with animation will reset animation from beginning.
- While a texture animation is active on any face of a prim, PRIM_NORMAL and PRIM_SPECULAR are forced to have their repeats, rotations and offsets to match the PRIM_TEXTURE ones, even on faces that are **not** being animated.
- As of server version 2025-09-03.17442317385, this prim property is maintained when copying in-world.

## Examples

This slides a texture smoothly, along the horizontal U-axis, and loops it when it gets to the end.

For Blinn-Phong materials, the texture's rotation for each side affects the apparent motion. So if the texture is rotated 90 degrees by use of the edit box, the texture may not flow in the direction expected.

For PBR materials, the Blinn-Phong texture rotation for each side affects the apparent motion, and any Blinn-Phong transform component (for example the offsets argument of PRIM_TEXTURE) which is not animated will be applied to the PBR material as well. Thus, a GLTF material without a GLTF texture transform will animate identically to a Blinn-Phong material. If a GLTF texture transform (for example PRIM_GLTF_BASE_COLOR) is applied, it will be in addition to the Blinn-Phong transform and texture animation. This allows for more flexibility, however a more complex GLTF texture transform will not loop as easily.

```lsl
llSetLinkTextureAnim(LINK_THIS, ANIM_ON | SMOOTH | LOOP , ALL_SIDES, 1, 1, 1, 1, 1);
```

This slides a texture smoothly, along the horizontal U-axis, in the opposite direction

```lsl
llSetLinkTextureAnim(LINK_THIS, ANIM_ON | SMOOTH | LOOP , ALL_SIDES, 1, 1, 1, 1, -1);
```

This divides a texture into 64 "cells", 8 across, and 8 down, and flips through them, left to right, top to bottom. This is useful for cell animation.

```lsl
llSetLinkTextureAnim(LINK_THIS, ANIM_ON | LOOP, ALL_SIDES, 8, 8, 0, 64, 6.4 );
```

This rotates a texture counter-clockwise at 2 revolutions per second. Change the last value to -2*TWO_PI to rotate clockwise.

```lsl
llSetLinkTextureAnim(LINK_THIS, ANIM_ON | SMOOTH | ROTATE | LOOP, ALL_SIDES,1,1,0, TWO_PI, 2*TWO_PI);
```

This scales a texture larger and smaller.

```lsl
llSetLinkTextureAnim(LINK_THIS, ANIM_ON | SMOOTH | SCALE | PING_PONG | LOOP, ALL_SIDES, 1, 1, 1, 3, 2);
```

This turns off all texture animations

```lsl
llSetLinkTextureAnim(LINK_THIS, FALSE, ALL_SIDES, 0, 0, 0.0, 0.0, 1.0);
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
Texture animation is a property of the prim (i.e., you can remove the script that started the animation, and the prim will remember the settings anyway.)

## See Also

### Functions

- **llGetLinkNumber** — prim
- **llSetTextureAnim** — Set texture animation for the prim the script is on.

### Articles

- Negative Index

<!-- /wiki-source -->
