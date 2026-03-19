---
name: "llGetTimestamp"
category: "example"
type: "example"
language: "LSL"
description: "Returns a string that is the current date and time in the UTC time zone in the  ISO 8601 format \"YYYY-MM-DDThh:mm:ss.ff..fZ\""
wiki_url: "https://wiki.secondlife.com/wiki/LlGetTimestamp"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

/LSL


GetTimestampllGetTimestamp

- 1 Summary
- 2 Examples
- 3 Useful Snippets

  - 3.1 Helper Functions
- 4 See Also

  - 4.1 Functions
  - 4.2 Articles
- 5 Deep Notes

  - 5.1 Signature
  - 5.2 Haiku

## Summary

 Function: string **llGetTimestamp**(  );

0.0

Forced Delay

10.0

Energy

Returns a string that is the current date and time in the UTC time zone in the  [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format `"YYYY-MM-DDThh:mm:ss.ff..fZ"`

Appears to be accurate to milliseconds.

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

## Useful Snippets

### Helper Functions

- Stamp2UnixInt - List format to Unix timestamp. ex: [2009, 2, 13, 3, 31, 30] to 1234567890

  - compatible with ***llParseString2List( llGetTimestamp(), ["-", "T", ":", "."], [] )***
- Stamp2WeekdayStr - Weekday from (Y, M, D) ex: "Friday" from (2009, 2, 13)
- Millisec - Converts a timestamp string to integer milliseconds accurate to within a month.
- Unix2PST_PDT - Converts a Unix Time stamp to an SLT date/time string with PST or PDT indication as appropriate.
- Unix2GMTorBST - Converts a Unix Time stamp to a UK date/time string with GMT or BST indication as appropriate.

## See Also

### Functions

•

llGetDate

–

Same format but without the time.

•

llGetUnixTime

–

Time in seconds since the epoch.

•

llGetTime

–

Elapsed script-time.

### Articles

•

[ISO 8601](http://www.cl.cam.ac.uk/~mgk25/iso-time.html)

•

 [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601)

•

Code Racer

- useful benchmarks within 100 trials

•

Efficiency Tester

- more accurate benchmarks within 10,000 trials

•

LSL_Script_Efficiency

- in-depth discussion of the Efficiency Tester

## Deep Notes

#### Signature

```lsl
function string llGetTimestamp();
```

#### Haiku

As time ticks away,


Tic-tac, tic-tac, on the clock,


No script ever stops.