---
name: "llSetHoverHeight"
category: "function"
type: "function"
language: "LSL"
description: 'Critically damps to a height above the ground (or water) in tau seconds.

Do not use with vehicles.
Use llStopHover to stop hovering.'
signature: "void llSetHoverHeight(float height, integer water, float tau)"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llSetHoverHeight'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llsethoverheight"]
---

Critically damps to a height above the ground (or water) in tau seconds.

Do not use with vehicles.
Use llStopHover to stop hovering.


## Signature

```lsl
void llSetHoverHeight(float height, integer water, float tau);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `float` | `height` | Distance to hover above the ground (if negative, hovers below ground) |
| `integer (boolean)` | `water` | boolean, if TRUE then hover above water too (or below if height is negative), if FALSE ignore water like it isn't there |
| `float` | `tau` | seconds to critically damp in |


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llSetHoverHeight)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llSetHoverHeight) — scraped 2026-03-18_

Critically damps to a height above the ground (or water) in tau seconds.

## Caveats

- Only works in  physics-enabled objects.
- Do not rely on built-in limits. In the past, the difference between the object's initial position and the hover height was limited to 64 meters. Under SL Server 1.26.2 the limit is 4096 meters above the ground level.
- This is not a prim property; stopping or resetting the script stops llSetHoverHeight; same with the similar llGroundRepel
- If the object tries to go above the height (like, walking up a prim ramp), llSetHoverHeight will pull it back down, unlike the similar llGroundRepel

## Examples

```lsl
// Put in an attached prim and touch to start floating in air without flying.
// Touch again to drop to the ground.

integer gHovering = FALSE; // are we supposd to be hovering now?

default {
    touch_start(integer total_number) {
        if (!llGetAttached()) {
            llWhisper(0, "Wear me to play.");
            return;
        }

        if (gHovering) {
            llOwnerSay("Releasing you.");
            llStopHover();
        }
        else {
            llOwnerSay("Making you float...");

            // Start hovering 5 meters over our current location.
            vector myPosition = llGetPos();
            llSetHoverHeight(myPosition.z - llGround(ZERO_VECTOR) + 5.0, FALSE, 1.0);
        }

        gHovering = !gHovering; // flip the switch
    }
}
```

## Notes

- It is possible to assign **height** a negative value. If **water** is TRUE, this will make the object hover below the water level.
- Unless volume detect is enabled, negative **height** values when **water** is FALSE will not move the object below the ground level and may cause it to be dragged down the local incline to the nearest low point. Enabling volume detect will cause negative **height** settings to move the object below the ground level.
- Assigning **height** a value of zero will have the same effect as llStopHover.

## See Also

### Functions

- **llGroundRepel** — Same as llSetHoverHeight but does not hover all the time
- **llStopHover** — To stop hovering

<!-- /wiki-source -->
