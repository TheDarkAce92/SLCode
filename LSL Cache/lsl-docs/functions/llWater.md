---
name: "llWater"
category: "function"
type: "function"
language: "LSL"
description: 'Returns a float that is the water height below the prim's position + offset

The requested position needs to be in the same region.
Only the x and y coordinates in offset are important, the z component is ignored.
Water height is constant across each entire sim and is typically 20 meters but not alw'
signature: "float llWater(vector offset)"
return_type: "float"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llWater'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llwater"]
---

Returns a float that is the water height below the prim's position + offset

The requested position needs to be in the same region.
Only the x and y coordinates in offset are important, the z component is ignored.
Water height is constant across each entire sim and is typically 20 meters but not always.


## Signature

```lsl
float llWater(vector offset);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `vector` | `offset` | offset relative to the prim's position and expressed in local coordinates |


## Return Value

Returns `float`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llWater)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llWater) — scraped 2026-03-18_

Returns a float that is the water height below the prim's position + offset

## Examples

```lsl
// Makes the object land on ground or on water

FindGroundOrWater()
{
    vector vTarget = llGetPos();
    vTarget.z = llGround( ZERO_VECTOR );
    float fWaterLevel = llWater( ZERO_VECTOR );
    if( vTarget.z < fWaterLevel )
        vTarget.z = fWaterLevel;
    llSetRegionPos(vTarget);
}

default
{
    touch_start(integer total_number)
    {
        FindGroundOrWater();
    }
}
```

## See Also

### Functions

- **llGround** — Gets the ground height
- **llWind** — Gets the wind velocity
- **llCloud** — Gets the cloud density

<!-- /wiki-source -->
