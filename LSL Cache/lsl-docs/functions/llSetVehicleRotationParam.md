---
name: "llSetVehicleRotationParam"
category: "function"
type: "function"
language: "LSL"
description: "Sets the vehicle rotation parameter param to rot."
signature: "void llSetVehicleRotationParam(integer param, rotation rot)"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llSetVehicleRotationParam'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llsetvehiclerotationparam"]
---

Sets the vehicle rotation parameter param to rot.


## Signature

```lsl
void llSetVehicleRotationParam(integer param, rotation rot);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `integer (vehicle_rotation)` | `param` | VEHICLE_* flag |
| `rotation` | `rot` |  |


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llSetVehicleRotationParam)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llSetVehicleRotationParam) — scraped 2026-03-18_

Sets the vehicle rotation parameter param to rot.

## Examples

The reference frame can be computed and set in two steps:

1. Place the vehicle with front facing east(red arrow) and with left side facing north(green arrow)
1. llSetVehicleRotationParam( VEHICLE_REFERENCE_FRAME, ZERO_ROTATION / llGetRootRotation());

## See Also

### Functions

- **llSetVehicleFloatParam** — Sets a vehicle float parameter
- **llSetVehicleVectorParam** — Sets a vehicle vector parmeter

### Articles

- Linden Vehicle Tutorial

<!-- /wiki-source -->
