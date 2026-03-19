---
name: "land_collision_start"
category: "event"
type: "event"
language: "LSL"
description: "Triggered in the root when a physical object or attached avatar starts colliding with land"
signature: "land_collision_start(vector pos)"
wiki_url: 'https://wiki.secondlife.com/wiki/land_collision_start'
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
deprecated: "false"
parameters: []
---

Triggered in the root when a physical object or attached avatar starts colliding with land


## Signature

```lsl
land_collision_start(vector pos)
{
    // your code here
}
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `vector` | `pos` | position of collision with the ground |


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/land_collision_start)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/land_collision_start) — scraped 2026-03-18_

## Examples

```lsl
//Put script into physical object and drop to ground.  It will say position of initial impact.
default
{
     land_collision_start( vector pos )
    {
       llOwnerSay("Land collision at: "+(string) pos.x + ","+(string) pos.y+","+(string)pos.z);
    }
}
```

## See Also

- Collision events & functions

### Events

- land_collision
- land_collision_end

### Functions

- **llGround** — Gets the ground height

<!-- /wiki-source -->
