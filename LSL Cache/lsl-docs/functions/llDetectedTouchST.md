---
name: "llDetectedTouchST"
category: "function"
type: "function"
language: "LSL"
description: "Returns a vector that is the surface coordinates for where the prim was touched. The x & y vector positions contain the horizontal (s) & vertical (t) face coordinates respectively (<s, t, 0.0>). Each component is usually in the interval [0.0, 1.0] with the origin in the bottom left corner. With some"
signature: "vector llDetectedTouchST(integer number)"
return_type: "vector"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llDetectedTouchST'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["lldetectedtouchst"]
---

Returns a vector that is the surface coordinates for where the prim was touched. The x & y vector positions contain the horizontal (s) & vertical (t) face coordinates respectively (<s, t, 0.0>). Each component is usually in the interval [0.0, 1.0] with the origin in the bottom left corner. With some mesh objects, values of less than 0.0 and higher than 1.0 have been observed.

TOUCH_INVALID_TEXCOORD is returned when the surface coordinates cannot be determined. See Caveats for further details.

index does not support negative indexes.
For the touch category of events only. The prim that was touched may not be the prim receiving the event, use llDetectedLinkNumber to check for this; likewise, you can use llDetectedTouchFace to determine which face was touched.


## Signature

```lsl
vector llDetectedTouchST(integer number);
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

- [SL Wiki](https://wiki.secondlife.com/wiki/llDetectedTouchST)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llDetectedTouchST) — scraped 2026-03-18_

Returns a vector that is the surface coordinates for where the prim was touched. The x & y vector positions contain the horizontal (s) & vertical (t) face coordinates respectively (<s, t, 0.0>). Each component is usually in the interval [0.0, 1.0] with the origin in the bottom left corner.[1] With some mesh objects, values of less than 0.0 and higher than 1.0 have been observed.

## Caveats

- If index is out of bounds  the script continues to execute without an error message.
- TOUCH_INVALID_TEXCOORD is returned when...

  - The avatar's viewer does not support face touch detection.

  - To check if face touch detection is supported check the return of llDetectedTouchFace.
  - The touch has moved off the surface of the prim.
  - The touch happened too close to the edge of the face to determine a location.
  - The event triggered is not a touch event.
- The vertical coordinate is flipped on a glTF mesh.

## Examples

```lsl
default
{
    touch_start(integer total_number)
    {
        integer touchFace = llDetectedTouchFace(0);
        vector  touchST   = llDetectedTouchST(0);

//      ZERO_VECTOR (<0.0, 0.0, 0.0> ... the origin) is in the bottom left corner of the face
//      touchST.x goes across the face from the left to the right
//      touchST.y goes up the face from the bottom to the top

        if (touchFace == -1)
            llWhisper(PUBLIC_CHANNEL, "Sorry, your viewer doesn't support touched faces.");
        else if (touchST == TOUCH_INVALID_TEXCOORD)
            llWhisper(PUBLIC_CHANNEL, "Sorry, the touch position upon the face could not be determined.");
        else
            llSay(PUBLIC_CHANNEL, "llDetectedTouchST(0) = " + (string)touchST
                    + "\ntouchST.x = " + (string)touchST.x
                    + "\ntouchST.y = " + (string)touchST.y);
    }
}
```

The following script will assume an (imaginary) 12x12 grid over the face, and identify which square was touched by the user.

```lsl
integer numberOfRows    = 12;
integer numberOfColumns = 12;

default
{
    touch_start(integer total_number)
    {
        vector  touchST     = llDetectedTouchST(0);

//      ZERO_VECTOR (<0.0, 0.0, 0.0> ... the origin) is in the bottom left corner of the face
//      touchST.x goes across the face from the left to the right
//      touchST.y goes up the face from the bottom to the top

        integer columnIndex = (integer) (touchST.x * numberOfColumns);
        integer rowIndex    = (integer) (touchST.y * numberOfRows);
        integer cellIndex   = (rowIndex * numberOfColumns) + columnIndex;

        llSay(PUBLIC_CHANNEL, "ST grid (" + (string)columnIndex + ", " + (string)rowIndex
                            + ") --> cell " + (string)cellIndex);
    }
}
```

```lsl
//  with friendly permission of Supremius Maximus
//  who made the texture used in this script
//
//  click & hold the mouse while dragging across
//  the face of the prim

default
{
    touch(integer num_detected)
    {
        integer link    = llDetectedLinkNumber(0);
        integer face    = llDetectedTouchFace(0);
        vector  touchST = llDetectedTouchST(0);

//      ZERO_VECTOR (<0.0, 0.0, 0.0> ... the origin) is in the bottom left corner of the face
//      touchST.x goes across the face from the left to the right
//      touchST.y goes across the face from the bottom to the top

        string uuid = "23badbe7-6d8c-639b-0131-bb321f8e9db5";

        llSetLinkPrimitiveParamsFast(link, [
            PRIM_TEXTURE, face, uuid, <1.0, 1.0, 0.0>, touchST, 0,
            PRIM_FULLBRIGHT, ALL_SIDES, TRUE]);
    }
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
- llDetectedTouchUV
- llDetectedTouchPos
- llDetectedTouchNormal
- llDetectedTouchBinormal

### Articles

- Detected

<!-- /wiki-source -->
