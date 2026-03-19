---
name: "llSetVehicleVectorParam"
category: "function"
type: "function"
language: "LSL"
description: "Sets the vehicle vector parameter param to vec."
signature: "void llSetVehicleVectorParam(integer param, vector vec)"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llSetVehicleVectorParam'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llsetvehiclevectorparam"]
---

Sets the vehicle vector parameter param to vec.


## Signature

```lsl
void llSetVehicleVectorParam(integer param, vector vec);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `integer (vehicle_vector)` | `param` | VEHICLE_* flag |
| `vector` | `vec` |  |


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llSetVehicleVectorParam)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llSetVehicleVectorParam) — scraped 2026-03-18_

Sets the vehicle vector parameter param to vec.

## Notes

- VEHICLE_ANGULAR_MOTOR_DIRECTION may conflict with any active llTargetOmega set in the root prim and prevent vehicle turns.  Call llTargetOmega with a gain of 0 to disable it.

## See Also

### Functions

- **llSetVehicleRotationParam** — Sets a vehicle rotation parameter
- **llSetVehicleFloatParam** — Sets a vehicle float parameter

### Articles

- Linden Vehicle Tutorial

<!-- /wiki-source -->
