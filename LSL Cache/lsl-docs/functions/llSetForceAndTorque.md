---
name: "llSetForceAndTorque"
category: "function"
type: "function"
language: "LSL"
description: "Sets the force and torque of object (if the script is physical)"
signature: "void llSetForceAndTorque(vector force, vector torque, integer local)"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llSetForceAndTorque'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llsetforceandtorque"]
---

Sets the force and torque of object (if the script is physical)


## Signature

```lsl
void llSetForceAndTorque(vector force, vector torque, integer local);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `vector` | `force` | directional force |
| `vector` | `torque` | torque force |
| `integer (boolean)` | `local` | boolean, if TRUE force is treated as a local directional vector, if FALSE force is treated as a region directional vector |


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llSetForceAndTorque)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llSetForceAndTorque) — scraped 2026-03-18_

Sets the force and torque of object (if the script is physical)

## Caveats

- Only works in  physics-enabled objects.
- If either value is ZERO_VECTOR, the function eliminates both forces. Both values must be non-zero for this function to work. (The workaround to this is setting both separately.)

## Examples

```lsl
default
{
    touch_start(integer total_number)
    {
        llSetForceAndTorque( <0.0,0.0,5.0>, <1.0,0.0,0.0>, FALSE );
    }
}
```

## See Also

### Functions

- llSetForce
- llSetTorque

<!-- /wiki-source -->
