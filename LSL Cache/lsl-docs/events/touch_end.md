---
name: "touch_end"
category: "event"
type: "event"
language: "LSL"
description: "Fires when an avatar releases a touch/click on the prim"
wiki_url: "https://wiki.secondlife.com/wiki/Touch_end"
first_fetched: "2026-03-09"
last_updated: "2026-03-09"
signature: "touch_end(integer num_detected)"
parameters:
  - name: "num_detected"
    type: "integer"
    description: "Number of avatars that ended touching during this cycle"
deprecated: "false"
---

# touch_end

```lsl
touch_end(integer num_detected)
{
    // handle touch release
}
```

Fires when an avatar releases a click/touch. Preferred over `touch_start` for triggering state changes, as it avoids missing subsequent touches.

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `num_detected` | integer | Number of touch-end events in this cycle |

## When to Use touch_end vs touch_start

- **`touch_end`** — use for state changes, or any action that should complete after the full click. Safer for state transitions.
- **`touch_start`** — use when immediate response to first contact is needed.
- **`touch`** — fires continuously while holding click; use for hold-sensitive interactions.

## Example

```lsl
default
{
    touch_end(integer num_detected)
    {
        // Safer than touch_start for state changes
        state active;
    }
}

state active
{
    state_entry()
    {
        llOwnerSay("Entered active state");
    }

    touch_end(integer num_detected)
    {
        state default;
    }
}
```

## See Also

- `touch_start` — fires at start of touch
- `touch` — fires continuously during touch
- `llPassTouches` — pass touch events to root prim


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/touch_end) — scraped 2026-03-18_

## Caveats

- If a prim face has Shared Media enabled and the avatar's viewer supports this feature, LSL scripts will not detect touches on that face. Touches from older clients will be detected.
- Rigged mesh attachments do not support touch events, this is because you can steer your avatar/camera by click dragging your avatar body which is what the rigged mesh replaces. The only way to get a touch event on a rigged mesh attachment is via the right click context menu and clicking the "Touch" button.

## Examples

You can use numbers 0 through num_detected - 1 with the various llDetected... functions to get detected agent keys etc. For most purposes, it is adequate to bother only with the first detected toucher e.g. llDetectedKey(0).  It is rare (but not impossible) for num_detected to be other than 1.

```lsl
default
{
    touch_start(integer num_detected)
    {
        llResetTime();
    }
    touch_end(integer num_detected)
    {
        llInstantMessage( llDetectedKey(0), "You held the mouse button down for " + (string) llGetTime() + " seconds");
    }
}
```

## Notes

- If using a touch to change states be careful about the touch_ event order. **The best advice is NOT to do state changes from within touch_start.** Use touch_end and do the state change there. Changing state from within touch_start can cause the next occurrence of THAT touch_start code to be missed.

- On clicking a prim with touch events we trigger touch_start (on first contact), touch (during) and touch_end (as released).

## See Also

### Events

- touch_start
- touch

### Functions

- llPassTouches

<!-- /wiki-source -->
