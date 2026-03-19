---
name: "llDetectedLinkNumber"
category: "function"
type: "function"
language: "LSL"
description: 'Returns the link_number (an integer) of the triggered event. If not supported by the event, returns zero.

number does not support negative indexes.
For touch and collision categories of events only.'
signature: "integer llDetectedLinkNumber(integer number)"
return_type: "integer"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llDetectedLinkNumber'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["lldetectedlinknumber"]
---

Returns the link_number (an integer) of the triggered event. If not supported by the event, returns zero.

number does not support negative indexes.
For touch and collision categories of events only.


## Signature

```lsl
integer llDetectedLinkNumber(integer number);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `integer` | `number` | Index of detection information |


## Return Value

Returns `integer`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llDetectedLinkNumber)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llDetectedLinkNumber) — scraped 2026-03-18_

Returns the link_number (an integer) of the triggered event. If not supported by the event, returns zero.

## Caveats

- llDetectedLinkNumber will return 0 in collision_start and collision_end events of VolumeDetect objects (SVC-2996).
- If number is out of bounds this function returns 0 and the script continues to execute without an error message.
- Events that enable the llDetected* functions always return at least one detected item.

  - Detection events are not raised if there is nothing detected.
  - The detection event's items detected parameter is initially never less than 1.

## Examples

```lsl
default
{
// Drop this script into the root prim of of a build
// Touch any prim to learn its link number
    touch_start(integer num_detected)
    {
        llOwnerSay("Link number clicked: " + (string)llDetectedLinkNumber(0) );
    }
}
```

## See Also

### Events

- touch_start
- touch
- touch_end
- collision_start
- collision
- collision_end

### Functions

- llDetectedTouchFace

### Articles

- Detected

<!-- /wiki-source -->
