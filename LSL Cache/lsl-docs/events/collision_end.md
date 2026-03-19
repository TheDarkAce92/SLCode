---
name: "collision_end"
category: "event"
type: "event"
language: "LSL"
description: "Triggered when task stops colliding with another task"
signature: "collision_end(integer num_detected)"
wiki_url: 'https://wiki.secondlife.com/wiki/collision_end'
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
deprecated: "false"
parameters: []
---

Triggered when task stops colliding with another task


## Signature

```lsl
collision_end(integer num_detected)
{
    // your code here
}
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `integer` | `num_detected` |  |


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/collision_end)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/collision_end) — scraped 2026-03-18_

## Caveats

- Phantom objects can never receive trigger collision events.
- `llVolumeDetect(TRUE)` objects get trigger collision_start and collision_end but not collision() events.
- A collision with a hovering avatar does not trigger collisions, unless the avatar turns or moves.
- Only a physical object will get collision events from colliding with a non-physical object.

## Examples

```lsl
collision_end(integer total_number)
{
    llOwnerSay("The collision I've had with " + llDetectedName(0) + "has ended.");
}
```

## See Also

### Events

- collision_start
- collision

### Functions

- llPassCollisions
- llCollisionFilter
- llCollisionSound
- llCollisionSprite
- llVolumeDetect

<!-- /wiki-source -->
