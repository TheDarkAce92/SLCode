---
name: "llDetectedTouchPos"
category: "function"
type: "function"
language: "LSL"
description: 'Returns the vector position where the object was touched in region coordinates, unless it is attached to the HUD, in which case it returns the position in screen space coordinates.

index does not support negative indexes.
For the touch category of events only. The prim that was touched may not be t'
signature: "vector llDetectedTouchPos(integer number)"
return_type: "vector"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llDetectedTouchPos'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["lldetectedtouchpos"]
---

Returns the vector position where the object was touched in region coordinates, unless it is attached to the HUD, in which case it returns the position in screen space coordinates.

index does not support negative indexes.
For the touch category of events only. The prim that was touched may not be the prim receiving the event, use llDetectedLinkNumber to check for this; likewise you can use llDetectedTouchFace to determine which face was touched.


## Signature

```lsl
vector llDetectedTouchPos(integer number);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `integer` | `index` | Index of detection information |


## Return Value

Returns `vector`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llDetectedTouchPos)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llDetectedTouchPos) — scraped 2026-03-18_

Returns the vector position where the object was touched in region coordinates, unless it is attached to the HUD, in which case it returns the position in screen space coordinates.

## Caveats

- HUD attachments currently return coordinates relative to the *center of the screen* rather than the attachment point. [SVC-3425](https://jira.secondlife.com/browse/SVC-3425)
- If index is out of bounds  the script continues to execute without an error message.
- TOUCH_INVALID_VECTOR is returned when...

  - The avatar's viewer does not support face touch detection.

  - To check if face touch detection is supported check the return of llDetectedTouchFace.
  - The touch has moved off the surface of the prim.
  - The event triggered is not a touch event.

## Examples

```lsl
default
{
    touch_start(integer num_detected)
    {
        llWhisper(0, "Pos clicked: " + (string)llDetectedTouchPos(0));
    }
}
```

```lsl
vector GetRealTouchPos(vector pos)
{
//  By Ariu Arai for free use to anyone
//  Returns a useful HUD Position Vector from the llDetectedTouchPos(); function
//  USE: vector pos = GetRealTouchPos(llDetectedTouchPos(0)); .. Etc.
//  This function is intended to be used to move child prims to where the user clicks. This does not work on the root prim.

    integer point = llGetAttached();
    vector offset;

    if      (point == ATTACH_HUD_TOP_RIGHT)    offset = <1.0, 0.933,-0.5>;
    else if (point == ATTACH_HUD_TOP_CENTER)   offset = <1.0, 0.000,-0.5>;
    else if (point == ATTACH_HUD_TOP_LEFT)     offset = <1.0,-0.933,-0.5>;
    else if (point == ATTACH_HUD_BOTTOM_LEFT)  offset = <1.0,-0.933, 0.5>;
    else if (point == ATTACH_HUD_BOTTOM)       offset = <1.0, 0.000, 0.5>;
    else if (point == ATTACH_HUD_BOTTOM_RIGHT) offset = <1.0, 0.933, 0.5>;

    //return (pos - llGetLocalPos()) + (offset * llGetLocalRot());
    return ((offset - llGetLocalPos()) + pos) / llGetLocalRot();
}
```

## See Also

### Events

- touch_start
- touch
- touch_end

### Functions

- llDetectedLinkNumber
- llDetectedTouchFace
- llDetectedTouchST
- llDetectedTouchUV
- llDetectedTouchNormal
- llDetectedTouchBinormal

### Articles

- Detected

<!-- /wiki-source -->
