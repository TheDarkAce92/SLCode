---
name: "llScaleByFactor"
category: "function"
type: "function"
language: "LSL"
description: 'Attempts to resize the entire object by scaling_factor, maintaining the size-position ratios of the prims.

Resizing is subject to prim scale limits and linkability limits. This function can not resize the object if the linkset is physical, a pathfinding character, in a keyframed motion, or if resiz'
signature: "integer llScaleByFactor(float scaling_factor)"
return_type: "integer"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llScaleByFactor'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llscalebyfactor"]
---

Attempts to resize the entire object by scaling_factor, maintaining the size-position ratios of the prims.

Resizing is subject to prim scale limits and linkability limits. This function can not resize the object if the linkset is physical, a pathfinding character, in a keyframed motion, or if resizing would cause the parcel to overflow.Returns an integer TRUE if it succeeds, FALSE if it fails.


## Signature

```lsl
integer llScaleByFactor(float scaling_factor);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `float` | `scaling_factor` | The multiplier to be used with the prim sizes and their local positions. |


## Return Value

Returns `integer`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llScaleByFactor)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llScaleByFactor) — scraped 2026-03-18_

Attempts to resize the entire object by scaling_factor, maintaining the size-position ratios of the prims.

## Caveats

- Due to floating point precision issues (often, sqrt(x*x) != x), avoid rescaling by the values returned by llGetMinScaleFactor and llGetMaxScaleFactor.  To guarantee successful rescaling, use values slightly within the limits returned by those functions.

## Examples

```lsl
//  Touching this script causes the object to double or halve in size.

integer growing;

default
{
    state_entry()
    {
        llSay(PUBLIC_CHANNEL, "Touch to toggle scale.");
    }

    touch_start(integer num_detected)
    {
        growing = !growing;

        float min_factor = llGetMinScaleFactor();
        float max_factor = llGetMaxScaleFactor();

        llSay(PUBLIC_CHANNEL, "min_scale_factor = " + (string)min_factor
                            + "\nmax_scale_factor = " + (string)max_factor);

        integer success;

        if (growing) success = llScaleByFactor(2.0);
        else         success = llScaleByFactor(0.5);

        if (!success) llSay(PUBLIC_CHANNEL, "Scaling failed!");
    }
}
```

## See Also

### Functions

- llScaleByFactor
- llGetMaxScaleFactor
- llGetMinScaleFactor

<!-- /wiki-source -->
