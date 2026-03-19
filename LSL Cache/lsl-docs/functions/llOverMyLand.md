---
name: "llOverMyLand"
category: "function"
type: "function"
language: "LSL"
description: 'Returns an integer boolean, TRUE if id is over land owned by the script owner, FALSE otherwise.

On group deeded land the object containing the script must be deeded to the same group. (It is not enough to set the script to the group.)'
signature: "integer llOverMyLand(key id)"
return_type: "integer"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llOverMyLand'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llovermyland"]
---

Returns an integer boolean, TRUE if id is over land owned by the script owner, FALSE otherwise.

On group deeded land the object containing the script must be deeded to the same group. (It is not enough to set the script to the group.)


## Signature

```lsl
integer llOverMyLand(key id);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `key` | `id` | group, avatar or object UUID that is in the same region |


## Return Value

Returns `integer`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llOverMyLand)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llOverMyLand) — scraped 2026-03-18_

Returns a boolean (an integer) boolean, TRUE if id is over land owned by the script owner, FALSE otherwise.

## Examples

```lsl
//--// private land message //--//

//-- list of people not to pester, lower case only
list gLstIgnore = ["void singer"];
key  gKeyAv;

default{
    state_entry(){
        llOwnerSay( "I'll pester anyone on your land I can find,"
                    + " unless they're in your ignore list." );
        llSensorRepeat( "", "", AGENT, 96, PI, 30 );
    }

    sensor( integer vIntFound ){
        do{
            gKeyAv = llDetectedKey( --vIntFound );  //-- Decrement sensor variable to walk backwards through all detections
             //-- check if they are over our land
            if (llOverMyLand( gKeyAv )){ //-- the return value is automatically tested by the if statemnt
                 //-- check if they are in the ignore list
                if (!~llListFindList( gLstIgnore, (list)llToLower( llDetectedName( vIntFound ) ) )){ //-- '!~llListFindList' == 'not found in the list'
                     //-- pester everyone not in the ignore list !!!
                    llInstantMessage( gKeyAv, "You are on private land, please leave this parcel" );
                }
            }
        }while (vIntFound);
    }
}
```

This following example is a variation of the previous one.  It will email you a daily visitor log.  This is useful to determine how much traffic your parcel is attracting each day, and who is visiting you regularly.  The llOverMyLand function is used to prevented the script from counting people on other parcels.

```lsl
// This script will email you a daily count of new visitors and repeat visitors.
// Visitors are counted once per email update cycle.

// -----------------------------------
// Configuration: customize this script here.
// Change this to your email address.
string MyEmail = "you@example.com";
// This is a number 0 to 96 meters, anything farther away than that will not be noticed.
float SensorRange = 96.0;
// How often to send email updates.
integer UpdateFrequency = 86400; // Number of seconds in 1 day.
// -----------------------------------

// Internal Variables -- Do not change.
list todayVisitors = [];
list allVisitors = [];
list repeatVisitors = [];
list firstTimers = [];
integer newVisitors = 0;
integer returnVisitors = 0;
string ParcelName;

default
{
    state_entry()
    {
        list parcelDetails = llGetParcelDetails(llGetPos(), [PARCEL_DETAILS_NAME]);
        ParcelName = llList2String(parcelDetails, 0);
        llSensorRepeat( "", "", AGENT, SensorRange, PI, 20);
        llSetTimerEvent(UpdateFrequency); // Email me a regular report.
        llOwnerSay("Visitor Log Started.");
    }

    sensor(integer avsFound)
    {
        key  avKey;
        integer avNum;
        for(avNum=0; avNum500)
        {
            allVisitors = llList2List(allVisitors, 0, 499);
        }
        llEmail(MyEmail, subj, body);
    }
}
```

## See Also

### Functions

- llReturnObjectsByID

<!-- /wiki-source -->
