---
name: "llGetParcelMaxPrims"
category: "function"
type: "function"
language: "LSL"
description: "Returns an integer that is the maximum combined land impact allowed for objects on the parcel at pos."
signature: "integer llGetParcelMaxPrims(vector pos, integer sim_wide)"
return_type: "integer"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetParcelMaxPrims'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgetparcelmaxprims"]
---

Returns an integer that is the maximum combined land impact allowed for objects on the parcel at pos.


## Signature

```lsl
integer llGetParcelMaxPrims(vector pos, integer sim_wide);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `vector` | `pos` | position in region coordinates (z component is ignored) |
| `integer (boolean)` | `sim_wide` | TRUE treats all parcels owned by this parcel owner in the sim in a single maximum,  FALSE determines the max for the specified parcel |


## Return Value

Returns `integer`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetParcelMaxPrims)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetParcelMaxPrims) — scraped 2026-03-18_

Returns an integer that is the maximum combined land impact allowed for objects on the parcel at pos.

## Caveats

- If there is an Object Bonus for the region, the value returned may be more than the region's total limit.

## Examples

```lsl
default
{
    touch_start(integer total_number)
    {
        llSay(0, "The total land impact of objects rezzed on this parcel is "
             +(string)llGetParcelPrimCount(llGetPos(), PARCEL_COUNT_TOTAL, FALSE) +", of "
             +(string)llGetParcelMaxPrims(llGetPos(), FALSE) + " allowed.");
    }
}
```

## See Also

### Functions

- llGetParcelPrimCount

<!-- /wiki-source -->
