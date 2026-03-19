---
name: "llDetectedTouchFace"
category: "function"
type: "function"
language: "LSL"
description: 'Returns an integer that is the index of the face the avatar clicked on.

For the Touch category of events only. The prim that was touched may not be the prim receiving the event, use llDetectedLinkNumber to check for this; likewise you can use llDetectedTouchFace to determine which face was touched.'
signature: "integer llDetectedTouchFace(integer number)"
return_type: "integer"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llDetectedTouchFace'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["lldetectedtouchface"]
---

Returns an integer that is the index of the face the avatar clicked on.

For the Touch category of events only. The prim that was touched may not be the prim receiving the event, use llDetectedLinkNumber to check for this; likewise you can use llDetectedTouchFace to determine which face was touched.


## Signature

```lsl
integer llDetectedTouchFace(integer number);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `integer` | `index` | Index of detection information |


## Return Value

Returns `integer`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llDetectedTouchFace)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llDetectedTouchFace) — scraped 2026-03-18_

Returns an integer that is the index of the face the avatar clicked on.

## Caveats

- If index is out of bounds  the script continues to execute without an error message.
- TOUCH_INVALID_FACE is returned when...

  - The avatar's viewer does not support face touch detection.
  - The touch has moved off the surface of the prim.
  - The event triggered is not a touch event.

## Examples

```lsl
// This is the essential script to drop in a prim when you need to ascertain the number of a face (or faces)
// Touch the prim surfaces to learn their face numbers, which you can then use in other scripts for texturing, colouring etc.

say(string message)
{
    llSay(PUBLIC_CHANNEL, message);
}

default
{
    touch_start(integer num_detected)
    {
        integer face = llDetectedTouchFace(0);

        if (face == TOUCH_INVALID_FACE)
//      {
            say("The touched face could not be determined");
//      }
        else
//      {
            say("You touched face number " + (string) face);
//      }
    }
}
```

```lsl
default
{
    touch_start(integer num_detected)
    {
        integer link = llDetectedLinkNumber(0);
        integer face = llDetectedTouchFace(0);

        if (face == TOUCH_INVALID_FACE)
            llSay(PUBLIC_CHANNEL, "Sorry, your viewer doesn't support touched faces.");
        else
        {
            // store the original color
            list   colorParams   = llGetLinkPrimitiveParams(link, [PRIM_COLOR, face]);
            vector originalColor = llList2Vector(colorParams, 0);

            // color detected face white
            llSetLinkColor(link, <1.0, 1.0, 1.0>, face);
            llSleep(0.2);

            // color detected face black
            llSetLinkColor(link, ZERO_VECTOR, face);
            llSleep(0.2);

            // color detected face back to original color
            llSetLinkColor(link, originalColor, face);
        }
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
- llDetectedTouchST
- llDetectedTouchUV
- llDetectedTouchPos
- llDetectedTouchNormal
- llDetectedTouchBinormal

### Articles

- Detected

<!-- /wiki-source -->
