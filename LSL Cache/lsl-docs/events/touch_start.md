---
name: "touch_start"
category: "event"
type: "event"
language: "LSL"
description: "Fires when an avatar begins clicking/touching the prim"
wiki_url: "https://wiki.secondlife.com/wiki/Touch_start"
first_fetched: "2026-03-09"
last_updated: "2026-03-09"
signature: "touch_start(integer num_detected)"
parameters:
  - name: "num_detected"
    type: "integer"
    description: "Number of avatars that started touching during the last clock cycle"
deprecated: "false"
---

# touch_start

```lsl
touch_start(integer num_detected)
{
    // handle touch
}
```

Fires at the beginning of a touch — when an avatar first clicks or holds click on a prim.

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `num_detected` | integer | Number of simultaneous touch starts in this event cycle |

## Detection Data

Use `llDetected*` functions with index 0 through `num_detected - 1`:
- `llDetectedKey(0)` — UUID of the touching avatar
- `llDetectedName(0)` — legacy name of the touching avatar
- `llDetectedPos(0)` — position of the touching avatar
- `llDetectedTouchFace(0)` — face number touched (0–8 or -1 for unknown)
- `llDetectedTouchPos(0)` — position on the prim's surface that was touched

## Caveats

- **Avoid state changes in `touch_start`** — use `touch_end` instead. State changes in `touch_start` can cause subsequent touch events to be missed.
- **Shared Media:** If a prim face has Shared Media enabled, touches on that face are not detected.
- **Multi-prim linksets:** Root prim handler fires if the root or an unhandled child is touched. Child handlers block root handler. Use `llPassTouches` to change this.
- **Rigged mesh attachments:** Do not support touch detection via script (only via right-click menu).
- **Known bug:** If an avatar is already touching a scripted object, `touch_start` may only fire every other time another avatar touches it.

## Examples

```lsl
default
{
    touch_start(integer num_detected)
    {
        key avatarKey   = llDetectedKey(0);
        string avatarName = llDetectedName(0);
        llInstantMessage(avatarKey, "Hello, " + avatarName + "!");
    }
}
```

```lsl
// Only owner can touch
default
{
    touch_start(integer num_detected)
    {
        if (llDetectedKey(0) != llGetOwner()) return;
        llOwnerSay("Owner touched!");
    }
}
```

## See Also

- `touch` — fires continuously while avatar holds the touch
- `touch_end` — fires when avatar releases the touch
- `llDetectedKey`, `llDetectedName`, `llDetectedPos`, `llDetectedTouchFace`
- `llPassTouches` — control touch pass-through in linksets


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/touch_start) — scraped 2026-03-18_

## Caveats

- If a prim face has Shared Media enabled and the avatar's viewer supports this feature, LSL scripts will not detect touches on that face. Touches from older clients will be detected.
- The default behavior is: If you have a multi-prim object and the root has a touch_start handler AND one or more child prims has a touch_start handler, the root prim's handler will be called when it (the root) or a child without a handler is touched. If you touch a child prim that has a touch_start handler, it will receive the event and the root prim will not.

  - This behavior can be configured with llPassTouches. After configuring a prim's touch-passing behavior you can delete the script that configured the prim.
- Rigged mesh attachments do not support touch events, this is because you can steer your avatar/camera by click dragging your avatar body which is what the rigged mesh replaces. The only way to get a touch event on a rigged mesh attachment is via the right click context menu and clicking the "Touch" button.
- [Due to a known issue](https://feedback.secondlife.com/scripting-bugs/p/touch-start-only-triggers-on-the-second-touch-if-touch-is-already-active), if a resident is already touching a scripted object, touch_start runs only every other time that other residents touch it.

## Examples

You can use numbers 0 through (`num_detected`-1) with the various `llDetected`... functions to get detected agent keys etc. For most purposes, it is adequate to bother only with the first detected toucher e.g. llDetectedKey(0). It is rare (but not impossible) for `num_detected` to be other than 1.

```lsl
default
{
    touch_start(integer num_detected)
    {
        key    avatarKey  = llDetectedKey(0);
        string avatarName = llDetectedName(0);

        llInstantMessage(avatarKey, "Hello " + avatarName );
    }
}
```

## Notes

- If using a touch to change states be careful about the touch event order. **The best advice is not to do state changes from within touch_start.** Add a touch_end handler and do the state change there. Changing state from within touch_start can cause the next occurrence of THIS touch_start code to be missed.

- On clicking a prim with touch event handlers, the following handlers are triggered: touch_start (on first contact), touch (during) and touch_end (as released).

## See Also

### Events

- touch
- touch_end

### Functions

- llSetTouchText
- llPassTouches
- llDetectedTouchFace
- llDetectedTouchST
- llDetectedTouchUV
- llDetectedTouchPos
- llDetectedTouchNormal
- llDetectedTouchBinormal

<!-- /wiki-source -->
