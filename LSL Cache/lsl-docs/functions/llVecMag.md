---
name: "llVecMag"
category: "function"
type: "function"
language: "LSL"
description: "Returns a float that is the magnitude of the vector (the undirected non-negative distance from vec to <0.0, 0.0, 0.0>)."
signature: "float llVecMag(vector v)"
return_type: "float"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llVecMag'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llvecmag"]
---

Returns a float that is the magnitude of the vector (the undirected non-negative distance from vec to <0.0, 0.0, 0.0>).


## Signature

```lsl
float llVecMag(vector v);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `vector` | `vec` |  |


## Return Value

Returns `float`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llVecMag)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llVecMag) — scraped 2026-03-18_

Returns a float that is the magnitude of the vector (the undirected non-negative distance from vec to <0.0, 0.0, 0.0>).

## Examples

```lsl
default {
    state_entry()
    {
        vector input = <1.0,2.0,3.0>;
        llSay(0,"The magnitude of "+(string)input+" is "+(string)llVecMag(input) + ".");
    }
}
```

## Notes

- Mathematically the formula for vector magnitude is

  - `llSqrt(vec.x * vec.x + vec.y * vec.y + vec.z * vec.z)`
- Knowing this, there are ways to circumvent llVecMag for more efficient code.

  - vec*vec < 16.0 is over twice as fast as llVecMag(vec) < 4.0.
  - vec*vec < (dist*dist) is about twice as fast as llVecMag(vec) < dist.
  - This can work in many other ways, too, with other comparisons.

## See Also

### Functions

- **llVecNorm** — The vector normal
- **llVecDist** — The distance between two vectors

<!-- /wiki-source -->
