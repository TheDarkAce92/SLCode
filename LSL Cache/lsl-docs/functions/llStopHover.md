---
name: "llStopHover"
category: "function"
type: "function"
language: "LSL"
description: "Stop hovering to a height"
signature: "void llStopHover()"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llStopHover'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llstophover"]
---

Stop hovering to a height


## Signature

```lsl
void llStopHover();
```


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llStopHover)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llStopHover) — scraped 2026-03-18_

Stop hovering to a height

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

## See Also

### Functions

- llGroundRepel
- llSetHoverHeight

<!-- /wiki-source -->
