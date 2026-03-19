---
name: "llSetAngularVelocity"
category: "function"
type: "function"
language: "LSL"
description: "Applies rotational velocity to object. It does the same job as llApplyRotationalImpulse but doesn't depend of the mass of object."
signature: "void llSetAngularVelocity(vector angular_velocity, integer local)"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llSetAngularVelocity'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llsetangularvelocity"]
---

Applies rotational velocity to object. It does the same job as llApplyRotationalImpulse but doesn't depend of the mass of object.


## Signature

```lsl
void llSetAngularVelocity(vector angular_velocity, integer local);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `vector` | `initial_omega` |  |
| `integer (boolean)` | `local` | boolean, if TRUE force is treated as a local directional vector, if FALSE force is treated as a region directional vector |


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llSetAngularVelocity)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llSetAngularVelocity) — scraped 2026-03-18_

Applies rotational velocity to object. It does the same job as llApplyRotationalImpulse but doesn't depend of the mass of object .

## Caveats

- Only works in  physics-enabled objects.

## Examples

Instances :

one regular cube with mass M , and gravity 0 ( to disable the gravity) ; the object is homogenous and with only one prim so, its center of mass is its center of the object and its physical axis of rotation are its local axis  :

- LlSetAngularVelocity(<0,0,1>, TRUE ) => starts to rotate around its Z local axis with a start value of omega = 1 radian /second , and slows down over time until it won't rotate
- llApplyRotationalImpulse(<0,0,1>, TRUE ) => starts to rotate around its Z local axis with a start value of omega = 1/M radian /second , and slows down over time until it won't rotate
- llTargetOmega(<0.0,0.0,1.0>, 1.0, 1.0) => if the object is physical , starts to rotate around its Z local axis with a start value of omega = 1 radian / second . It won t slow down over time

## See Also

### Functions

- llApplyRotationalImpulse
- llSetVelocity

<!-- /wiki-source -->
