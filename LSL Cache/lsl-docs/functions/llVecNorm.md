---
name: "llVecNorm"
category: "function"
type: "function"
language: "LSL"
description: "Returns the normalised (unit) vector of a vector (magnitude 1.0)"
wiki_url: "https://wiki.secondlife.com/wiki/llVecNorm"
first_fetched: "2026-03-09"
last_updated: "2026-03-09"
signature: "vector llVecNorm(vector v)"
parameters:
  - name: "v"
    type: "vector"
    description: "The vector to normalise"
return_type: "vector"
energy_cost: "10.0"
sleep_time: "0.0"
patterns: ["llvecnorm"]
deprecated: "false"
---

# llVecNorm

```lsl
vector llVecNorm(vector v)
```

Returns the unit vector (magnitude = 1.0) in the same direction as `v`. Returns ZERO_VECTOR if `v` is ZERO_VECTOR.

## Return Value

`vector` — unit vector with magnitude 1.0, or ZERO_VECTOR if input is zero.

## Examples

```lsl
vector dir = llVecNorm(<3.0, 4.0, 0.0>);  // <0.6, 0.8, 0.0>
// Equivalent to: v / llVecMag(v)

// Direction from A to B
vector a = llGetPos();
vector b = targetPos;
vector direction = llVecNorm(b - a);
```

## See Also

- `llVecMag` — magnitude of a vector
- `llVecDist` — distance between two vectors
- `llRot2Fwd` / `llRot2Left` / `llRot2Up` — direction vectors from rotation


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llVecNorm) — scraped 2026-03-18_

Returns the vector that is vec normalized (a unit vector sharing the same direction as vec).

## Examples

```lsl
default {
    state_entry()
    {
        vector input = <1.0,2.0,3.0>;
        llSay(0,"The unit vector on "+(string)input+" is: "+(string)llVecNorm(input) );
    }
}
```

## Notes

- Mathematically equivalent to:

  - vec / llVecMag( vec )
  - vec / llSqrt( vec.x * vec.x + vec.y * vec.y + vec.z * vec.z )

## See Also

### Functions

- llVecMag
- llVecDist

<!-- /wiki-source -->
