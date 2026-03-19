---
name: "llRot2Left"
category: "function"
type: "function"
language: "LSL"
description: 'Computes the orientation of the local y-axis relative to the parent (i.e. relative to the root prim or the world).

Returns a vector that is the left vector defined by q, i.e. a unit vector pointing in the local positive Y direction'
signature: "vector llRot2Left(rotation q)"
return_type: "vector"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llRot2Left'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llrot2left"]
---

Computes the orientation of the local y-axis relative to the parent (i.e. relative to the root prim or the world).

Returns a vector that is the left vector defined by q, i.e. a unit vector pointing in the local positive Y direction


## Signature

```lsl
vector llRot2Left(rotation q);
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

- [SL Wiki](https://wiki.secondlife.com/wiki/llRot2Left)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llRot2Left) — scraped 2026-03-18_

Computes the orientation of the local y-axis relative to the parent (i.e. relative to the root prim or the world).Returns a vector that is the left vector defined by q, i.e. a unit vector pointing in the local positive Y direction

## Examples

```lsl
// Move an object 5 metres forwards along its own y axis, when touched, no matter how the object is oriented in world.
// Works for a root or child prim
default
{
    touch_start(integer total_number)
    {
        vector v = llRot2Left( llGetLocalRot() );
        llSetPos( llGetLocalPos() + v * 5 );
    }
}
```

## Notes

Can be useful to identify the orientation of the local  [sagittal-plane](https://en.wikipedia.org/wiki/sagittal_plane) of the prim, since it's y-axis is always perpendicular to this local sagittal-plane.

## See Also

### Functions

- llRot2Up
- llRot2Fwd
- llRot2Axis
- llRot2Angle

<!-- /wiki-source -->
