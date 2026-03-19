---
name: "No Auto-Return (Multi)"
category: "example"
type: "example"
language: "LSL"
description: "I was inspired by Bellla Clarity to create this small piece of code by her No Auto-Return script. This one is quite similar, except that it works with multi-prim objects."
wiki_url: "https://wiki.secondlife.com/wiki/No_Auto-Return_(Multi)"
author: "Bellla Clarity"
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

I was inspired by Bellla Clarity to create this small piece of code by her No Auto-Return script. This one is quite similar, except that it works with multi-prim objects.

To use it, simply drop the following bit of code in a script in a multi-prim object and voilà, the object won't go away due to autoreturn.

(Please Note: For each prim in the object it takes one extra second for the script, so if the autoretun is set to 60 seconds, then no more than 55 prims will be saved in an object!)

Please, PLEASE, don't abuse this script.

-Xaviar Czervik



```lsl
default {
    state_entry() {
        llRequestPermissions(llGetOwner(),PERMISSION_CHANGE_LINKS);
    }
    run_time_permissions(integer perm) {
        if (perm & PERMISSION_CHANGE_LINKS)
            llSetTimerEvent(llGetNumberOfPrims()+5);
        else
            llRequestPermissions(llGetOwner(), PERMISSION_CHANGE_LINKS);
    }
    timer() {
        llSetTimerEvent(llGetNumberOfPrims()+5);
        if (llGetNumberOfPrims() == 1)  {
            llBreakAllLinks();
            return;
        }
        list keys;
        integer i = 1;
        while (i <= llGetNumberOfPrims()) {
            keys += llGetLinkKey(i);
            i++;
        }
        llBreakAllLinks();
        i = 0;
        while (i < llGetListLength(keys)) {
            llCreateLink(llList2String(keys, i), 1);
            i++;
        }
    }
}
```