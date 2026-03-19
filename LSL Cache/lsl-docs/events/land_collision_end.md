---
name: "land_collision_end"
category: "event"
type: "event"
language: "LSL"
description: "Triggered in the root when a physical object or attached avatar stops colliding with land"
signature: "land_collision_end(vector pos)"
wiki_url: 'https://wiki.secondlife.com/wiki/land_collision_end'
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
deprecated: "false"
parameters: []
---

Triggered in the root when a physical object or attached avatar stops colliding with land


## Signature

```lsl
land_collision_end(vector pos)
{
    // your code here
}
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `vector` | `pos` | position of last collision with the ground |


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/land_collision_end)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/land_collision_end) — scraped 2026-03-18_

## Examples

```lsl
default
{
    land_collision_start(vector pos)
    {
        llOwnerSay("Colliding with land.");
    }
    land_collision_end(vector pos)
    {
        llOwnerSay("Stopped colliding with land.");
    }
}
```

## See Also

- Collision events & functions

### Events

- **land_collision_start** — transition to starting land collision
- land_collision

### Functions

- **llGround** — Gets the ground height

<!-- /wiki-source -->
