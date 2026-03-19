---
name: "llGetMaxScaleFactor"
category: "function"
type: "function"
language: "LSL"
description: "Returns a float that is the largest scaling factor that can be used with llScaleByFactor to resize the object.  This maximum is determined by the Linkability Rules and prim scale limits."
signature: "float llGetMaxScaleFactor()"
return_type: "float"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetMaxScaleFactor'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgetmaxscalefactor"]
---

Returns a float that is the largest scaling factor that can be used with llScaleByFactor to resize the object.  This maximum is determined by the Linkability Rules and prim scale limits.


## Signature

```lsl
float llGetMaxScaleFactor();
```


## Return Value

Returns `float`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetMaxScaleFactor)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetMaxScaleFactor) — scraped 2026-03-18_

Returns a float that is the largest scaling factor that can be used with llScaleByFactor to resize the object. This maximum is determined by the Linkability Rules and prim scale limits.

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
