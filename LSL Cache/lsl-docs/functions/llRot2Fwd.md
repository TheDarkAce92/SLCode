---
name: "llRot2Fwd"
category: "function"
type: "function"
language: "LSL"
description: 'Computes the orientation of the local x-axis relative to the parent (i.e. the root prim or the world).

Returns a vector that is the forward vector defined by q, i.e. a unit vector pointing in the local positive X direction.'
signature: "vector llRot2Fwd(rotation q)"
return_type: "vector"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llRot2Fwd'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llrot2fwd"]
---

Computes the orientation of the local x-axis relative to the parent (i.e. the root prim or the world).

Returns a vector that is the forward vector defined by q, i.e. a unit vector pointing in the local positive X direction.


## Signature

```lsl
vector llRot2Fwd(rotation q);
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

- [SL Wiki](https://wiki.secondlife.com/wiki/llRot2Fwd)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llRot2Fwd) — scraped 2026-03-18_

Computes the orientation of the local x-axis relative to the parent (i.e. the root prim or the world).Returns a vector that is the forward vector defined by q, i.e. a unit vector pointing in the local positive X direction.

## Examples

```lsl
// Move an object 5 metres forwards along its x axis, when touched, no matter how the object is oriented in world.
// Works for a root or child prim
default
{
    touch_start(integer total_number)
    {
        vector v = llRot2Fwd( llGetLocalRot() );
        llSetPos( llGetLocalPos() + v * 5 );
    }
}
```

## Notes

Can be useful to identify the orientation of the local frontal-plane of the prim, since its x-axis is always perpendicular to this local frontal plane.

## See Also

### Functions

- llRot2Left
- llRot2Up
- llRot2Axis
- llRot2Angle

<!-- /wiki-source -->
