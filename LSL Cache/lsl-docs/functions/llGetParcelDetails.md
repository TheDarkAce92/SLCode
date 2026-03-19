---
name: "llGetParcelDetails"
category: "function"
type: "function"
language: "LSL"
description: 'Returns a list that is the parcel details specified in params (in the same order) for the parcel at pos.

Both x and y components of pos are clamped to the range [0.0, 256.0] component is ignored.'
signature: "list llGetParcelDetails(vector pos, list params)"
return_type: "list"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetParcelDetails'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgetparceldetails"]
---

Returns a list that is the parcel details specified in params (in the same order) for the parcel at pos.

Both x and y components of pos are clamped to the range [0.0, 256.0] component is ignored.


## Signature

```lsl
list llGetParcelDetails(vector pos, list params);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `vector` | `pos` | only x and y are important and to be given in region coordinates |
| `list` | `params` | a list of PARCEL_DETAILS_* flags. |


## Return Value

Returns `list`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetParcelDetails)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetParcelDetails) — scraped 2026-03-18_

Returns a list that is the parcel details specified in params (in the same order) for the parcel at pos.

## Caveats

- This cannot be used to get the parcel details of parcels in neighboring regions.

## Examples

A very simple example to return the parcel name and description for the current parcel.

```lsl
default
{
    touch_start(integer total_number)
    {
        list details = llGetParcelDetails(llGetPos(), [PARCEL_DETAILS_NAME, PARCEL_DETAILS_DESC]);

        llSay(0, "Local Parcel Name:" + llList2String(details ,0));
        llSay(0, "Local Parcel Desc:" + llList2String(details ,1));
    }
}
```

## See Also

### Functions

- llGetParcelFlags
- llGetRegionFlags
- llGetRegionName
- llRequestSimulatorData
- llGetObjectDetails

<!-- /wiki-source -->
