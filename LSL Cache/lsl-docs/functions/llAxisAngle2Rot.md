---
name: "llAxisAngle2Rot"
category: "function"
type: "function"
language: "LSL"
description: 'Returns a rotation that is a generated angle about axis

axis need not be normalized, only the direction is important.

angle need to be between the value 0<angle<PI (higher values than PI lead to 2*PI-angle), because a rotation is not really a rotation (it is more of a rigid motion/mirroring), the '
signature: "rotation llAxisAngle2Rot(vector axis, float angle)"
return_type: "rotation"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llAxisAngle2Rot'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llaxisangle2rot"]
---

Returns a rotation that is a generated angle about axis

axis need not be normalized, only the direction is important.

angle need to be between the value 0<angle<PI (higher values than PI lead to 2*PI-angle), because a rotation is not really a rotation (it is more of a rigid motion/mirroring), the final destination is the rotation. (in other words: it doesn't matter wether you rotate left by 90 degrees or right by 270 degrees it will return the same rotation).


## Signature

```lsl
rotation llAxisAngle2Rot(vector axis, float angle);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `vector` | `axis` |  |
| `float` | `angle` | expressed in radians. |


## Return Value

Returns `rotation`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llAxisAngle2Rot)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llAxisAngle2Rot) — scraped 2026-03-18_

Returns a rotation that is a generated angle about axis

## Examples

```lsl
default
{
    state_entry()
    {
        vector axis = <0.0, 0.0, 1.0>;
        float angle = 90.0 * DEG_TO_RAD;
        rotation rot = llAxisAngle2Rot(axis, angle);
        vector euler = llRot2Euler(rot) * RAD_TO_DEG;

        llOwnerSay((string) euler);
        //Says <0.0, 0.0, 90.0> since it is rotating 90 degrees on the Z axis caused by the 1.0 placed in the Z vector spot.
    }
}
```

## See Also

### Functions

- llRot2Angle
- llRot2Axis

<!-- /wiki-source -->
