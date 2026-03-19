---
name: "llGetPhysicsMaterial"
category: "function"
type: "function"
language: "LSL"
description: 'Used to get the physical characteristics of an object.

Returns a list in the form [ float gravity_multiplier, float restitution, float friction, float density ]

The default values for friction and restitution depend upon the material type.'
signature: "list llGetPhysicsMaterial()"
return_type: "list"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetPhysicsMaterial'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgetphysicsmaterial"]
---

Used to get the physical characteristics of an object.

Returns a list in the form [ float gravity_multiplier, float restitution, float friction, float density ]

The default values for friction and restitution depend upon the material type.


## Signature

```lsl
list llGetPhysicsMaterial();
```


## Return Value

Returns `list`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetPhysicsMaterial)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetPhysicsMaterial) — scraped 2026-03-18_

Used to get the physical characteristics of an object.Returns a list in the form [ float gravity_multiplier, float restitution, float friction, float density ]

## Caveats

- A collision between two objects with restitution 1.0 will still not be perfectly elastic due to damping in the physics engine.

## Examples

```lsl
default
{
    touch_start(integer total_number)
    {
        list params = llGetPhysicsMaterial();
        llOwnerSay(
            "\nGravity multiplier: " + (string)llList2Float(params, 0) +
            "\nRestitution: " + (string)llList2Float(params, 1) +
            "\nFriction: " + (string)llList2Float(params, 2) +
            "\nDensity: " + (string)llList2Float(params, 3) + "kg/m^3"
        );
    }
}
```

## See Also

### Constants

- PRIM_MATERIAL

### Functions

- llSetPhysicsMaterial

<!-- /wiki-source -->
