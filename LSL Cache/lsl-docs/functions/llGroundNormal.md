---
name: "llGroundNormal"
category: "function"
type: "function"
language: "LSL"
description: "Returns a vector that is the ground normal from the current position + offset."
signature: "vector llGroundNormal(vector offset)"
return_type: "vector"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGroundNormal'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgroundnormal"]
---

Returns a vector that is the ground normal from the current position + offset.


## Signature

```lsl
vector llGroundNormal(vector offset);
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

- [SL Wiki](https://wiki.secondlife.com/wiki/llGroundNormal)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGroundNormal) — scraped 2026-03-18_

Returns a vector that is the ground  normal from the current position + offset.

## Notes

- There seems to some confusion be between a [Surface Normal](http://en.wikipedia.org/wiki/Normal_%28geometry%29) (the direction from the surface) and [Normalized Vector](http://en.wikipedia.org/wiki/Unit_vector) (a vector with a magnitude of 1.0, AKA Unit Vector). This function does **not** return a unit vector. Surface normals may encode additional information in the magnitude of the vector. If you need a Unit Vector, simply use llVecNorm.

## See Also

### Functions

- **llGround** — Gets the ground height
- **llGroundContour** — Gets the ground contour
- **llGroundSlope** — Gets the ground slope

<!-- /wiki-source -->
