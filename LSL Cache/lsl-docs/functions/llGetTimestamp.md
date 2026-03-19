---
name: "llGetTimestamp"
category: "function"
type: "function"
language: "LSL"
description: 'Returns a string that is the current date and time in the UTC time zone in the format 'YYYY-MM-DDThh:mm:ss.ff..fZ'

Appears to be accurate to milliseconds.'
signature: "string llGetTimestamp()"
return_type: "string"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetTimestamp'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgettimestamp"]
---

Returns a string that is the current date and time in the UTC time zone in the format "YYYY-MM-DDThh:mm:ss.ff..fZ"

Appears to be accurate to milliseconds.


## Signature

```lsl
string llGetTimestamp();
```


## Return Value

Returns `string`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetTimestamp)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetTimestamp) — scraped 2026-03-18_

Returns a string that is the current date and time in the UTC time zone in the  ISO 8601 format "YYYY-MM-DDThh:mm:ss.ff..fZ"

## Examples

```lsl
// Reset tracker

string BOOT_TIME;

default
{
    state_entry()
    {
        BOOT_TIME = llGetTimestamp(); // state_entry is triggered on script reset.
    }

    touch_start(integer num)
    {
        llSay(PUBLIC_CHANNEL, "The last script was last reset @ " + BOOT_TIME);
        llSay(PUBLIC_CHANNEL, "Right now it is " + llGetTimestamp());
    }
}
```

```lsl
// Greeting

default
{
    state_entry()
    {
        llSetTouchText("Greet");
    }
    touch_start(integer num)
    {
        list TimeStamp = llParseString2List(llGetTimestamp(),["-",":"],["T"]); //Get timestamp and split into parts in a list
        integer Hour = llList2Integer(TimeStamp,4);
        if(Hour<12)
            llSay(PUBLIC_CHANNEL,"Good Morning, Oliver Sintim-Aboagye!");
        else if(Hour<17)
            llSay(PUBLIC_CHANNEL,"Good Afternoon, " + llDetectedName(0));
        else
            llSay(PUBLIC_CHANNEL,"Good Evening, " + llKey2Name(llDetectedKey(0)));
    }
}
```

## See Also

### Functions

- **llGetDate** — Same format but without the time.
- **llGetUnixTime** — Time in seconds since the epoch.
- **llGetTime** — Elapsed script-time.

### Articles

- ISO 8601
- **Code Racer** — - useful benchmarks within 100 trials
- **Efficiency Tester** — - more accurate benchmarks within 10,000 trials
- **LSL_Script_Efficiency** — - in-depth discussion of the Efficiency Tester

<!-- /wiki-source -->
