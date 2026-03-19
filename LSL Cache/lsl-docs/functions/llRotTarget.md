---
name: "llRotTarget"
category: "function"
type: "function"
language: "LSL"
description: 'This function is to have the script know when it has reached a rotation.
It registers a rot with a error that triggers at_rot_target and not_at_rot_target events continuously until unregistered.

Returns a handle (an integer) to unregister the target with llRotTargetRemove

A similar function exists'
signature: "integer llRotTarget(rotation rot, float error)"
return_type: "integer"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llRotTarget'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llrottarget"]
---

This function is to have the script know when it has reached a rotation.
It registers a rot with a error that triggers at_rot_target and not_at_rot_target events continuously until unregistered.

Returns a handle (an integer) to unregister the target with llRotTargetRemove

A similar function exists for positions: llTarget
This function does not rotate the object, to do that use llSetRot, llRotLookAt or llLookAt.


## Signature

```lsl
integer llRotTarget(rotation rot, float error);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `rotation` | `rot` | target rotation |
| `float` | `error` | angle in radians, defines when rot has been reached |


## Return Value

Returns `integer`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llRotTarget)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llRotTarget) — scraped 2026-03-18_

This function is to have the script know when it has reached a rotation.It registers a rot with a error that triggers at_rot_target and not_at_rot_target events continuously until unregistered.Returns a handle (an integer) to unregister the target with llRotTargetRemove

## Examples

```lsl
vector standrot = <0.0, 0.0, 0.0>;
vector fliprot = <45.0, 0.0, 0.0>;

// simple two-state rot target detection and rotation by Hypatia Callisto
// works, to detect a rotation target. An example I wrote
// since there is almost zilch for clean examples for
// at_rot_target, not_at_rot_target, llRotTarget, llRotTargetRemove

integer rottarget;

default
{

    state_entry(){
        rottarget = llRotTarget(llEuler2Rot(fliprot*DEG_TO_RAD), 0.1);
        llSetPrimitiveParams ([PRIM_ROTATION, llEuler2Rot(standrot*DEG_TO_RAD)]); // rotate to starting point
    }

    not_at_rot_target()
    {
        llRotTargetRemove( rottarget );
        llOwnerSay("not there"); //not at target
    }

    touch_start (integer total_number)
    {
        state rotatestate; // change to state for new position
    }
}


state rotatestate
{
    state_entry(){
        rottarget = llRotTarget(llEuler2Rot(fliprot*DEG_TO_RAD), 0.1);
        llSetPrimitiveParams ([PRIM_ROTATION, llEuler2Rot(fliprot*DEG_TO_RAD)]); // rotate to new point
    }

    at_rot_target(integer tnum, rotation targetrot, rotation ourrot)
    {
        llRotTargetRemove( rottarget );
        llOwnerSay("there"); //reached the target
    }

    touch_start(integer touched){
        state default;
    }

}
```

## See Also

### Events

| • at_rot_target | not_at_rot_target | – | rotational target events |  |
| --- | --- | --- | --- | --- |
| • at_target | not_at_target | – | positional target events |  |

### Functions

- **llRotTargetRemove** — Cancel a target rotation
- **llTarget** — Register a target position
- **llTargetRemove** — Cancel a target position

<!-- /wiki-source -->
