---
name: "llPassCollisions"
category: "function"
type: "function"
language: "LSL"
description: 'Sets the pass-collisions prim attribute.

Whether Collisions are passed to the root prim depends not only on which PASS_* flag is selected, but may also depend on if there is a script that in the prim that handles one of the collision events. For this reason most users will want to use PASS_ALWAYS o'
signature: "void llPassCollisions(integer pass)"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llPassCollisions'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llpasscollisions"]
---

Sets the pass-collisions prim attribute.

Whether Collisions are passed to the root prim depends not only on which PASS_* flag is selected, but may also depend on if there is a script that in the prim that handles one of the collision events. For this reason most users will want to use PASS_ALWAYS or PASS_NEVER as they do not have this variable behavior.

The default value for this attribute is PASS_IF_NOT_HANDLED.


## Signature

```lsl
void llPassCollisions(integer pass);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `integer (pass)` | `pass` | PASS_* flag |


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llPassCollisions)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llPassCollisions) — scraped 2026-03-18_

Sets the pass-collisions prim attribute.

## Caveats

- Has no known effect if called from within the root prim.
- The script must be located in the prim whose pass-touch behavior is being changed; if not, the prim reverts to the default pass-touch setting.

## See Also

### Events

- collision_start
- collision
- collision_end

### Functions

- llPassTouches
- llCollisionFilter
- llCollisionSound
- llCollisionSprite
- llVolumeDetect

<!-- /wiki-source -->
