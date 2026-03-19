---
name: "collision_start"
category: "event"
type: "event"
language: "LSL"
description: "Fires when the object begins colliding with another object or avatar"
wiki_url: "https://wiki.secondlife.com/wiki/Collision_start"
first_fetched: "2026-03-09"
last_updated: "2026-03-09"
signature: "collision_start(integer num_detected)"
parameters:
  - name: "num_detected"
    type: "integer"
    description: "Number of colliding objects/avatars detected"
deprecated: "false"
---

# collision_start

```lsl
collision_start(integer num_detected)
{
    // handle collision start
}
```

Fires when the object first makes contact with another object or avatar.

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `num_detected` | integer | Number of detected collision entities |

## Detection Data

Use `llDetected*` functions with index 0 through `num_detected - 1`.

## Caveats

- **Does not detect ground collisions** — use `land_collision_start` instead.
- Phantom objects do not receive collision events.
- Objects with `llVolumeDetect(TRUE)` receive `collision_start` and `collision_end` but not the continuous `collision` event.
- Only a **physical** object receives collision events from colliding with a non-physical object.
- Avatar collisions require actual movement or rotation to trigger.

## Example

```lsl
default
{
    collision_start(integer num)
    {
        llSay(0, "Ouch! Something hit me.");
    }
}
```

## See Also

- `collision` — fires continuously while collision continues
- `collision_end` — fires when collision ends
- `land_collision_start` — ground collisions
- `llVolumeDetect` — trigger collision events without physics
- `llPassCollisions` — pass collision events to root
- `llCollisionFilter` — filter which objects trigger events


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/collision_start) — scraped 2026-03-18_

## Caveats

- Will not detect collisions with ground.  Use land_collision_start instead.
- Phantom objects can never receive trigger collision events.
- `llVolumeDetect(TRUE)` objects get trigger collision_start and collision_end but not collision() events.
- A collision with a hovering avatar does not trigger collisions, unless the avatar turns or moves.
- Only a physical object will get collision events from colliding with a non-physical object.

## Examples

```lsl
default
{
    collision_start(integer num)
    {
        llSay(0,"No pushing.");
    }
}
```

```lsl
list DetectedAvatars = [];
default
{
    state_entry()
    {
        llVolumeDetect(TRUE); // Enable detection of people colliding with object....
    }
    collision_start(integer detected)
    {
        integer index = llListFindList(DetectedAvatars, [llDetectedKey(0)]);
        if (index == -1)
        {
            llInstantMessage(llDetectedKey(0), " Welcome to the Community");
            DetectedAvatars = llListInsertList(DetectedAvatars, [llDetectedKey(0)], -1);

            if (llGetListLength(DetectedAvatars) == 2)
            {
                DetectedAvatars = llDeleteSubList(DetectedAvatars, 1, 2);
            }
        }
    }
}
```

## See Also

### Events

- collision
- collision_end

### Functions

- llPassCollisions
- llCollisionFilter
- llCollisionSound
- llCollisionSprite
- llVolumeDetect

<!-- /wiki-source -->
