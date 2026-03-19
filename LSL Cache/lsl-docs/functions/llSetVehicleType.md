---
name: "llSetVehicleType"
category: "function"
type: "function"
language: "LSL"
description: "Sets the vehicle type to one of the default types."
signature: "void llSetVehicleType(integer type)"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llSetVehicleType'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llsetvehicletype"]
---

Sets the vehicle type to one of the default types.


## Signature

```lsl
void llSetVehicleType(integer type);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `integer (vehicle_type)` | `type` |  |


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llSetVehicleType)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llSetVehicleType) — scraped 2026-03-18_

Sets the vehicle type to one of the default types.

## Caveats

Scripted Vehicles can have a maximum Physics weight of 32.0 Above that the function will fail with a warning on the Debug Channel.

## Examples

```lsl
llSetVehicleType(VEHICLE_TYPE_BALLOON);
```

## See Also

### Articles

The Linden Vehicle Tutorial

<!-- /wiki-source -->
