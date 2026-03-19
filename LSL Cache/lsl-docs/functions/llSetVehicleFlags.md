---
name: "llSetVehicleFlags"
category: "function"
type: "function"
language: "LSL"
description: "Enabled the specified vehicle flags"
signature: "void llSetVehicleFlags(integer flags)"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llSetVehicleFlags'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llsetvehicleflags"]
---

Enabled the specified vehicle flags


## Signature

```lsl
void llSetVehicleFlags(integer flags);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `integer (vehicle_flag)` | `flags` | mask of VEHICLE_FLAG_* flags |


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llSetVehicleFlags)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llSetVehicleFlags) — scraped 2026-03-18_

Enabled the specified vehicle flags

## Caveats

- Some vehicle flags may remain enabled after script reset. Use llRemoveVehicleFlags to disable any flags that would interfere with the correct functioning of your vehicle.
- VEHICLE_FLAG_MOUSELOOK_STEER and VEHICLE_FLAG_MOUSELOOK_BANK only turn the vehicle up to the current VEHICLE_ANGULAR_MOTOR_DIRECTION; If VEHICLE_ANGULAR_MOTOR_DIRECTION is set to ZERO_VECTOR, then the vehicle will not turn.

## See Also

### Functions

- **llRemoveVehicleFlags** — Remove vehicle flags

### Articles

- Linden Vehicle Tutorial

<!-- /wiki-source -->
