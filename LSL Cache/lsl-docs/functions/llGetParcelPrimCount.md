---
name: "llGetParcelPrimCount"
category: "function"
type: "function"
language: "LSL"
description: "Returns an integer that is the total land impact of objects on the parcel at pos of the given category"
signature: "integer llGetParcelPrimCount(vector pos, integer category, integer sim_wide)"
return_type: "integer"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetParcelPrimCount'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgetparcelprimcount"]
---

Returns an integer that is the total land impact of objects on the parcel at pos of the given category


## Signature

```lsl
integer llGetParcelPrimCount(vector pos, integer category, integer sim_wide);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `vector` | `pos` | position in region coordinates (z component is ignored) |
| `integer` | `category` | a PARCEL_COUNT_* flag |
| `integer (boolean)` | `sim_wide` | boolean, TRUE searches parcels in the region with the same owner as the targeted parcel, FALSE searches only the targeted parcel |


## Return Value

Returns `integer`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetParcelPrimCount)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetParcelPrimCount) — scraped 2026-03-18_

Returns an integer that is the total land impact of objects on the parcel at pos of the given category

## Caveats

- Temp mesh is not included in totals for PARCEL_COUNT_TEMP

## Examples

```lsl
//  gives prim usage information when touched

string primCountThisParcel(integer flag)
{
    vector currentPosition = llGetPos();

    return
        (string)llGetParcelPrimCount(currentPosition, flag, FALSE);
}

default
{
    touch_start(integer total_number)
    {
        llSay(PUBLIC_CHANNEL,
            "The total land impact of objects on this parcel is " + primCountThisParcel(PARCEL_COUNT_TOTAL) + ".");

        llSay(PUBLIC_CHANNEL,
            primCountThisParcel(PARCEL_COUNT_OWNER) + " LI for objects owned by the parcel owner.");

        llSay(PUBLIC_CHANNEL,
            primCountThisParcel(PARCEL_COUNT_GROUP) + " LI for objects set to or owned by the parcel's group.");

        llSay(PUBLIC_CHANNEL,
            primCountThisParcel(PARCEL_COUNT_OTHER) + " LI for objects not set to the parcel group or owned by the parcel owner.");

        llSay(PUBLIC_CHANNEL,
            primCountThisParcel(PARCEL_COUNT_SELECTED) + " LI for selected objects.");

        llSay(PUBLIC_CHANNEL,
            primCountThisParcel(PARCEL_COUNT_TEMP) + " LI for temp-on-rez objects.");
    }
}
```

```lsl
//Sim-wide scanner to count prim use in each parcel
list gPrclID;
integer gTotPrims;
float gX;
float gY;
string gObjName;
integer gNUM;

default
{
    state_entry()
    {
        gObjName = llGetObjectName();
        gPrclID = [];
        gTotPrims = 0;
        // Begin scanning at the SW <0.0,0.0,0.0> corner of the sim
        gX = 4.0;
        gY = 4.0;
    }

    on_rez(integer start)
    {
        llSetPos(llGetPos() + <0.0,0.0,0.5>);
        llSetText("Touch to start scan",<1.0,1.0,0.0>,1.0);
    }

    touch_start(integer total_number)
    {
        llSetText("Scanning ....",<1.0,1.0,0.0>,1.0);
        gNUM = 0;
        llRegionSayTo(llGetOwner(),0,"Scan started on " + llGetRegionName());
        llSetTimerEvent(0.1);
    }

    timer()
    {
        //Grab the parcel's ID and name at position
        list parcel = llGetParcelDetails(,[PARCEL_DETAILS_ID,PARCEL_DETAILS_NAME]);
        key temp = llList2Key(parcel,0);
        string parcel_name = llList2String(parcel,1);
        if (parcel_name == "")
        {
            parcel_name = "(no name)";
        }
        if (!~llListFindList(gPrclID,[temp]))   //Scan at this location if this parcel was not scanned earlier
        {
            ++gNUM;
            llSetObjectName((string)gNUM);
            integer Count = llGetParcelPrimCount(,PARCEL_COUNT_TOTAL,FALSE); //Do not include other parcels owned by llGetOwner()
            gTotPrims += Count;
            llRegionSayTo(llGetOwner(),0, "/me "+ parcel_name + " @ <"+(string)gX+","+(string)gY+",Z>  = " + (string)Count);
            gPrclID += [temp];  //Add this parcel to the "previously scanned" list
        }
        // Increment X and Y in successive scans to look at the entire sim in 8m square blocks
        if (gX < 256.0)
        {
            gX +=8.0;
        }
        if (gX > 256.0)
        {
            gY += 8.0;
            gX = 4.0;
        }
        if (gY > 256.0) // Reached NE corner
        {
            llSetObjectName(gObjName);
            llRegionSayTo(llGetOwner(),0,"Scan finished.  Total land impact = " + (string)gTotPrims + " in " + (string)llGetListLength(gPrclID) + " parcels (not counting temp rez prims).");
            llSetText("Touch to start scan",<1.0,1.0,0.0>,1.0);
            llResetScript();
        }
    }
}
```

## See Also

### Functions

- llGetParcelMaxPrims

### Articles

For a detailed explanation on how the land impact is calculated, see also [Jenni Darkwatch's post](https://community.secondlife.com/forums/topic/83294-prims-prim-equivalent-land-impact-a-too-long-guide/) from late 2011.

<!-- /wiki-source -->
