---
name: "llSetBuoyancy"
category: "function"
type: "function"
language: "LSL"
description: 'Sets the buoyancy of the task or object. Requires physics to be enabled.

A buoyancy value of 0.0 disables the effect
when buoyancy is < 1.0, the object sinks
when buoyancy equals 1.0 it floats
when buoyancy is > 1.0 the object rises'
signature: "void llSetBuoyancy(float buoyancy)"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llSetBuoyancy'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llsetbuoyancy"]
---

Sets the buoyancy of the task or object. Requires physics to be enabled.

A buoyancy value of 0.0 disables the effect
when buoyancy is < 1.0, the object sinks
when buoyancy equals 1.0 it floats
when buoyancy is > 1.0 the object rises


## Signature

```lsl
void llSetBuoyancy(float buoyancy);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `float` | `buoyancy` |  |


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llSetBuoyancy)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llSetBuoyancy) — scraped 2026-03-18_

Sets the buoyancy of the task or object. Requires physics to be enabled.

## Caveats

- Wind can cause the prim to drift. (server 1.38.4 this appears not to be true)
- Unlike some other characteristics, a buoyancy effect is cancelled if the script that set buoyancy is removed from the prim.
- This function cannot be used to set relative levels of buoyancy in parts of a linked object, e.g. to simulate a helium balloon weighted by its string. The most recent call of `llSetBuoyancy` in any child prim appears to set the global buoyancy level for the object.
- This function eats energy to keep the object floating. Large objects may not be able to supply enough energy to keep the object floating.
- For better performance, replace by `llSetPhysicsMaterial(GRAVITY_MULTIPLIER, gravity, 0.0, 0.0, 0.0)` which doesn't consume energy.

For example, replace `llSetBuoyancy(1.5)` by `llSetPhysicsMaterial(GRAVITY_MULTIPLIER, -0.5 ,0.0, 0.0, 0.0)` to raise an object; replace `llSetBuoyancy(1.0)` by `llSetPhysicsMaterial(GRAVITY_MULTIPLIER, 0.0 ,0.0, 0.0, 0.0)` to float an object

- When buoyancy is changed, the object briefly continues to be affected by the last value. For example, if buoyancy was set it to 1.5 to raise an object, and whilst moving, buoyancy is changed it to 0.0, the object continues to rise for a moment, because the force is not reversed, only cancelled. With `llSetPhysicsMaterial(GRAVITY_MULTIPLIER, -0.5 ,0.0, 0.0, 0.0)` followed by `llSetPhysicsMaterial(GRAVITY_MULTIPLIER, 1.0 ,0.0, 0.0, 0.0)`, the change in movement is immediate, and the object starts to fall at the instant that the second call is done.

## Examples

Makes an object float up slowly (e.g. a red balloon)

```lsl
default
{
    state_entry()
    {
        llSetStatus(STATUS_PHYSICS, TRUE);
        llSetBuoyancy(1.05);
    }
}
```

## Notes

Often used to make an object appear to be unaffected by gravity.

<!-- /wiki-source -->
