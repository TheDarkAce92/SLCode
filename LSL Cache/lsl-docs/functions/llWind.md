---
name: "llWind"
category: "function"
type: "function"
language: "LSL"
description: 'Returns a vector that is the wind velocity at the prim's position + offset

The requested position needs to be in the same region.
Only the x and y coordinates in offset are important, the z component is ignored.'
signature: "vector llWind(vector offset)"
return_type: "vector"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llWind'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llwind"]
---

Returns a vector that is the wind velocity at the prim's position + offset

The requested position needs to be in the same region.
Only the x and y coordinates in offset are important, the z component is ignored.


## Signature

```lsl
vector llWind(vector offset);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `vector` | `offset` | offset relative to the prim's position and expressed in local coordinates |


## Return Value

Returns `vector`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llWind)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llWind) — scraped 2026-03-18_

Returns a vector that is the wind velocity at the prim's position + offset

## Examples

```lsl
default
{
    touch_start(integer num)
    {
        llSay(0, "Wind velocity: " + (string)llWind(ZERO_VECTOR));
    }
}
```

```lsl
// wind interpretation as angle and speed
default
{
    state_entry()
    {
        vector windVector = llWind( ZERO_VECTOR);
        float windSpeed = llVecMag( windVector);
        float windDirection = llAtan2( windVector.y, windVector.x);
        integer compassWind = ( 450 - (integer)( RAD_TO_DEG*windDirection))%360;
        llOwnerSay( "\nWind direction: "+(string)compassWind+"°\nWind speed: "+(string)windSpeed+" m/S");
    }
}
```

## Notes

- Each region simulates its own wind with a random seed value, and chaos is scaled by the region's sun position.

  - While the simulation is performed on a 16x16 grid, the wind has perfect resolution anywhere between those cells. (interpolated)
  - This low resolution tends to result in smooth gradients of wind, however sudden and strong changes in wind speed and direction are possible.
  - Vortexes and are also possible, sometimes multiple in the same region.
- Neighboring regions influence each other at the connecting border, which may lead to cascading changes for either region.
- Regions without neighbors exhibit very uniform wind across the whole region.

  - Wind will occasionally change direction over time, but eventually stabilizes toward the new direction.
- Maximum wind speed can reach at least 20m/s.

## See Also

### Functions

- llCloud

### Articles

- **Weather** — SL Weather information
- Moderated in-world wind

<!-- /wiki-source -->
