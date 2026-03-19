---
name: "Self Upgrading Script Enhanced"
category: "example"
type: "example"
language: "LSL"
description: "Thanks to Markov Brodsky's Self Upgrading Script and Jippen Faddoul's update to the idea, I was inspired to add to the flexibility and usefulness of their original works."
wiki_url: "https://wiki.secondlife.com/wiki/Self_Upgrading_Script_Enhanced"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

/LSL

Thanks to Markov Brodsky's Self Upgrading Script and Jippen Faddoul's update to the idea, I was inspired to add to the flexibility and usefulness of their original works.

Markov Brodsky's original code is quite good, and I based my own implementation upon it, but it has an admitted flaw: It requires that all the scripts that use it have no spaces within the name. For me this will not do. I like my space ;D

Jippen Faddoul's update is also pretty good, but while it is nicely shortened and optimized, it can't handle being copied into the prim more than 2 times. This makes it unusable for my coding style. (Tweak, save, copy, test, repeat...)

So here's my edition to fix those shortcomings. (You may use this code freely and distribute it freely, but DO NOT even try to SELL it.)

```lsl
// Self Upgrading Script by Cron Stardust based upon work by Markov Brodsky and Jippen Faddoul.
// If this code is used, these header lines MUST be kept.
upgrade() {
    //Get the name of the script
    string self = llGetScriptName();

    string basename = self;

    // If there is a space in the name, find out if it's a copy number and correct the basename.
    if (llSubStringIndex(self, " ") >= 0) {
        // Get the section of the string that would match this RegEx: /[ ][0-9]+$/
        integer start = 2; // If there IS a version tail it will have a minimum of 2 characters.
        string tail = llGetSubString(self, llStringLength(self) - start, -1);
        while (llGetSubString(tail, 0, 0) != " ") {
            start++;
            tail = llGetSubString(self, llStringLength(self) - start, -1);
        }

        // If the tail is a positive, non-zero number then it's a version code to be removed from the basename.
        if ((integer)tail > 0) {
            basename = llGetSubString(self, 0, -llStringLength(tail) - 1);
        }
    }

    // Remove all other like named scripts.
    integer n = llGetInventoryNumber(INVENTORY_SCRIPT);
    while (n-- > 0) {
        string item = llGetInventoryName(INVENTORY_SCRIPT, n);

        // Remove scripts with same name (except myself, of course)
        if (item != self && 0 == llSubStringIndex(item, basename)) {
            llRemoveInventory(item);
        }
    }
}

// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
// * The real start of the universe.
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

default {
    state_entry() {
        upgrade();
    }
}
```

As far as my testing was able to show, I was able to have spaces in my script names and I was even able to tack on a number at the end of my script for personal version tracking and had no troubles. I was able to copy the script into the same prim over and over again with only the latest ever staying.

**Note:** Due to the nature of SL, your script's name will alternate between "scriptname" and "scriptname 1", where "scriptname" is the actual name of your script.