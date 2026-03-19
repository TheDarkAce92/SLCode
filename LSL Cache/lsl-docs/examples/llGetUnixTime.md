---
name: "llGetUnixTime"
category: "example"
type: "example"
language: "LSL"
description: "Returns an integer that is the number of seconds elapsed since 00:00 hours, Jan 1, 1970  UTC from the system clock."
wiki_url: "https://wiki.secondlife.com/wiki/LlGetUnixTime"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

/LSL


GetUnixTimellGetUnixTime

- 1 Summary
- 2 Caveats
- 3 Examples
- 4 Useful Snippets

  - 4.1 Helper Functions:
- 5 See Also

  - 5.1 Functions
- 6 Deep Notes

  - 6.1 Tests

  - 6.1.1 Signature
  - 6.1.2 Haiku

## Summary

1/2 Bugs Function: integer **llGetUnixTime**( ); 0.0 Forced Delay 10.0 Energy Returns an integer that is the number of seconds elapsed since 00:00 hours, Jan 1, 1970  UTC from the system clock. ## Caveats Time codes before the year 1902 or past the end of 2037 are limited due to the size of LSL's 32-bit integers. As of writing (2024) this is just 14 years away now and any scripts relying on this function may have logical errors. ## Examples ```lsl // Reset tracker integer BOOT_TIME; default { state_entry() { BOOT_TIME = llGetUnixTime(); llSetTimerEvent(0.1); } timer() { llSetText((string)(llGetUnixTime() - BOOT_TIME) + " Seconds since boot.\n\n ", , 1.0); llSetTimerEvent(1); } } ``` ## Useful Snippets ### Helper Functions: •  Unix2StampLst – Converts Unix Time stamp to a list. ex: 1234567890 to [2009, 2, 13, 23, 31, 30] •  Stamp2UnixInt – Converts date to Unix Time stamp. ex: [2009, 2, 13, 23, 31, 30] to 1234567890 •  uuLinuxTime – Converts date to Unix Time stamp (from Linux kernel's sources) •  Unix2WeekdayStr – Gets the weekday from a Unix Time stamp. ex: "Friday" from 1234567890 •  Unix2PST_PDT – Converts Unix Time stamp to an SLT date/time string with PST or PDT indication as appropriate •  Unix2GMTorBST – Converts Unix Time stamp to a UK date/time string with GMT or BST indication as appropriate ## See Also ### Functions •  llGetTimestamp – Human Readable UTC Date and time •  llGetDate – Human Readable UTC Date •  llGetTime – Elapsed script-time. ## Deep Notes ### Tests •  llGetUnixTime Conformance Test #### Signature ```lsl function integer llGetUnixTime(); ``` #### Haiku Ticking time bomb waits, A few years till scripts explode— Y2K, take two! — ChatGPT 4

---

## Subpage: test

**## Purpose Scripts to test the conformance of the llGetUnixTime function.   ## Scripts ## llGetUnixTime test #1 Status**:  draft

## Introduction

First test, copied from [the Second Life KB](http://secondlife.com/knowledgebase/article.php?id=199)

## Script text

```lsl
default
{
    touch_start(integer total_number)
    {
        string time;
        float ft = llGetGMTclock();
        integer ut = llGetUnixTime();
        integer hours = llFloor(ft / 3600);
        integer minutes = llFloor((ft - (hours*3600)) / 60.0);
        time = (string)hours+ ":" + (string)minutes + ":" + (string)(llFloor(ft) % 60);
        llOwnerSay("This object was touched at " + llGetDate() + "  " + time + ".  Unix time = " + (string)ut);
    }
}
```

Authorized Signature:  (none) by (none)

## Instructions

1. Put this script on an object in world
1. Touch the object
1. Copy the number after 'Unix time ='
1. Paste the number into the Timestamp box on [http://www.4webhelp.net/us/timestamp.php](http://www.4webhelp.net/us/timestamp.php)
1. Press 'Convert to a date'
1. Verify the date shown near the top of the web page matches the date and time said by the box
1. Repeat steps 2 -> 6 a few times

## Events Used

- touch_start

## Functions Used

- llGetUnixTime
- llGetGMTclock
- llFloor
- llGetDate
- llOwnerSay

## Notes