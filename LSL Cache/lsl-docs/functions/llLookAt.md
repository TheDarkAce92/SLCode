---
name: "llLookAt"
category: "function"
type: "function"
language: "LSL"
description: 'Cause object to point its up axis (positive z) towards target, while keeping its forward axis (positive x) below the horizon.

Continues to track target until llStopLookAt is called.

To change the position in the same manner use llMoveToTarget.'
signature: "void llLookAt(vector target, float strength, float damping)"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llLookAt'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["lllookat"]
---

Cause object to point its up axis (positive z) towards target, while keeping its forward axis (positive x) below the horizon.

Continues to track target until llStopLookAt is called.

To change the position in the same manner use llMoveToTarget.


## Signature

```lsl
void llLookAt(vector target, float strength, float damping);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `vector` | `target` | position in region coordinates |
| `float` | `strength` |  |
| `float` | `damping` | seconds to critically damp in |


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llLookAt)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llLookAt) — scraped 2026-03-18_

Cause object to point its up axis (positive z) towards target, while keeping its forward axis (positive x) below the horizon.

## Caveats

- There is no guarantee that the host objects will wind up pointing at the target. Depending on the shape of the object, the strength and the damping, it may well settle out at a different rotation pointing in a different direction if the damping stops the rotation before the final position is reached.
- If the prim is not the root, then target will need correction for the root prim's rotation (see example below).
- If the object is an attachment, then target will need correction for the wearer's rotation.
- If the host object is physical and not symmetrical it may cause a recoil effect where the object winds up drifting away from it's original position as well as making the final rotation it settles on less accurate.

## Examples

```lsl
//Causes Object to look at nearest Avatar.
default
{
    state_entry()
    {
        llSensorRepeat("", "", AGENT, 20.0, PI, 0.2);
    }

    sensor(integer total_number)
    {
        llLookAt( llDetectedPos(0) + <0.0, 0.0, 1.0>, 3.0, 1.0 );
    }
}
```

```lsl
// Same as above, but for use inside a child prim or the root of an attachment.
// Make the child or attachment look at nearest Avatar.

default
{
    state_entry()
    {
        llSensorRepeat("", "", AGENT, 20.0, PI, 0.2);
    }

    sensor(integer total_number)
    {
        vector p = llGetPos();
        llLookAt(p + (llDetectedPos(0) + <0.0, 0.0, 1.0> - p) / llGetRootRotation(), 3.0, 1.0);
    }
}
```

## See Also

### Functions

- llRotLookAt
- llStopLookAt

<!-- /wiki-source -->
