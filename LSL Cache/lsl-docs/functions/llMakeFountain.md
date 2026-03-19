---
name: "llMakeFountain"
category: "function"
type: "function"
language: "LSL"
description: "Make a fountain of particles"
signature: "void llMakeFountain(integer particles, float scale, float vel, float lifetime, float arc, integer bounce, string texture, vector offset, float bounce_offset)"
return_type: "void"
sleep_time: "0.1"
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llMakeFountain'
deprecated: "true"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
---

Make a fountain of particles


## Signature

```lsl
void llMakeFountain(integer particles, float scale, float vel, float lifetime, float arc, integer bounce, string texture, vector offset, float bounce_offset);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `integer` | `particles` |  |
| `float` | `scale` |  |
| `float` | `vel` |  |
| `float` | `lifetime` |  |
| `float` | `arc` |  |
| `integer` | `bounce` |  |
| `string` | `texture` | a texture in the inventory of the prim this script is in or a UUID of a texture |
| `vector` | `offset` | offset relative to the prim's position and expressed in local coordinates and is completely ignored. |
| `float` | `bounce_offset` | offset relative to the prim's position and expressed in local coordinates and is completely ignored |


## Caveats

- Forced delay: **0.1 seconds** — the script sleeps after each call.
- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llMakeFountain)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llMakeFountain) — scraped 2026-03-18_

Make a fountain of particles

## Caveats

- This function causes the script to sleep for 0.1 seconds.
- This function has been deprecated, please use llParticleSystem instead.
- offset functionality has been removed, any value provided is completely ignored. For future proofing purposes, you should use a ZERO_VECTOR for it's value.
- If texture is missing from the prim's inventory  and it is not a UUID or it is not a texture then an error is shouted on DEBUG_CHANNEL.
- If texture is a UUID then there are no new asset permissions consequences for the object.

  - The resulting object develops no new usage restrictions that might have occurred if the asset had been placed in the prims inventory.

## Notes

Beginning in 1.14, the simulator will be using llParticleSystem to emulate legacy llMakeFountain particles.

```lsl
llMakeFountain(integer particle_count,
              float particle_scale,
              float particle_speed,
              float particle_lifetime,
              float source_cone,
              integer source_bounce,
              string source_texture_id,
              vector local_offset,
              vector bounce_offset);
```

```lsl
fakeMakeFountain(integer particle_count, float particle_scale, float particle_speed,
                float particle_lifetime, float source_cone, integer bounce,
                string source_texture_id, vector local_offset, vector bounce_offset)
{
//      local_offset is ignored
//      bounce is ignored
//      bounce_offset is ignored
    llParticleSystem([
        PSYS_PART_FLAGS,            PSYS_PART_INTERP_COLOR_MASK | PSYS_PART_INTERP_SCALE_MASK | PSYS_PART_WIND_MASK | PSYS_PART_BOUNCE_MASK | PSYS_PART_EMISSIVE_MASK,
        PSYS_SRC_PATTERN,           PSYS_SRC_PATTERN_ANGLE_CONE,
        PSYS_PART_START_COLOR,      <1.0, 1.0, 1.0>,
        PSYS_PART_END_COLOR,        <1.0, 1.0, 1.0>,
        PSYS_PART_START_ALPHA,      0.50,
        PSYS_PART_END_ALPHA,        0.25,
        PSYS_PART_START_SCALE,

,
        PSYS_PART_END_SCALE,        <0.0, 0.0, 0.0>,
        PSYS_PART_MAX_AGE,          3.0,
        PSYS_SRC_ACCEL,             <1.0, 0.0, -4>,
        PSYS_SRC_TEXTURE,           source_texture_id,
        PSYS_SRC_BURST_RATE,        5/particle_count,
        PSYS_SRC_ANGLE_BEGIN,       0.0,
        PSYS_SRC_ANGLE_END,         source_cone*PI,
        PSYS_SRC_BURST_PART_COUNT,  1,
        PSYS_SRC_BURST_RADIUS,      0.0,
        PSYS_SRC_BURST_SPEED_MIN,   particle_speed,
        PSYS_SRC_BURST_SPEED_MAX,   particle_speed,
        PSYS_SRC_MAX_AGE,           particle_lifetime/2,
        PSYS_SRC_OMEGA,             <0.0, 0.0, 0.0>
    ]);
}
//    Known discrepancies:
//    1) The bounce level is not adjustable with the new particle system,
//       it will be fixed to 0
//    2) The original llMakeFountain has random particle lifetime, which cannot be
//       created in the current particle system via a single call
//    3) several values are not taken 'verbatim' in the original particle system
//       (velocity is not m/sec for instance, and number of particles seems to be
//       wildly off), these are approximated loosely in this simulation via basic
//       divisors, which may not work out the same in some scenarios
//    4) There is no way to duplicate the offset from the old functions within the
//       new particle system
```

<!-- /wiki-source -->
