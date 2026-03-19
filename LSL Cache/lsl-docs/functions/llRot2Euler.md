---
name: "llRot2Euler"
category: "function"
type: "function"
language: "LSL"
description: "Returns a vector that is the Euler representation (roll, pitch, yaw) of quat, with each component expressed in radians."
signature: "vector llRot2Euler(rotation q)"
return_type: "vector"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llRot2Euler'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llrot2euler"]
---

Returns a vector that is the Euler representation (roll, pitch, yaw) of quat, with each component expressed in radians.


## Signature

```lsl
vector llRot2Euler(rotation q);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `rotation` | `quat` | Any valid rotation |


## Return Value

Returns `vector`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llRot2Euler)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llRot2Euler) — scraped 2026-03-18_

Returns a vector that is the Euler representation (roll, pitch, yaw) of quat, with each component expressed in radians.

## Caveats

- Angles greater than PI radians (180 degrees) are returned as negative angles.

## Examples

```lsl
default
{
    state_entry()
    {
        rotation input = llGetRot();
        llSay(0, "The Rot2Euler of " + (string)input + " is: " + (string) llRot2Euler(input) );
    }
}
```

```lsl
// This script rotates a prim by 15 degrees each time the prim is touched

// While not the best way of achieving the result,
// this script demonstrates the use of llRot2Euler and llEuler2Rot
// and the use of more human-friendly degrees rather than radians

default
{
    touch_start(integer total_number)
    {
        // Get the object's current rotation as a quarternion
        rotation rot = llGetRot();
        // Convert the rotation to a euler with roll, pitch, and yaw in radians
        vector euler = llRot2Euler(rot);
        // convert the angles from radians to degrees
        euler *= RAD_TO_DEG;
        // Add 15 degrees on the Z axis
        euler += <0, 0, 15>;
        // Say the current euler values in degrees
        llSay(0, (string) euler);
        // convert degrees back to radians
        euler *= DEG_TO_RAD;
        // Convert the euler back to a rotation quarternion
        rot =  llEuler2Rot (euler);
        // Apply the updated rotation to the prim
        llSetRot( rot );
    }
}
```

## See Also

### Functions

- llEuler2Rot

### Articles

<!-- /wiki-source -->
