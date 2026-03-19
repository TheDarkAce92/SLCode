---
name: "llRot2Axis"
category: "function"
type: "function"
language: "LSL"
description: 'Returns a vector the rotation axis represented by rot

Use in conjunction with llRot2Angle.
To undo use llAxisAngle2Rot or llAxes2Rot.'
signature: "vector llRot2Axis(rotation rot)"
return_type: "vector"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llRot2Axis'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llrot2axis"]
---

Returns a vector the rotation axis represented by rot

Use in conjunction with llRot2Angle.
To undo use llAxisAngle2Rot or llAxes2Rot.


## Signature

```lsl
vector llRot2Axis(rotation rot);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `rotation` | `rot` |  |


## Return Value

Returns `vector`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llRot2Axis)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llRot2Axis) — scraped 2026-03-18_

Returns a vector the rotation axis represented by rot

## See Also

### Functions

- llRot2Angle
- llAxisAngle2Rot
- llRot2Left
- llRot2Fwd
- llRot2Up

### Articles

- Slerp

<!-- /wiki-source -->
