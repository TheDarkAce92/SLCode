---
name: "llGroundRepel"
category: "function"
type: "function"
language: "LSL"
description: 'Critically damps to height if within height * 0.5 of ground or water level (which ever is higher).

Do not use with vehicles.'
signature: "void llGroundRepel(float height, integer water, float tau)"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGroundRepel'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgroundrepel"]
---

Critically damps to height if within height * 0.5 of ground or water level (which ever is higher).

Do not use with vehicles.


## Signature

```lsl
void llGroundRepel(float height, integer water, float tau);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `float` | `height` | Distance above the ground |
| `integer` | `water` | boolean, if TRUE then hover above water too. |
| `float` | `tau` | seconds to critically damp in |


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGroundRepel)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGroundRepel) — scraped 2026-03-18_

Critically damps to height if within height * 0.5 of ground or water level (which ever is higher).

## Caveats

- Only works in  physics-enabled objects.
- This is not a prim property; stopping or resetting the script stops llGroundRepel; same with the similar llSetHoverHeight
- Crossing a sim border will cancel llGroundRepel, unlike llSetHoverHeight
- A negative height value allows you to hover underwater, same as llSetHoverHeight
- A previous version of this page suggested that llStopHover will stop llGroundRepel, but it does not

## Examples

```lsl
default
{
    state_entry()
    {
        llSetStatus(STATUS_PHYSICS, TRUE);
        llGroundRepel(0.5, TRUE, 0.2); // In a 1/2 meter cube this is roughly the minimum height for any noticeable effect.
        // to
        llGroundRepel(4096.0, TRUE, 0.2); // There is no restrictive maximum.
        // However as the prim reaches 4096 meters (bear in mind the prim height will be (float height + ground height))
        // it will be too high to be allowed to exist.
    }
}// This is actually a remarkably fast way to go straight up!!
```

## See Also

### Functions

- **llSetHoverHeight** — Similar to llGroundRepel, but also pulls down

<!-- /wiki-source -->
