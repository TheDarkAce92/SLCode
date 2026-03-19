---
name: "llGetOmega"
category: "function"
type: "function"
language: "LSL"
description: "Returns a vector that is the rotation velocity of the object in radians per second."
signature: "vector llGetOmega()"
return_type: "vector"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetOmega'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgetomega"]
---

Returns a vector that is the rotation velocity of the object in radians per second.


## Signature

```lsl
vector llGetOmega();
```


## Return Value

Returns `vector`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetOmega)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetOmega) — scraped 2026-03-18_

Returns a vector that is the rotation velocity of the object in radians per second.

## Caveats

- Returns the omega of the root if called in a child prim.

## Examples

```lsl
default
{
    state_entry()
    {
        llTargetOmega(<0,0,0.5>, 1, 1);
    }

    touch_start(integer total_number)
    {
        vector omega = llGetOmega();
        llSay(0, (string)omega);
    }
}
```

## See Also

### Functions

- llGetAccel
- llGetVel
- **llGetForce** — Gets the objects force
- llGetTorque
- llGetMass
- **llTargetOmega** — Rotates the object around axis

<!-- /wiki-source -->
