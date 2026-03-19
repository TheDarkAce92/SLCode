---
name: "llSetScale"
category: "function"
type: "function"
language: "LSL"
description: 'Sets the size of the prim according to size

The components of size (x, y & z) each need to be in the range [0.01, 64.0], if they are out of the range they are rounded to the nearest endpoint.'
signature: "void llSetScale(vector scale)"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llSetScale'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llsetscale"]
---

Sets the size of the prim according to size

The components of size (x, y & z) each need to be in the range [0.01, 64.0], if they are out of the range they are rounded to the nearest endpoint.


## Signature

```lsl
void llSetScale(vector scale);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `vector` | `size` |  |


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llSetScale)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llSetScale) — scraped 2026-03-18_

Sets the size of the prim according to size

## Caveats

- This function only changes the size of the *prim* that the script is in. **Not** the entire object.
- If the prim is part of a link set, rescaling will fail if the new size is too large or small to satisfy the linkability rules.
- Does not work on physical prims.

## Examples

```lsl
//A basic door that opens and closes when an avatar collides with it.
//Not very effective, as it would be better to use llSetStatus(STATUS_PHANTOM, 1)...
//But, it works.
vector startingSize;
default {
     state_entry() {
          startingSize = llGetScale();
     }
     collision_start(integer i) {
          llSetScale(<0.1, 0.1, 0.1>); //Shrink
          llSetPos(llGetPos() + <0.0,0.0,10.0>); //Hide us
          llSetTimerEvent(3.0);
     }
     timer() {
          llSetTimerEvent(0.0);
          llSetScale(startingSize); //Go back to normal size
          llSetPos(llGetPos() - <0.0,0.0,10.0>); //And where we started
     }
} //Code by Xaviar Czervik.
```

**Curtain/Door script**

For a flexible curtain or door script using llSetScale(), see [[[1]](http://wiki.secondlife.com/wiki/Curtain_script)]

## See Also

### Functions

- **llGetScale** — Gets the prims size
- **llScaleByFactor** — Uniformly rescale a linkset
- **llSetPrimitiveParams** — Sets prims attributes
- **llGetPrimitiveParams** — Gets prims attributes

<!-- /wiki-source -->
