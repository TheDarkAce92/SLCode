---
name: "llEuler2Rot"
category: "function"
type: "function"
language: "LSL"
description: "Converts Euler angles (in radians) to a rotation quaternion"
wiki_url: "https://wiki.secondlife.com/wiki/llEuler2Rot"
first_fetched: "2026-03-09"
last_updated: "2026-03-09"
signature: "rotation llEuler2Rot(vector v)"
parameters:
  - name: "v"
    type: "vector"
    description: "Euler angles in radians as <x, y, z>"
return_type: "rotation"
energy_cost: "10.0"
sleep_time: "0.0"
patterns: ["lleuler2rot"]
deprecated: "false"
---

# llEuler2Rot

```lsl
rotation llEuler2Rot(vector v)
```

Converts Euler angles (in radians) to a rotation quaternion. Rotation order is X, then Y, then Z.

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `v` | vector | `<pitch, roll, yaw>` in radians (X=pitch, Y=roll, Z=yaw) |

## Examples

```lsl
// 45 degrees around Z axis (yaw)
rotation rot = llEuler2Rot(<0.0, 0.0, 45.0 * DEG_TO_RAD>);
llSetRot(rot);

// Rotate incrementally
rotation increment = llEuler2Rot(<0.0, 0.0, 1.0 * DEG_TO_RAD>);
llSetRot(llGetRot() * increment);

// Common: face a direction
vector targetDir = llVecNorm(targetPos - llGetPos());
rotation faceRot = llRotBetween(<1.0, 0.0, 0.0>, targetDir);
llSetRot(faceRot);
```

## See Also

- `llRot2Euler` — convert rotation to Euler angles
- `llAxisAngle2Rot` — rotation from axis + angle
- `llSetRot` — apply rotation to prim
- `DEG_TO_RAD` — degrees to radians conversion constant


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llEuler2Rot) — scraped 2026-03-18_

Returns a rotation representation of the  Euler Angles v.

## Examples

```lsl
default
{
    state_entry()
    {
        vector input = <73.0, -63.0, 20.0> * DEG_TO_RAD;
        rotation rot = llEuler2Rot(input);
        llSay(0,"The Euler2Rot of "+(string)input+" is: "+(string)rot );
    }
}
```

## Notes

```lsl
v/=2;
rotation k = <0.0, 0.0, llSin(v.z), llCos(v.z)> * <0.0, llSin(v.y), 0.0, llCos(v.y)> * ;
```

## See Also

### Functions

- llRot2Euler

### Articles

<!-- /wiki-source -->
