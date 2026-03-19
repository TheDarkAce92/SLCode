---
name: "llDetectedTouchNormal"
category: "function"
type: "function"
language: "LSL"
description: 'Returns a vector that is the surface normal (perpendicular to the surface) where the touch event was triggered. Along with llDetectedTouchBinormal, this information can be used to find the tangent space at the touch location.

For the Touch category of events only. The prim that was touched may not '
signature: "vector llDetectedTouchNormal(integer number)"
return_type: "vector"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llDetectedTouchNormal'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["lldetectedtouchnormal"]
---

Returns a vector that is the surface normal (perpendicular to the surface) where the touch event was triggered. Along with llDetectedTouchBinormal, this information can be used to find the tangent space at the touch location.

For the Touch category of events only. The prim that was touched may not be the prim receiving the event, use cross the binormal with this vector.


## Signature

```lsl
vector llDetectedTouchNormal(integer number);
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

- [SL Wiki](https://wiki.secondlife.com/wiki/llDetectedTouchNormal)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llDetectedTouchNormal) — scraped 2026-03-18_

Returns a vector that is the surface normal (perpendicular to the surface) where the touch event was triggered. Along with llDetectedTouchBinormal, this information can be used to find the tangent space at the touch location.

## Caveats

- If index is out of bounds  the script continues to execute without an error message.
- TOUCH_INVALID_VECTOR is returned when...

  - The avatar's viewer does not support face touch detection.

  - To check if face touch detection is supported check the return of llDetectedTouchFace.
  - The touch has moved off the surface of the prim.
  - The event triggered is not a touch event.
- The rotation of a legacy sphere prim does not influence touch normal like it does with other legacy prims.

## Examples

```lsl
default
{
    touch_start(integer total_num)
    {
        llOwnerSay((string)llDetectedTouchNormal(0)); //Says the vector where the touched face is pointing to.
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
- llDetectedTouchUV
- llDetectedTouchPos
- llDetectedTouchBinormal

### Articles

- Detected

<!-- /wiki-source -->
