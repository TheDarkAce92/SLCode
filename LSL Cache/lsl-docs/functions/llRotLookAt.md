---
name: "llRotLookAt"
category: "function"
type: "function"
language: "LSL"
description: 'Causes an object to smoothly rotate to target_direction with strength resistance at damping force.

Maintains rotation target_direction until stopped with llStopLookAt.

To change the position in the same manner, use llMoveToTarget. For physical objects a range between .2 and 1 is good for both para'
signature: "void llRotLookAt(rotation target, float strength, float damping)"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llRotLookAt'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llrotlookat"]
---

Causes an object to smoothly rotate to target_direction with strength resistance at damping force.

Maintains rotation target_direction until stopped with llStopLookAt.

To change the position in the same manner, use llMoveToTarget. For physical objects a range between .2 and 1 is good for both parameters.


## Signature

```lsl
void llRotLookAt(rotation target, float strength, float damping);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `rotation` | `target_direction` |  |
| `float` | `strength` |  |
| `float` | `damping` | seconds to critically damp in |


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llRotLookAt)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llRotLookAt) — scraped 2026-03-18_

Causes an object to smoothly rotate to target_direction with strength resistance at damping force.

## Caveats

- In Non-Physical objects this function operates effectively the same as llSetLocalRot.
- damping seems to be capped at 1.0; greater values are reduced to 1.0 *(Tested 21 October 2010 on server version 10.10.18.212360)*
- The minimum value for strength seems to be 0.0445 for the function to have any effect.

## Examples

#### Point the prim's positive y axis (<0.0, 1.0, 0.0>) towards a position on the sim

```lsl
//-- where vPosTarget is the global position of the object you want to "look" at
llRotLookAt( llRotBetween( <0.0,1.0,0.0>, llVecNorm( vPosTarget - llGetPos() ) ), 1.0, 0.4 ); // Point +Y axis towards vPosTarget
```

- **vPosTarget - llGetPos()** converts the global coordinates of the objects, to a local distance and direction from the object pointing
- Per llRotBetween article:

  - **llRotBetween** returns a scaled rotation, unless both inputs are equal magnitude (e.g. unit vector).
  - The use of llVecNorm reduces the magnitude to 1 (so that both are equal magnitude), preventing errors.

#### Constraining the Rotation to One Axis

```lsl
      vector detected = llDetectedPos( 0 );
      vector pos = llGetPos();
      llRotLookAt( llRotBetween( <0.0, 1.0, 0.0>, llVecNorm(  - pos ) ), 1.0, 0.4 );
```

## See Also

### Functions

- llLookAt
- llStopLookAt
- llSetPhysicsMaterial
- llSetKeyframedMotion

<!-- /wiki-source -->
