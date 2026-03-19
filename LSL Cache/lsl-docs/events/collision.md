---
name: "collision"
category: "event"
type: "event"
language: "LSL"
description: "Triggered while task is colliding with another task."
signature: "collision(integer num_detected)"
wiki_url: 'https://wiki.secondlife.com/wiki/collision'
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
deprecated: "false"
parameters: []
---

Triggered while task is colliding with another task.


## Signature

```lsl
collision(integer num_detected)
{
    // your code here
}
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `integer` | `num_detected` |  |


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/collision)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/collision) — scraped 2026-03-18_

## Caveats

- Max number detected is 8.
- Smallest repeat rate is approximatively 0.13 seconds.
- Will not detect collisions with ground; use land_collision instead.
- Will not detect collisions between an avatar sitting on the task and the task itself (avatars are linked to objects they sit on so there is no collision, use the changed event to detect sits).
- Phantom objects can never receive trigger collision events.
- `llVolumeDetect(TRUE)` objects get trigger collision_start and collision_end but not collision() events.
- A collision with a hovering avatar does not trigger collisions, unless the avatar turns or moves.
- A collision with a physical object or avatar resting on object does not continuously trigger collisions but for a few times, unless there is movement.
- Only a physical object will get collision events from colliding with a non-physical object.

## Examples

```lsl
//Will turn phantom when someone bumps into it if on the list

list access_list = ["Governor Linden"];

default
{
    collision(integer num_detected)
    {
        if(~llListFindList(access_list, (list)llDetectedName(0)))
        {
            llSetStatus(STATUS_PHANTOM, TRUE);
        }
    }
}
```

## See Also

### Events

- collision_start
- collision_end

### Functions

- llPassCollisions
- llCollisionFilter
- llCollisionSound
- llCollisionSprite
- llVolumeDetect

<!-- /wiki-source -->
