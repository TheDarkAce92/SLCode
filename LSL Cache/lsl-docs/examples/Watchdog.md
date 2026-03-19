---
name: "Watchdog"
category: "example"
type: "example"
language: "LSL"
description: "These are some simple scripts that watch other scripts in the same prim and restarts them if they crash."
wiki_url: "https://wiki.secondlife.com/wiki/Watchdog"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

## LSL WATCHDOG

These are some simple scripts that watch other scripts in the same prim and restarts them if they crash.

**DESIGN PRINCIPLE**

First and foremost, a watchdog needs to be very robust. Small and simple is better. A watchdog should also do exactly ONLY those things that it needs to do in order to do the job, not one iota more than absolutely necessary. Performance is not a high priority and a watchdog does not need to run at a high rate of speed. Code flow should be linear and easy to follow. For these reasons, these code examples have been written with timed self-resets to help keep the heap space fresh and without timer events or jumps to keep the flow of code clean. No fancy tricks that could lead to potential problems (more parts to break) have been included in these examples.

**USE**

Simply place the desired watchdog script into the prim containing the script(s) to monitor.

**IMPORTANT:** Hopefully it is obvious, but, the watchdog MUST be a separate script from the primary scripts that are being watched!

OPTIONAL: Indeed, for extra assurance, you may wish to place BOTH watchdog scripts into the prim, and have the basic single-script watchdog watch the multiple script watchdog. However, it is very unlikely that you will realistically need to do so. If either watchdog regularly crashes, you have bigger problems than a watchdog can solve. :)

Enjoy. These scripts are released to the community in the public domain as of 2012-01-17. You are free to use them for any purpose including in commercial products. If you break something, you get to keep all the pieces. I only ask that you do not sell these as standalone scripts (they're on the wiki, silly). If you have improvements that you wish to share, please add it as another script on this page. --Tika Oberueng

**BASIC LSL WATCHDOG FOR A SINGLE PRIMARY SCRIPT**

```lsl
// Basic LSL Watchdog Script to watch a single script
// 2012-01-17 By Tika Oberueng
// Released to the public domain.
// You break it, you get to keep both pieces.
//
string watchee = "Test";    // Set this to the name of a script in prim inventory to watch
float interval = 60.0; // Number of seconds between watchdog ticks. Probably best to keep this above >= 10. First check happens at 1/2 this interval.

default {
    state_entry() {
        llSleep(interval/2); // Sleep for 1/2 of the interval. Just to make sure everything has enough time to start up on rez or reset.
        if (llGetInventoryType(watchee) == INVENTORY_SCRIPT) { // Make sure the script exists first!
            if (!llGetScriptState(watchee)) { // if the watched script is not running
                llResetOtherScript(watchee); // reset it first to clear the error and let the next command actually work.
                llSetScriptState(watchee, TRUE); // then set it running again
                llRegionSay(DEBUG_CHANNEL, "Watchdog Trip: The script ["+watchee+"] has crashed and has been restarted."); // scream!
            } // end if
        } // end if
        llSleep(interval/2); // Now sleep for the second half of the interval. Again, to make sure things are stable.
        llResetScript(); // Reset this script and start all over again
    } // end state_entry
    on_rez(integer param) {
        llResetScript(); // Reset this script on rez just to be paranoid
    } // end on_rez
} // end state
```

**BASIC LSL WATCHDOG FOR MULTIPLE SCRIPTS**

```lsl
// Basic LSL Watchdog Script to watch multiple scripts
// 2012-01-17 By Tika Oberueng
// Released to the public domain.
// You break it, you get to keep both pieces.
//
float interval = 60.0; // Number of seconds between watchdog ticks. Probably best to keep this above >= 10. First check happens at 1/2 this interval.

default {
    state_entry() {
        integer loop; // loop variable
        string watchee; // name of script in inventory
        llSleep(interval/2); // Sleep for 1/2 of the interval. Just to make sure everything has enough time to start up on rez or reset.
        for (loop = llGetInventoryNumber(INVENTORY_SCRIPT) -1; loop > -1; --loop) { // loop through each script in inventory
            watchee = llGetInventoryName(INVENTORY_SCRIPT,loop); // get the name of the script
            if (llGetInventoryType(watchee) == INVENTORY_SCRIPT) { // Make sure the script exists first!
                if (!llGetScriptState(watchee)) { // if the watched script is not running
                    if (watchee != llGetScriptName()) { // and is not this script
                        llResetOtherScript(watchee); // reset it first to clear the error and let the next command actually work.
                        llSetScriptState(watchee, TRUE); // then set it running
                        llRegionSay(DEBUG_CHANNEL, "Multiple Watchdog Trip: The script ["+watchee+"] has crashed and has been restarted."); // scream!
                    } // end if
                } // end if
            } // end if
        } // end loop
        llSleep(interval/2); // Now sleep for the second half of the interval. Again, to make sure things are stable.
        llResetScript(); // Reset this script and start all over again
    } // end state_entry
    on_rez(integer param) {
        llResetScript(); // Reset this script on rez just to be paranoid
    } // end on_rez
} // end state
```