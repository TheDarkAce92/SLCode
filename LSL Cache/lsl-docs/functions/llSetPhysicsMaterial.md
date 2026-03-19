---
name: "llSetPhysicsMaterial"
category: "function"
type: "function"
language: "LSL"
description: 'Used to set the physical characteristics of an object.

The default values for friction and restitution depend upon the material type.'
signature: "void llSetPhysicsMaterial(integer flags, float gravity_multiplier, float restitution, float friction, float density)"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llSetPhysicsMaterial'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llsetphysicsmaterial"]
---

Used to set the physical characteristics of an object.

The default values for friction and restitution depend upon the material type.


## Signature

```lsl
void llSetPhysicsMaterial(integer flags, float gravity_multiplier, float restitution, float friction, float density);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `integer` | `material_mask` | bitwise combination of DENSITY, FRICTION, RESTITUTION, and GRAVITY_MULTIPLIER and specifies which floats to actually apply |
| `float` | `gravity_multiplier` | range [-1.0, +28.0], default: 1.0 |
| `float` | `restitution` | range [0.0, 1.0], default: [0.3, 0.9] |
| `float` | `friction` | range [0.0, 255.0], default: [0.2, 0.9] |
| `float` | `density` | range [1.0, 22587.0] kg/m^3, default: 1000.0 |


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llSetPhysicsMaterial)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llSetPhysicsMaterial) — scraped 2026-03-18_

Used to set the physical characteristics of an object.

## Caveats

- A collision between two objects with restitution 1.0 will still not be perfectly elastic due to damping in the physics engine.
- Using PRIM_MATERIAL to set the material type will reset the values for friction and restitution to that material's defaults.
- llSetPhysicsMaterial silently fails if called from an attachment.

## Examples

- Basic Example

```lsl
     llSetPhysicsMaterial(FRICTION, 1.0,0.9,0.1,0.5); // Sets FRICTION to 0.1
```

- Multiple Settings

```lsl
     llSetPhysicsMaterial(GRAVITY_MULTIPLIER | RESTITUTION | FRICTION | DENSITY, 0.5,0.9,0.1,1.0);
```

## See Also

### Constants

- PRIM_MATERIAL

### Functions

- llGetPhysicsMaterial
- **llSetBuoyancy** — Set how gravity interacts with an object. Works in attachments (changes are applied to the avatar).

<!-- /wiki-source -->
