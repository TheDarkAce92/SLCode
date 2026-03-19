---
name: "llGetMinScaleFactor"
category: "function"
type: "function"
language: "LSL"
description: "Returns a float that is the smallest scaling factor that can be used with llScaleByFactor to resize the object. This minimum is determined by the prim scale limits."
signature: "float llGetMinScaleFactor()"
return_type: "float"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetMinScaleFactor'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgetminscalefactor"]
---

Returns a float that is the smallest scaling factor that can be used with llScaleByFactor to resize the object. This minimum is determined by the prim scale limits.


## Signature

```lsl
float llGetMinScaleFactor();
```


## Return Value

Returns `float`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetMinScaleFactor)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetMinScaleFactor) — scraped 2026-03-18_

Returns a float that is the smallest scaling factor that can be used with llScaleByFactor to resize the object. This minimum is determined by the prim scale limits.

## Examples

```lsl
default
{
    touch_start(integer total_number)
    {
        float min_factor = llGetMinScaleFactor();
        float max_factor = llGetMaxScaleFactor();
        llSay(0, "Choose a value between " + (string)min_factor + " and " + (string)max_factor
            + " when calling llScaleByFactor() on this linkset.");
    }
}
```

## See Also

### Functions

- llScaleByFactor
- llGetMaxScaleFactor
- llGetMinScaleFactor

<!-- /wiki-source -->
