---
name: "llGetParcelPrimOwners"
category: "function"
type: "function"
language: "LSL"
description: 'Returns a list of all residents and groups who own objects on the parcel at pos and with individual land impact used.

The list is formatted as [ key ownerKey1, integer agentImpact1, key ownerKey2, integer agentImpact2, ... ], and sorted by agent/group key with a maximum of 100 strides.

Requires ow'
signature: "list llGetParcelPrimOwners(vector pos)"
return_type: "list"
sleep_time: "2.0"
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetParcelPrimOwners'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgetparcelprimowners"]
---

Returns a list of all residents and groups who own objects on the parcel at pos and with individual land impact used.

The list is formatted as [ key ownerKey1, integer agentImpact1, key ownerKey2, integer agentImpact2, ... ], and sorted by agent/group key with a maximum of 100 strides.

Requires owner-like permissions for the parcel.


## Signature

```lsl
list llGetParcelPrimOwners(vector pos);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `vector` | `pos` | position in region coordinates |


## Return Value

Returns `list`.


## Caveats

- Forced delay: **2.0 seconds** — the script sleeps after each call.
- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetParcelPrimOwners)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetParcelPrimOwners) — scraped 2026-03-18_

Returns a list of all residents and groups who own objects on the parcel at pos and with individual land impact used. The list is formatted as [ key ownerKey1, integer agentImpact1, key ownerKey2, integer agentImpact2, ... ], and sorted by agent/group key with a maximum of 100 strides.

## Caveats

- This function causes the script to sleep for 2.0 seconds.
- Function WILL NOT work on group owned land if the owner of the object where this function resides is not currently online and connected to the sim (although now seems to be working for land owner on privately owned land even when the owner is not around).

  - These limitation can be overcome by deeding the object to a group the object owner is one of the owners of.
  - Remember to take a copy before deeding because you cannot undeed something.

## Examples

Show a comma separated list of user IDs and their prim counts.
key1, count1, key2, count2 .... etc.

```lsl
default
{
    state_entry()
    {
        list TempList = llGetParcelPrimOwners( llGetPos() );
        llSay(0, llList2CSV(TempList) );
    }
}
```

Use floating text to show prim owner names and counts in count order

```lsl
// Show a floating text list of prim owners on this parcel,
// Sorted by prim count per owner. Highest users first.
// Omei Qunhua

// The object has the same permisions to view prim parcel owners
// as its owner (In About Land >> Objects >> Object Owners )

// Example: If you can't return group object, you won't see group objects
// If you can't return any objects, an empty list will be returned.
// If the prim is deeded to the right group, it should always get a full list

// Note: Only works on group owned land when the object owner is in the Sim
//       Deeded objects always work (group is always online?)

list    gListCountsAndOwners;       // Sorted list count+owner pairs
list    gListNamesAndCounts;        // List of owner names + prim counts
integer gOffset;
integer gIndex;
key     gDataserverID;
integer gListLength;

default
{
    state_entry()
    {
        llSetText("Parcel Prim Owner List\n", <1,1,1>, 1);
        list TempList = llGetParcelPrimOwners( llGetPos() );
        gListLength= llGetListLength(TempList);
        if (!gListLength)
        {
            llSetText("[ERROR]\n Couldn't get Parcel Prim Owners", <1,0,0>, 1);
        }
        else
        {
            // Produce a copy of the list suitable for sorting by count, i.e. count then key
            integer x;
            for ( ; x < gListLength; x += 2)
            {
                gListCountsAndOwners += llList2Integer(TempList, x+1);
                gListCountsAndOwners += llList2String(TempList, x);
            }
            // Sort the list in descending order of prim count
            gListCountsAndOwners = llListSort(gListCountsAndOwners, 2, FALSE);
            // Lookup each owner's name. Start at the beginning of our sorted list
            gDataserverID = llRequestAgentData( llList2String(gListCountsAndOwners, 1), DATA_NAME );
        }
    }

    dataserver( key request_id, string data)
    {
        string TempStr = "Parcel Prim Owner List\n";
        if ( request_id == gDataserverID )
        {
            gListNamesAndCounts += data;
            gListNamesAndCounts += llList2String(gListCountsAndOwners, gIndex);  // process the count as a string

            gIndex += 2;               // bump through the strided list
            if (gIndex < gListLength )
            {
                // lookup name of next owner in our list
                gDataserverID = llRequestAgentData( llList2String(gListCountsAndOwners, gIndex +1) , DATA_NAME );
            }
            integer x;
            for (; x < 16; x+=2)       // show an 8-name subset of the list, starting at 'gOffset'
            {
                // If we run off the end of the list, we just pick up nulls, so no harm done
                TempStr += llList2String(gListNamesAndCounts, gOffset+x) + " : " + llList2String(gListNamesAndCounts, gOffset+x+1) + "\n";
            }
            llSetText(TempStr, <1,1,1>, 1);
            if ( (gListNamesAndCounts != []) > 14)       // If list is longer than 14 (7 owners + counts) ...
            {
                gOffset += 2;   // scroll the list forwards
                llSleep(2);     // at 2 second intervals
            }
        }
    }

    touch_start(integer total_number)
    {
        llResetScript();        // On touch, start the whole process over again
    }
}
```

<!-- /wiki-source -->
