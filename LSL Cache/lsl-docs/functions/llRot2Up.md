---
name: "llRot2Up"
category: "function"
type: "function"
language: "LSL"
description: 'Computes the orientation of the local z-axis relative to the parent (i.e. the root prim or the world).

Returns a vector that is the up vector defined by q, i.e. a unit vector pointing in the positive Z direction'
signature: "vector llRot2Up(rotation q)"
return_type: "vector"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llRot2Up'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llrot2up"]
---

Computes the orientation of the local z-axis relative to the parent (i.e. the root prim or the world).

Returns a vector that is the up vector defined by q, i.e. a unit vector pointing in the positive Z direction


## Signature

```lsl
vector llRot2Up(rotation q);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `rotation` | `q` |  |


## Return Value

Returns `vector`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llRot2Up)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llRot2Up) — scraped 2026-03-18_

Computes the orientation of the local z-axis relative to the parent (i.e. the root prim or the world).Returns a vector that is the up vector defined by q, i.e. a unit vector pointing in the positive Z direction

## Examples

```lsl
// Move a prim 5 metres forwards along its own z axis, when touched, no matter how the object is oriented in world.
// Works for a root or child prim
default
{
    touch_start(integer total_number)
    {
        vector v = llRot2Up( llGetLocalRot() );
        llSetPos( llGetLocalPos() + v * 5 );
    }
}
```

## Notes

Can be useful to identify the orientation of the local horizontal-plane of the prim, since it's z-axis is always perpendicular to this local horizontal plane.

## See Also

### Functions

- llRot2Left
- llRot2Fwd
- llRot2Axis
- llRot2Angle

<!-- /wiki-source -->
