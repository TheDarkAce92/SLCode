---
name: "llDetectedTouchBinormal"
category: "function"
type: "function"
language: "LSL"
description: 'Returns a vector that is the surface binormal (tangent to the surface, pointing along the positive T (V) direction of tangent space) where the touch event was triggered. Along with llDetectedTouchNormal, this information can be used to find the tangent space at the touch location.

index does not su'
signature: "vector llDetectedTouchBinormal(integer number)"
return_type: "vector"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llDetectedTouchBinormal'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["lldetectedtouchbinormal"]
---

Returns a vector that is the surface binormal (tangent to the surface, pointing along the positive T (V) direction of tangent space) where the touch event was triggered. Along with llDetectedTouchNormal, this information can be used to find the tangent space at the touch location.

index does not support negative indexes.
For the touch category of events only. The prim that was touched may not be the prim receiving the event, use llDetectedLinkNumber to check for this; likewise you can use llDetectedTouchFace to determine which face was touched.
To find the third tangent vector, cross this vector with the normal.


## Signature

```lsl
vector llDetectedTouchBinormal(integer number);
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

- [SL Wiki](https://wiki.secondlife.com/wiki/llDetectedTouchBinormal)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llDetectedTouchBinormal) — scraped 2026-03-18_

Returns a vector that is the surface binormal (tangent to the surface, pointing along the positive T (V) direction of tangent space) where the touch event was triggered. Along with llDetectedTouchNormal, this information can be used to find the tangent space at the touch location.

## Caveats

- If index is out of bounds  the script continues to execute without an error message.
- Events that enable the llDetected* functions always return at least one detected item.

  - Detection events are not raised if there is nothing detected.
  - The detection event's items detected parameter is initially never less than 1.
- TOUCH_INVALID_VECTOR is returned when...

  - The avatar's viewer does not support face touch detection.

  - To check if face touch detection is supported check the return of llDetectedTouchFace.
  - The touch has moved off the surface of the prim.
  - The event triggered is not a touch event.

## Examples

```lsl
default
{
    touch_start(integer total_num)
    {
        llOwnerSay((string)llDetectedTouchBinormal(0));
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
- llDetectedTouchNormal

### Articles

- Detected

<!-- /wiki-source -->
