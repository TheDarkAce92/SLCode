---
name: "land_collision"
category: "event"
type: "event"
language: "LSL"
description: "Triggered in the root when physical object or attached avatar is colliding with land"
signature: "land_collision(vector pos)"
wiki_url: 'https://wiki.secondlife.com/wiki/land_collision'
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
deprecated: "false"
parameters: []
---

Triggered in the root when physical object or attached avatar is colliding with land


## Signature

```lsl
land_collision(vector pos)
{
    // your code here
}
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `vector` | `pos` | position of collision with the ground |


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/land_collision)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/land_collision) — scraped 2026-03-18_

## Examples

```lsl
//Will die on collision with land.
default
{
     land_collision(vector pos)
     {
          llDie();
     }
}
```

## See Also

- Collision events & functions

### Events

- land_collision_start
- land_collision_end

### Functions

- **llGround** — Gets the ground height

<!-- /wiki-source -->
