---
name: "llGetAccel"
category: "function"
type: "function"
language: "LSL"
description: "Returns a vector that is the acceleration of the object in the region frame of reference."
signature: "vector llGetAccel()"
return_type: "vector"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetAccel'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgetaccel"]
---

Returns a vector that is the acceleration of the object in the region frame of reference.


## Signature

```lsl
vector llGetAccel();
```


## Return Value

Returns `vector`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetAccel)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetAccel) — scraped 2026-03-18_

Returns a vector that is the acceleration of the object in the region frame of reference.

## Caveats

- Returns ZERO_VECTOR in attachments regardless of the avatar's acceleration.
- Returns ZERO_VECTOR in child prims regardless of the linkset's acceleration.

## Examples

```lsl
//A very simple (and not very effective) way of keeping a physical object in place.
//If the object is moving when the script is put in the object, then the object will continue to move, so long as it doesn't accelerate.
//If you ever want to actually stop an object, use llMoveToTarget(llGetPos(), .1)
default {
    moving_start(){
        vector ac;
        // Go forever
        while(llVecMag(ac = llGetAccel()) > .001) { //We're accelerating...
            llApplyImpulse(-ac, 0); //Slow us down.
        }
    }
}
```

## See Also

### Functions

- llGetOmega
- llGetVel
- llGetTorque
- llGetMass
- llGetForce
- llSetForce
- llSetTorque
- llSetForceAndTorque

<!-- /wiki-source -->
