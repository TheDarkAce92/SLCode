---
name: "llDetectedTouchUV"
category: "function"
type: "function"
language: "LSL"
description: "Returns a vector that is the texture coordinates for where the prim was touched. The x & y vector positions contain the horizontal (u) & vertical (v) texture coordinates respectively (<u, v, 0.0>). Like llDetectedTouchST, the interval of each component will be [0.0, 1.0] unless the texture repeats a"
signature: "vector llDetectedTouchUV(integer number)"
return_type: "vector"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llDetectedTouchUV'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["lldetectedtouchuv"]
---

Returns a vector that is the texture coordinates for where the prim was touched. The x & y vector positions contain the horizontal (u) & vertical (v) texture coordinates respectively (<u, v, 0.0>). Like llDetectedTouchST, the interval of each component will be [0.0, 1.0] unless the texture repeats are set to a non-default value. Increasing or decreasing the texture repeats of the face will change this interval accordingly. Additionally, unlike with llDetectedTouchST, changing a texture's rotation will change the results of this function.

 is returned when the touch UV coordinates cannot be determined. See Caveats for further details.

For the Touch category of events only. The prim that was touched may not be the prim receiving the event, use llDetectedLinkNumber to check for this; likewise you can use llDetectedTouchFace to determine which face was touched.


## Signature

```lsl
vector llDetectedTouchUV(integer number);
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

- [SL Wiki](https://wiki.secondlife.com/wiki/llDetectedTouchUV)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llDetectedTouchUV) — scraped 2026-03-18_

Returns a vector that is the texture coordinates for where the prim was touched. The x & y vector positions contain the horizontal (u) & vertical (v) texture coordinates respectively (<u, v, 0.0>). Like llDetectedTouchST, the interval of each component will be [0.0, 1.0] unless the texture repeats are set to a non-default value. Increasing or decreasing the texture repeats of the face will change this interval accordingly. Additionally, unlike with llDetectedTouchST, changing a texture's rotation will change the results of this function.

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
        integer face = llDetectedTouchFace(0);
        vector  touchUV   = llDetectedTouchUV(0);

//      ZERO_VECTOR (<0.0, 0.0, 0.0> ... the origin) is in the bottom left corner of the texture
//      touchUV.x goes across the texture from left to right
//      touchUV.y goes up the texture from bottom to top

        if (face == TOUCH_INVALID_FACE)
            llWhisper(PUBLIC_CHANNEL, "Sorry, your viewer doesn't support touched faces.");
        else if (touchUV == TOUCH_INVALID_TEXCOORD)
            llWhisper(PUBLIC_CHANNEL, "Sorry, the touch position upon the texture could not be determined.");
        else
            llSay(PUBLIC_CHANNEL, "llDetectedTouchUV(" + (string)touchUV + ")"
                    + "\ntouchUV.x = " + (string)touchUV.x
                    + "\ntouchUV.y = " + (string)touchUV.y);
    }
}
```

```lsl
integer numberOfRows    = 12;
integer numberOfColumns = 12;

default
{
    touch_start(integer num_detected)
    {
        vector touchUV = llDetectedTouchUV(0);

//      ZERO_VECTOR (<0.0, 0.0, 0.0> ... the origin) is in the bottom left corner of the texture
//      touchUV.x goes across the texture from left to right
//      touchUV.y goes up the texture from bottom to top

        integer columnIndex = (integer) (touchUV.x * numberOfColumns);
        integer rowIndex    = (integer) (touchUV.y * numberOfRows);
        integer cellIndex   = rowIndex * numberOfColumns + columnIndex;

        llSay(PUBLIC_CHANNEL, "UV grid (" + (string)columnIndex + ", " + (string)rowIndex + ") --> cell " + (string)cellIndex);
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
- llDetectedTouchST
- llDetectedTouchPos
- llDetectedTouchNormal
- llDetectedTouchBinormal

### Articles

- Detected

<!-- /wiki-source -->
