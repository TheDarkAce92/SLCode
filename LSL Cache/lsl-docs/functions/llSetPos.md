---
name: "llSetPos"
category: "function"
type: "function"
language: "LSL"
description: "Moves a prim or object to a target position (non-physics, max 10m per call)"
wiki_url: "https://wiki.secondlife.com/wiki/llSetPos"
first_fetched: "2026-03-09"
last_updated: "2026-03-09"
signature: "void llSetPos(vector pos)"
parameters:
  - name: "pos"
    type: "vector"
    description: "Target position. Region coordinates for unattached root prims; local coordinates (relative to attachment point) for attached root prims; local coordinates (relative to root prim) for child prims."
return_type: "void"
energy_cost: "10.0"
sleep_time: "0.2"
patterns: ["llsetpos"]
deprecated: "false"
---

# llSetPos

```lsl
void llSetPos(vector pos)
```

Moves the prim towards `pos` without physics. Movement is capped to 10 metres per call for unattached root prims. Causes a 0.2-second script sleep.

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `pos` | vector | Target position |

## Coordinate System

| Context | Coordinate frame |
|---------|----------------|
| Unattached root prim | Region coordinates |
| Attached root prim | Local to attachment point |
| Child prim | Local to root prim |

## Caveats

- **0.2-second forced delay** — the script sleeps for 0.2 seconds after each call.
- **Physical objects:** Does not work on root prims of physical objects. Use `llMoveToTarget` instead.
- **10-metre cap:** Movement is silently capped to 10 metres per call for unattached root prims.
- **Pathfinding:** Fails on objects marked as static pathfinding obstacles.
- **Preferred alternatives:** `llSetRegionPos` (no distance cap for root), `llSetLinkPrimitiveParamsFast` with `PRIM_POSITION` (no delay).

## Examples

```lsl
// Move object up 1 metre on touch
default
{
    touch_start(integer i)
    {
        llSetPos(llGetPos() + <0.0, 0.0, 1.0>);
    }
}
```

## See Also

- `llGetPos` — get current position (region coordinates)
- `llGetLocalPos` — get position relative to parent
- `llSetRegionPos` — set position with no distance cap
- `llSetLinkPrimitiveParamsFast` with `PRIM_POSITION` — set position without forced delay
- `llMoveToTarget` — physics-based movement


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llSetPos) — scraped 2026-03-18_

Moves the object or primitive towards pos without using physics.

## Caveats

- This function causes the script to sleep for 0.2 seconds.
- Because of the intermixing of local and regional coordinates with this function, when a prims position is wanted it is best to use llGetLocalPos.
- This function does not work in the root prim of physical objects. Use a physical function like llMoveToTarget instead.
- If you have explicitally set your object as "static obstacle" for pathfinding , the function will fail with the error in the debug channel:

  - "Unable to set prim position or scale: object contributes to the navmesh."

## Examples

|  | Important: This function has a movement cap of 10m and a time delay of 0.2 seconds per call. Please consider using llSetRegionPos and/or llSetLinkPrimitiveParamsFast instead. |
| --- | --- |

```lsl
//Move the object up 1m when someone touches it.
default {
     touch_start(integer i) {
          llSetPos(llGetPos() + <0,0,1>);
     }
}
// to bypass the small movement bug use this
// - created by Madpeter Zond
// notes: it does not check if the movement would go out of limit range for linked prims
llSetLocalPos(vector offset)
{
    vector save = offset;
    if(offset.x < 0.0) offset.x -= 1;
    else offset.x += 1;
    if(offset.y < 0.0) offset.y -= 1;
    else offset.y += 1;
    if(offset.z < 0.0) offset.z -= 1;
    else offset.z += 1;
    llSetPos(offset);
    llSetPos(save);
}
```

## Notes

Multiple movement commands can be chained together with llSetPrimitiveParams and PRIM_POSITION. The advantage of doing this is that the script only sleeps once per function call instead of once per movement.

## See Also

### Functions

- **llSetRegionPos** — Sets position of object to any position within the region.
- **llGetLocalPos** — Returns the prim's local position if it is attached or non-root (otherwise it returns the global position)
- **llGetRootPosition** — Gets the root prims position
- **llGetPos** — Returns the prim's global position, even if it is attached or non-root

<!-- /wiki-source -->
