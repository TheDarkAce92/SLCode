---
name: "touch"
category: "event"
type: "event"
language: "LSL"
description: "Fires continuously while an avatar holds a click/touch on the prim"
wiki_url: "https://wiki.secondlife.com/wiki/Touch"
first_fetched: "2026-03-09"
last_updated: "2026-03-09"
signature: "touch(integer num_detected)"
parameters:
  - name: "num_detected"
    type: "integer"
    description: "Number of avatars currently holding touch"
deprecated: "false"
---

# touch

```lsl
touch(integer num_detected)
{
    // fires continuously while holding click
}
```

Fires repeatedly while an avatar holds a click on the prim. Fires after `touch_start` and before `touch_end`.

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `num_detected` | integer | Number of avatars currently touching |

## Caveats

- Use `llDetectedTouchPos`, `llDetectedTouchFace`, `llDetectedTouchST`, `llDetectedTouchUV` for advanced interaction.
- Fires at the server frame rate — not suitable for precise timing without additional logic.

## Example

```lsl
default
{
    touch(integer num_detected)
    {
        vector touchPos = llDetectedTouchPos(0);
        llOwnerSay("Touch position: " + (string)touchPos);
    }
}
```

## See Also

- `touch_start` — fires at start of touch
- `touch_end` — fires when touch is released
- `llDetectedTouchFace` — which face was touched
- `llDetectedTouchPos` — world position of touch point


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/touch) — scraped 2026-03-18_

## Caveats

- If a prim face has Shared Media enabled and the avatar's viewer supports this feature, LSL scripts will not detect touches on that face. Touches from older clients will be detected.
- Rigged mesh attachments do not support touch events, this is because you can steer your avatar/camera by click dragging your avatar body which is what the rigged mesh replaces. The only way to get a touch event on a rigged mesh attachment is via the right click context menu and clicking the "Touch" button.

## Examples

You can use numbers 0 through (num_detected-1) with the various llDetected... functions to get detected agent keys etc. For most purposes, it is adequate to bother only with the first detected toucher e.g. llDetectedKey(0). It is rare (but not impossible) for num_detected to be other than 1.

```lsl
default
{
     touch(integer num_detected)
     {
          llOwnerSay("I am being touched by " + llDetectedName(0) + ".");
     }
}
```

This next example demonstrates detecting when the owner of the object clicks-and-holds on the object for 1 second in order perhaps to access a management menu or similar, Normal brief clicks are distinguished.

```lsl
default
{
    touch_start(integer num_detected)
    {
	llResetTime();
    }
    touch(integer num_detected)
    {
	if (llDetectedKey(0) == llGetOwner() && llGetTime() > 1.0)
	{
	    // The owner has touched this object for longer than 1 second
	    // execute some special feature such as issuing a management dialog
	    // ...
	}
    }
    touch_end(integer num_detected)
    {
	if (llGetTime() <= 1.0)
	{
	    // The user did a normal quick click on the object
	    // execute actions for normal clicks
	    // ...
	}
    }
}
```

Clicking and holding can't be used to call a menu since the menu will pop out continuosly.
Use a flag to avoid this.

```lsl
integer touched;

default
{

    touch_start(integer n)
    {
        touched = FALSE;//HERE, before llResetTime() otherwise it doesn't run
        llResetTime();
    }

    touch(integer n)
    {
        if (llGetTime() > 1.0 && touched == FALSE)
            {
                //Call here the menu
                touched = TRUE;
            }
    }

    touch_end(integer n)
    {
        if (llGetTime() <= 1.0)
            {
	        //Do something
            }
    }
}
```

## Notes

- On clicking a prim with touch events we trigger touch_start (on first contact), touch (during) and touch_end (as released).

## See Also

### Events

- touch_start
- touch_end

### Functions

- **llSetTouchText** — Set the pie menu's text for touch-action
- **llPassTouches** — Allows clicks captured by a child prim to be passed to the root as well

<!-- /wiki-source -->
