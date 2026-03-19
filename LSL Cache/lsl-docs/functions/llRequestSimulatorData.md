---
name: "llRequestSimulatorData"
category: "function"
type: "function"
language: "LSL"
description: 'Requests data about region. When data is available the dataserver event will be raised.

Returns a handle (a key) for a dataserver event response.'
signature: "key llRequestSimulatorData(string simulator, integer data)"
return_type: "key"
sleep_time: "1.0"
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llRequestSimulatorData'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llrequestsimulatordata"]
---

Requests data about region. When data is available the dataserver event will be raised.

Returns a handle (a key) for a dataserver event response.


## Signature

```lsl
key llRequestSimulatorData(string simulator, integer data);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `string` | `region` | Case sensitive region name. |
| `integer` | `data` | DATA_* flag |


## Return Value

Returns `key`.


## Caveats

- Forced delay: **1.0 seconds** — the script sleeps after each call.
- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llRequestSimulatorData)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llRequestSimulatorData) — scraped 2026-03-18_

Requests data about region. When data is available the dataserver event will be raised.Returns a handle (a key) for a dataserver event response.

## Caveats

- This function causes the script to sleep for 1.0 seconds.
- There is no DATA_SIM_MAXPRIMS flag (but `llGetEnv("region_product_name")` returns the region type). SVC-4921

## Examples

Hide objects in PG or unknown regions

```lsl
key         gRateingQuery       =   NULL_KEY        ;

show()
{
    llSetLinkAlpha( LINK_SET, 1.0, ALL_SIDES );
}//show

hide()
{
     llSetLinkAlpha( LINK_SET, 0.0, ALL_SIDES );
}//hide

default
{
    on_rez(integer Setting)
    {
        llResetScript();
    }//on_rez

    state_entry()
    {
        gRateingQuery = llRequestSimulatorData( llGetRegionName(), DATA_SIM_RATING );
    }//state_entry

    changed(integer ItChanged)
    {
        if (ItChanged & CHANGED_OWNER)      llResetScript();
        if (ItChanged & CHANGED_REGION)     llResetScript();
    }//changed

    dataserver(key query_id, string data)
    {
        if (query_id == gRateingQuery)
        {
            if (data == "MATURE" || data == "ADULT")        show();
            else if (data == "UNKNOWN" || data == "PG")     hide();
        }//gRateingQuery
    }//dataserver

}//default
```

## Notes

Global Position in meters

## See Also

### Functions

- llGetEnv
- llGetParcelDetails
- llGetParcelFlags
- llGetParcelMaxPrims
- llGetParcelPrimCount

<!-- /wiki-source -->
