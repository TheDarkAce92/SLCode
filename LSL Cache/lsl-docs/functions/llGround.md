---
name: "llGround"
category: "function"
type: "function"
language: "LSL"
description: "Returns a float that is the ground height directly below the prim position + offset"
signature: "float llGround(vector offset)"
return_type: "float"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGround'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llground"]
---

Returns a float that is the ground height directly below the prim position + offset


## Signature

```lsl
float llGround(vector offset);
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

- [SL Wiki](https://wiki.secondlife.com/wiki/llGround)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGround) — scraped 2026-03-18_

Returns a float that is the ground height directly below the prim position + offset

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

- **llGroundContour** — Gets the ground contour
- **llGroundNormal** — Gets the ground normal
- **llGroundSlope** — Gets the ground slope
- **llEdgeOfWorld** — Returns existence of neighboring sims

<!-- /wiki-source -->
