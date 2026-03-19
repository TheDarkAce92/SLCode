---
name: "llTargetOmega"
category: "function"
type: "function"
language: "LSL"
description: "Rotates the object/prim around axis at a rate of spinrate * llVecMag(axis) in radians per second with strength gain."
signature: "void llTargetOmega(vector axis, float spinrate, float gain)"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llTargetOmega'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["lltargetomega"]
---

Rotates the object/prim around axis at a rate of spinrate * llVecMag(axis) in radians per second with strength gain.


## Signature

```lsl
void llTargetOmega(vector axis, float spinrate, float gain);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `vector` | `axis` | arbitrary axis to rotate the object around |
| `float` | `spinrate` | rate of rotation in radians per second |
| `float` | `gain` | also modulates the final spinrate and disables the rotation behavior if zero |


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llTargetOmega)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llTargetOmega) — scraped 2026-03-18_

Rotates the object/prim around axis at a rate of spinrate * llVecMag(axis) in radians per second with strength gain.

## Caveats

- If the object is not physical, then the rotation is only a client side effect, and it will collide as non-moving geometry.
- If the function does not appear to be working, make sure that that **Advanced > Network > Velocity Interpolate Objects** (viewer 1.x) or **Develop > Network > Velocity Interpolate Objects** (viewer 2.x) is enabled.
- As of server version 2025-09-03.17442317385, this prim property is maintained when copying in-world.

## Examples

```lsl
//rotates the x axis once per second,
//  rotates the y axis 3 times per second,
//  rotates the z axis once every two seconds.
//  combined the rate is about 3.20156 revolutions per second

llTargetOmega(<1.0,3.0,0.5>,TWO_PI,1.0);
```

```lsl
 //Rotates very slowly around a sphere's local X axis .... Good for making a globe that rotates around a tilted axis

default
{
    state_entry()
    {
       llTargetOmega(<1.0,0.0,0.0>*llGetRot(),0.1,0.01);
    }
}
```

```lsl
 //Rotates very slowly around a cylinder's local or global Z axis
 // .... Good for making a propeller that rotates regardless of initial orientation.

default
{
    state_entry()
    {
       llTargetOmega(llRot2Up(llGetLocalRot()), PI, 1.0);
    }
}
```

```lsl
//To make an object return to its initial rotation when target omega stops, first make the object
//   rotate both client side and server side. Then, when you stop llTargetOmega, reset server side rotation.
//   Here's one way to do it.

integer iOn;
integer iStep;

default
{
    touch_start(integer total_number)
    {
        iOn = !iOn;
        if (iOn)
        {
            llTargetOmega(<0.0,0.0,1.0>, PI/8, 1.0); // Start rotating client side with llTargetOmega
            llSetTimerEvent(1.0);  //Start timer to rotate server side
        }
        else
        {
            llTargetOmega(<0.0,0.0,1.0>, 0.0, 0.0); //Stop client side rotation
            llSetTimerEvent(0.0);   //Stop timer and thus server side rotation
            llSetRot(ZERO_ROTATION);    //Set server side rotation to <0.0,0.0,0.0>
            iStep = 0;
        }
    }

    timer()
    {
        llSetRot(llAxisAngle2Rot(<0.0,0.0,1.0> ,++iStep *PI/8));  // Rotate at the same speed as llTargetOmega
    }
}
```

## Notes

- Use llVecNorm on axis so that spinrate actually represents the rate of rotation.
- Set the gain to zero to disable and remove the rotation behavior, e.g. `llTargetOmega(ZERO_VECTOR, 0, 0)`;

  - When rotating stops, the object will keep its final orientation, which is only a client side effect. The final orientation observed by other viewers will be different, and new viewers (after omega has been stopped) will see the object in its real (pre-omega) orientation.
  - A spinrate of 0 with a non-zero gain causes the object to try to stop all spin, rather than simply clearing a previous `llTargetOmega()` call.
- If there are other forces applied to a prim together with `llTargetOmega()` (like using llSetForce to make the object float), use `llTargetOmega(-llGetOmega(), 0., 1.)` to cancel spin. Note that the gain must be non-zero, but not necessarily 1.

## See Also

### Functions

- **llRot2Fwd** — the earth
- **llRot2Left** — the earth
- **llRot2Up** — the earth

<!-- /wiki-source -->
