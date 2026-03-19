---
name: "llSetCameraAtOffset"
category: "function"
type: "function"
language: "LSL"
description: 'Sets the point the camera is looking at to offset for avatars that sit on the object.

This is the point the camera looks at, not the position of the camera's eye.'
signature: "void llSetCameraAtOffset(vector offset)"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llSetCameraAtOffset'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llsetcameraatoffset"]
---

Sets the point the camera is looking at to offset for avatars that sit on the object.

This is the point the camera looks at, not the position of the camera's eye.


## Signature

```lsl
void llSetCameraAtOffset(vector offset);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `vector` | `offset` | offset relative to the prim's position and expressed in local coordinates |


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llSetCameraAtOffset)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llSetCameraAtOffset) — scraped 2026-03-18_

Sets the point the camera is looking at to offset for avatars that sit on the object.

## Caveats

- Setting this will not update the cameras of seated avatars, it will only effect avatars that subsequently sit down. The camera settings have to be prepared in advance.
- The offset is locally relative to the object, if you want it relative to the seated avatar (which likely has a custom sit rotation and offset) or the region, you must do the computation yourself.
- ZERO_VECTOR offset will cancel any offset.
- Camera focus set by this function is a **Prim Property**. **It will survive the script** and it will survive prim taking and prim rezzing

## Examples

```lsl
// Set the seated avatar looking at an arbitrary direction
// Look over the avatar's shoulders from behind once it sits down

back_view(float degrees)
{
     rotation sitRot = llAxisAngle2Rot(<0, 0, 1>, degrees * DEG_TO_RAD);

     llSitTarget(<0, 0, 0.1>, sitRot);

     llSetCameraEyeOffset(<-2, 0, 1> * sitRot);
     llSetCameraAtOffset(<2, 0, 1> * sitRot);
}

default
{
    state_entry()
    {
        back_view( 208 );
        llSay(0, "Please sit down");
    }
}
```

## See Also

### Functions

- llSetLinkCamera
- llSetCameraEyeOffset
- llForceMouselook
- llSetCameraParams

<!-- /wiki-source -->
