---
name: "llSetTorque"
category: "function"
type: "function"
language: "LSL"
description: "Sets the torque of object (if the script is physical)"
signature: "void llSetTorque(vector torque, integer local)"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llSetTorque'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llsettorque"]
---

Sets the torque of object (if the script is physical)


## Signature

```lsl
void llSetTorque(vector torque, integer local);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `vector` | `torque` |  |
| `integer (boolean)` | `local` | boolean, if TRUE uses the local axis, if FALSE uses the region region axis |


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llSetTorque)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llSetTorque) — scraped 2026-03-18_

Sets the torque of object (if the script is physical)

## Caveats

- Only works in  physics-enabled objects.

## Examples

```lsl
default
{
    touch_start(integer total_number)
    {
        llSetTorque(<0,10,0>,1);
                   //X  Y Z  Local
    }
}
```

## See Also

### Functions

- llSetForceAndTorque
- llSetForce

<!-- /wiki-source -->
