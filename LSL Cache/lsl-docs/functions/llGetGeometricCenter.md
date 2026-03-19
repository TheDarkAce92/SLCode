---
name: "llGetGeometricCenter"
category: "function"
type: "function"
language: "LSL"
description: "Returns the vector that is the geometric center of the object relative to the root prim."
signature: "vector llGetGeometricCenter()"
return_type: "vector"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetGeometricCenter'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgetgeometriccenter"]
---

Returns the vector that is the geometric center of the object relative to the root prim.


## Signature

```lsl
vector llGetGeometricCenter();
```


## Return Value

Returns `vector`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetGeometricCenter)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetGeometricCenter) — scraped 2026-03-18_

Returns the vector that is the geometric center of the object relative to the root prim.

## Caveats

The "geometric center" is different from the "center" in viewer's build tools and also different from what llRezObject considers to be the "center" of a linkset.

## Examples

```lsl
default
{
    touch_start(integer total_number)
    {
        llOwnerSay("Geometric center of the object relative to the root prim: " + (string)llGetGeometricCenter());
    }
}
```

## Notes

- The "geometric center" is the average of all linked prim centers. Mathematically, it's the root-relative positions of all linked prims in the linkset added together and divided by the number of prims in the linkset.

## See Also

### Functions

- llGetCenterOfMass

<!-- /wiki-source -->
