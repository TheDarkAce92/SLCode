---
name: "llSetLinkCamera"
category: "function"
type: "function"
language: "LSL"
description: "Sets the camera eye offset, and the offset that camera is looking at, for avatars that sit on the linked prim."
signature: "void llSetLinkCamera(integer link, vector eye, vector at)"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llSetLinkCamera'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llsetlinkcamera"]
---

Sets the camera eye offset, and the offset that camera is looking at, for avatars that sit on the linked prim.


## Signature

```lsl
void llSetLinkCamera(integer link, vector eye, vector at);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `integer (link)` | `link` | Link number (0: unlinked, 1: root prim, >1: child prims and seated avatars) or a LINK_* flag |
| `vector` | `eye` | offset relative to the prim's position and expressed in local coordinates |
| `vector` | `at` | offset relative to the prim's position and expressed in local coordinates |


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llSetLinkCamera)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llSetLinkCamera) — scraped 2026-03-18_

Sets the camera eye offset, and the offset that camera is looking at, for avatars that sit on the linked prim.

## Caveats

- link needs to be either an actual link number or a link constants that equate to a single prim, such as LINK_ROOT and LINK_THIS.

  - LINK_SET, LINK_ALL_CHILDREN and LINK_ALL_OTHERS will not work.
- Setting this will not update the cameras of seated avatars, it will only effect avatars that subsequently sit down. The camera settings have to be prepared in advance.
- The offsets at and eye are locally relative to the prim, if you want it relative to the seated avatar (which likely has a custom sit rotation and offset) or the region, you must do the computation yourself.

Camera position and focus set by this function is a **Prim Property**. **It will survive the script** and it will survive prim taking and prim rezzing

## Examples

### Complex Examples

- Capture Camera View

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
- llSetCameraAtOffset
- llSetCameraEyeOffset
- llForceMouselook
- llSetCameraParams

<!-- /wiki-source -->
