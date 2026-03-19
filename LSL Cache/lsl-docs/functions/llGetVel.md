---
name: "llGetVel"
category: "function"
type: "function"
language: "LSL"
description: 'Returns a vector that is the velocity of the object.

Speed is the magnitude of the velocity. Speed is measured in meter per second.
Velocity reported is relative to the global coordinate frame (the object rotation has no affect on this functions output).
For physic objects, velocity is the velocity'
signature: "vector llGetVel()"
return_type: "vector"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetVel'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgetvel"]
---

Returns a vector that is the velocity of the object.

Speed is the magnitude of the velocity. Speed is measured in meter per second.
Velocity reported is relative to the global coordinate frame (the object rotation has no affect on this functions output).
For physic objects, velocity is the velocity of its center of mass llGetCenterOfMass. ( When the object has some torque and has not force, position of the object moves ( it turns ), but its center of mass is unchanged, so the velocity is null )


## Signature

```lsl
vector llGetVel();
```


## Return Value

Returns `vector`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetVel)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetVel) — scraped 2026-03-18_

Returns a vector that is the velocity of the object.

## Examples

```lsl
//A very simple (and not very effective) way of keeping a physical object in place.
//If you ever want to actually stop an object, use llMoveToTarget(llGetPos(), .1)

default
{
    state_entry()
    {
        vector spd;
        {
            @loop;
            if (llVecMag(spd = llGetVel()) > .001)
            { //We're accelerating...
                llApplyImpulse(-spd, 0); //Slow us down.
            }
        jump loop;
        }
    }
}//Written by Xaviar Czervik
```

## Notes

To get the velocity relative the local frame (the direction the object is pointing), divide the output of this function by that of its rotation.

```lsl
vector local_vel = llGetVel() / llGetRot()
```

## See Also

### Functions

- llGetAccel
- llGetOmega
- **llGetForce** — Gets the objects force
- llGetTorque
- llGetMass

<!-- /wiki-source -->
