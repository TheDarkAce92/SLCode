---
name: "llRot2Angle"
category: "function"
type: "function"
language: "LSL"
description: 'Returns a float that is the rotation angle represented by rot

Use in conjunction with llRot2Axis.
To undo use llAxisAngle2Rot.'
signature: "float llRot2Angle(rotation rot)"
return_type: "float"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llRot2Angle'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llrot2angle"]
---

Returns a float that is the rotation angle represented by rot

Use in conjunction with llRot2Axis.
To undo use llAxisAngle2Rot.


## Signature

```lsl
float llRot2Angle(rotation rot);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `rotation` | `rot` |  |


## Return Value

Returns `float`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llRot2Angle)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llRot2Angle) — scraped 2026-03-18_

Returns a float that is the rotation angle represented by rot

## Caveats

This always returns a positive angle <= PI radians, that is, it is the unsigned minimum angle. A rotation of 3/2 PI radians (270 degrees) will return an angle of PI / 2 radians, not -PI / 2.

## See Also

### Functions

- llAxisAngle2Rot
- llRot2Axis
- llRot2Up
- llRot2Fwd
- llRot2Left
- **llAngleBetween** — Similar functionality.

<!-- /wiki-source -->
