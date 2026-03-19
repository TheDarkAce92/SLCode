---
name: "Dialog NumberPad"
category: "example"
type: "example"
language: "LSL"
description: "// Dialog module which acts as a simple positive integer number pad. // Send a link_message with the following format: // integer num = max number of digits allowed // string msg = \"numpad_open\" //..."
wiki_url: "https://wiki.secondlife.com/wiki/Dialog_NumberPad"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

/LSL

```lsl
// Dialog Number Pad
// DoteDote Edison
// 1-26-2007

// Dialog module which acts as a simple positive integer number pad.
// Send a link_message with the following format:
//    integer num = max number of digits allowed
//    string msg  = "numpad_open"
//    key id      = key of the avatar the dialog should target
// A return link_message will be sent with the following format:
//    integer num = The number entered by the dialog user
//    string msg  = "numpad_close"
//    key id      = key of the avatar who used the dialog

// Things to-do:
// --Add floating point compatability
// --Add negative sign
// --Add undo or cancel button (12-button limit makes this difficult)

float   time_limit     = 15.0; // seconds before dialog times-out
list    numpad_buttons = ["0","00","Done",  "7","8","9",  "4","5","6",  "1","2","3"];

key     numpad_user;
string  numpad_number;
integer numpad_channel;
integer numpad_sender;
integer numpad_limit;

default {
    link_message(integer sender, integer n, string msg, key id) {
        if (msg == "numpad_open" && id != NULL_KEY) {
            numpad_sender = sender;
            numpad_limit = n;
            numpad_user = id;
            state numberPad;
        }
    }
}

state numberPad {
    state_entry() {
        numpad_number = "";
        numpad_channel = llCeil(llFrand(9999));
        llListen(numpad_channel, "", numpad_user, "");
        llDialog(numpad_user, "Use buttons to enter a number.", numpad_buttons, numpad_channel);
        llSetTimerEvent(time_limit);
    }
    listen(integer ch, string n, key id, string msg) {
        if (msg == "Done") state default;
        numpad_number += msg;
        integer length = llStringLength(numpad_number);
        if (length < numpad_limit) {
            llSetTimerEvent(time_limit);
            llDialog(numpad_user, "Current number: " + numpad_number, numpad_buttons, numpad_channel);
        }
        else state default;
    }
    timer() {
        llInstantMessage(numpad_user, "Dialog timed-out...");
        state default;
    }
    state_exit() {
        llSetTimerEvent(0.0);
        integer numpad_return = (integer)llGetSubString(numpad_number, 0, numpad_limit - 1);
        llMessageLinked(numpad_sender, numpad_return, "numpad_close", numpad_user);
        numpad_sender = -1;
        numpad_limit = -1;
        numpad_user = NULL_KEY;
    }
}
```