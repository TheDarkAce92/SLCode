---
name: "llDetectedGrab"
category: "function"
type: "function"
language: "LSL"
description: 'Returns a vector that is the grab offset of the user touching the object; only works in the touch event.

number does not support negative indexes.
Returns <0.0, 0.0, 0.0> if number is out of range or if called from an event other than the touch event.'
signature: "vector llDetectedGrab(integer number)"
return_type: "vector"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llDetectedGrab'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["lldetectedgrab"]
---

Returns a vector that is the grab offset of the user touching the object; only works in the touch event.

number does not support negative indexes.
Returns <0.0, 0.0, 0.0> if number is out of range or if called from an event other than the touch event.


## Signature

```lsl
vector llDetectedGrab(integer number);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `integer` | `number` | Index of detection information |


## Return Value

Returns `vector`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llDetectedGrab)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llDetectedGrab) — scraped 2026-03-18_

Returns a vector that is the grab offset of the user touching the object; only works in the touch event.

## Caveats

- If number is out of bounds this function returns <0.0, 0.0, 0.0> and the script continues to execute without an error message.
- Events that enable the llDetected* functions always return at least one detected item.

  - Detection events are not raised if there is nothing detected.
  - The detection event's items detected parameter is initially never less than 1.
- When called in HUD attachments, values returned are affected by the wearer's position and rotation.

## Examples

```lsl
default
{
    state_entry()
    {
        llSetStatus(PRIM_PHYSICS,TRUE);//This allows the object to be "grabbed" and dragged
    }
    touch(integer num_detected)
    {
        llSay(0,(string)llDetectedGrab(0));//Be prepared for a great amount of chatted info.
                                           //The faster you move the mouse while grabbing the object the greater the offset becomes.
                                           //This is not due to the speed but the reaction time of the turn around of the physical prim,
                                           //thus an offset (distance from grab to prim center) is created and measured by this function.
    }
}
```

```lsl
/**

Simple llDetectedGrab illustration, rez a prim and add this script.
The prim will become a cone that follows mouse grabs.

 Click and hold the mouse button down on the object, then:
 - Drag left and right to move parallel to the camera focal plane.
 - Drag up and down to move to and from the camera.
 - Hold down Ctrl, then drag up and down to move vertically.

**/

default
{
    state_entry()
    {
        llMinEventDelay(0.25);
        llSetStatus(STATUS_PHYSICS, FALSE); // make the object static for simplicity
        llSetPrimitiveParams([
            PRIM_SIZE, <0.5, 0.5, 0.5>,
            PRIM_TYPE, PRIM_TYPE_CYLINDER, PRIM_HOLE_DEFAULT, <0.0, 1.0, 0.0>,
              0.0, ZERO_VECTOR, ZERO_VECTOR, ZERO_VECTOR
        ]); // a cone that can follow the mouse pointer
    }

    touch(integer total_number)
    {
        llLookAt(llGetPos() + llDetectedGrab(0), 1.0, 1.0);
    }
}
```

## Notes

llDetectedGrab() is not blocked by STATUS_BLOCK_GRAB or STATUS_BLOCK_GRAB_OBJECT.

## See Also

### Events

- touch_start
- touch
- touch_end

### Functions

- llPassTouches

### Articles

- Detected
- Grab

<!-- /wiki-source -->
