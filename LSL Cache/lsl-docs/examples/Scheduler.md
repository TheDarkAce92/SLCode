---
name: "Scheduler"
category: "example"
type: "example"
language: "LSL"
description: "A lot of scripters (myself included) have a lot of trouble managing multiple events using LSL's single timer capability. For this reason I wrote myself a simple scheduling engine, it's as efficient as I can really make it given LSL's limitations, and unfortunately Mono is unlikely to speed it up significantly."
wiki_url: "https://wiki.secondlife.com/wiki/Scheduler"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

- 1 Scheduler
- 2 Notes
- 3 Global variables and functions
- 4 Timer event
- 5 Example

## Scheduler

A lot of scripters (myself included) have a lot of trouble managing multiple events using LSL's single timer capability. For this reason I wrote myself a simple scheduling engine, it's as efficient as I can really make it given LSL's limitations, and unfortunately Mono is unlikely to speed it up significantly.

When making use of this script template/library you should consider your requirements carefully, as it is not advisable to schedule a lot of rapid events. If however you want to trigger events with around 10 seconds or more between them then you should be just fine using this library.

Please see the example at the bottom of this page on how to use this library.

## Notes

This scheduling system is primarily intended for use in scheduling single unique events. If you wish to repeatedly trigger an event at a set interval then you should still use an ordinary timer event, using another script as required. You can use this script for recurring events if you really want, by having your event schedule itself again. This should only be done if the events are relatively infrequent, as LSL list operations are not particularly efficient.

## Global variables and functions

The following code segment should be entered at the top of your script. You may rename the variables themselves as you see fit, but make sure to rename them in the rest of the script!

```lsl
list events = [];

// PARAMS:
//    id     - the unique, positive id you associate with your event, use of global variables is recommended here.
//    time - the time at which you want the event to try and execute.
//    data - a piece of data you want passed to your handler when the event executes.
scheduleEvent(integer id, integer time, string data) {
    events = llListSort((events = []) + events + [time, id, data], 3, TRUE);
    setTimer(FALSE);
}

// This function sets the timer correctly for the next scheduled event, or de-activates the timer
// if there are no event remaining
integer setTimer(integer executing) {
    if ((events != []) > 0) { // Are there any list items?
        integer time = llList2Integer(events, 0);
        float t = (float)(time - llGetUnixTime());
        if (t <= 0.0) {
            if (executing) return TRUE;
            else t = 0.01;
        }
        llSetTimerEvent(t);
    } else { llSetTimerEvent(0.0); }
    return FALSE;
}

// Place your event handling code in here
handleEvent(integer id, string data) {
    //if (id == 1) {
    //    llOwnerSay(data);
    //    scheduleEvent(2, llGetUnixTime() + 10, "Done");
    //} else if (id == 2) llOwnerSay(data);
}
```

## Timer event

Enter this timer event into your script. It is important that you do not edit it unless you know what you are doing! During normal use you should only have to modify the contents of the handleEvent() function.

```lsl
timer() {
    // Clear timer or it might fire again before we're done
    llSetTimerEvent(0.0);

    do {
        // Fire the event
        handleEvent(llList2Integer(events, 1), llList2String(events, 2));

        // Get rid of the first item as we've executed it
        integer l = events != [];
        if (l > 0) {
            if (l > 3)
                events = llList2List((events = []) + events, 3, -1);
            else events = [];
        }

        // Prepare the timer for the next event
    } while (setTimer(TRUE));
}
```

## Example

This example simply has two events, 10 seconds apart. The first says "Half-way there" and the second says "Done".

```lsl
list events = [];

// PARAMS:
//    id     - the unique, positive id you associate with your event, use of global variables is recommended here.
//    time - the time at which you want the event to try and execute.
//    data - a piece of data you want passed to your handler when the event executes.
scheduleEvent(integer id, integer time, string data) {
    events = llListSort((events = []) + events + [time, id, data], 3, TRUE);
    setTimer(FALSE);
}

// This function sets the timer correctly for the next scheduled event, or de-activates the timer
// if there are no event remaining
integer setTimer(integer executing) {
    if ((events != []) > 0) { // Are there any list items?
        integer time = llList2Integer(events, 0);

        float t = (float)(time - llGetUnixTime());
        if (t <= 0.0) {
            if (executing) return TRUE;
            else t = 0.01;
        }
        llSetTimerEvent(t);
    } else { llSetTimerEvent(0.0); }
    return FALSE;
}

// Place your event handling code in here
handleEvent(integer id, string data) {
    if (id == 1) {
        llOwnerSay(data);
        scheduleEvent(2, llGetUnixTime() + 10, "Done");
    } else if (id == 2) llOwnerSay(data);
}

default {
    state_entry() {
        scheduleEvent(1, llGetUnixTime() + 10, "Half-way there");
    }

    timer() {
        // Clear timer or it might fire again before we're done
        llSetTimerEvent(0.0);

        do {
            // Fire the event
            handleEvent(llList2Integer(events, 1), llList2String(events, 2));

            // Get rid of the first item as we've executed it
            integer l = events != [];
            if (l > 0) {
                if (l > 3)
                    events = llList2List((events = []) + events, 3, -1);
                else events = [];
            }

            // Prepare the timer for the next event
        } while (setTimer(TRUE));
    }
}
```