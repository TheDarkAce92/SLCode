---
name: "llGroundContour"
category: "function"
type: "function"
language: "LSL"
description: "Returns a vector that is the ground contour direction below the prim position + offset. The contour is the direction of a contour line at that point, that is the direction in which there is no change in elevation."
signature: "vector llGroundContour(vector offset)"
return_type: "vector"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGroundContour'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgroundcontour"]
---

Returns a vector that is the ground contour direction below the prim position + offset. The contour is the direction of a contour line at that point, that is the direction in which there is no change in elevation.


## Signature

```lsl
vector llGroundContour(vector offset);
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

- [SL Wiki](https://wiki.secondlife.com/wiki/llGroundContour)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGroundContour) — scraped 2026-03-18_

Returns a vector that is the ground contour direction below the prim position + offset. The contour is the direction of a contour line at that point, that is the direction in which there is no change in elevation.

## See Also

### Functions

- **llGround** — Gets the ground height
- **llGroundNormal** — Gets the ground normal
- **llGroundSlope** — Gets the ground slope

<!-- /wiki-source -->
