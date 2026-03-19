---
name: "Linkset Resizer 2"
category: "example"
type: "example"
language: "LSL"
description: "Resizer by Emma Nowhere"
wiki_url: "https://wiki.secondlife.com/wiki/Linkset_Resizer_2"
author: "Emma Nowhere"
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

- 1 About
- 2 Resizer

## About

Resizer by Emma Nowhere

Yet another object resizer script.  Seeing as I was the person who originally opened the JIRA for [LLGetLinkPrimitiveParams](https://jira.secondlife.com/browse/SVC-224)
I thought I should put it to good use.  I like it more than the other resizer scripts out there, but of course, I'm biased.  In any case, it never hurts to have more
code being shared.

How to use with menu:

1. Install this script in the root prim of a linked set of prims (aka "linkset")
1. Type /1resizer to show the menu
1. Hit the appropriate buttons to scale up or down the linkset
1. Hit the "Finish" button to remove the script and finalize prim sizes

Optionally, enter the percentage directly via chat by typing /1resizer x%
where x is the percentage of the original size you want to resize to.

**IMPORTANT:**  You should always make a backup copy of the object before using this script.

The script below is configured to be used as a drop-in script for a user or builder that wants to resize something for themselves.  If putting into a product, you may
want to set START_ON_TOUCH to be TRUE so that your customers can just touch the object to start resizing.  You may also want to set SAY_STATUS to FALSE
so that a bunch of text doesn't get sent to the chat window (only seen by the owner, but can still be annoying to the end-user).

## Resizer

```lsl
///////////////////////////////////////////////////////////////////////////////
// Resizer
// by Emma Nowhere
//
// Last modified: 6/1/2010
//
// How to use with menu:
// 1. Install this script in the root prim of a linked set of prims (aka "linkset")
// 2. Type /1resizer to show the menu
// 3. Hit the appropriate buttons to scale up or down the linkset
// 4. Hit the "Finish" button to remove the script and finalize prim sizes
//
// Optionally, enter the percentage directly via chat by typing /1resizer x%
// where x is the percentage of the original size you want to resize to.
//
// If using in a product with no other scripts, change START_ON_TOUCH below to TRUE
// so user can initiate resizing by just touching the object.

integer START_ON_TOUCH = FALSE;

// Display status messages in chat window (to owner only)

integer SAY_STATUS = TRUE;

// Channel to listen for commands on

integer CHAT_CHANNEL = 1;

// SL constraints

float MIN_SIZE = .01;
float MAX_SIZE = 10;
float MAX_DISTANCE = 10;
float MIN_SCALE = .1;

integer MENU_CHANNEL = -1001;

list backupPrims = [];
integer backupStored = FALSE;

float scale = 1.0;

init_menu_channel() {
    MENU_CHANNEL = ((integer)("0x" + llGetSubString((string)llGetKey(), -8, -1)) & 0x3FFFFFFF) ^ 0xBFFFFFFF;
}

say_status(string msg) {
    if (SAY_STATUS) llOwnerSay(msg);
}

backup() {
    if (!backupStored) {
        say_status("Backing up prim positions and sizes.");
        backupPrims = [];
        integer p = llGetNumberOfPrims();
        integer i = 0;
        vector root_pos = <0, 0, 0>;
        for (i = 1; i <= p; i++)
        {
            list params = llGetLinkPrimitiveParams(i, [PRIM_POSITION, PRIM_SIZE]);
            vector pos = llList2Vector(params, 0);
            vector size = llList2Vector(params, 1);
            if (i == 1)
            {
                root_pos = pos;
            }
            else {
                pos = pos - root_pos;
            }
            backupPrims = backupPrims + pos + size;
        }
        backupStored = TRUE;
        say_status("Prim positions and sizes backed up.");
    }
}

float min(float a, float b) {
    if (a < b) return a;
    return b;
}

float max(float a, float b) {
    if (a > b) return a;
    return b;
}

float constrainMinMax(float value, float min, float max) {
    value = max(value, min);
    value = min(value, max);
    return value;
}

vector constrainSize(vector size) {
    size.x = constrainMinMax(size.x, MIN_SIZE, MAX_SIZE);
    size.y = constrainMinMax(size.y, MIN_SIZE, MAX_SIZE);
    size.z = constrainMinMax(size.z, MIN_SIZE, MAX_SIZE);
    return size;
}

vector constrainDistance(vector delta) {
    delta.x = min(delta.x, MAX_DISTANCE);
    delta.y = min(delta.y, MAX_DISTANCE);
    delta.z = min(delta.z, MAX_DISTANCE);
    return delta;
}

process(integer restore) {
    backup();

    if (restore) {
        say_status("Restoring previously backed up positions and sizes.");
        scale = 1;
    }
    else {
        say_status("Resizing prims to " + (string)llRound(scale * 100) + "% of original size.");
    }

    integer p = llGetNumberOfPrims();
    integer i = 0;
    for (i = 1; i <= p; i++)
    {
        vector pos = llList2Vector(backupPrims, (i - 1) * 2);
        vector size = llList2Vector(backupPrims, ((i - 1) * 2) + 1);

        if (!restore) size = constrainSize(size * scale);

        if (i == 1) {
            llSetLinkPrimitiveParamsFast(i, [PRIM_SIZE, size]);
        }
        else {
            if (!restore) pos = constrainDistance(pos * scale);
            llSetLinkPrimitiveParamsFast(i, [PRIM_POSITION, pos, PRIM_SIZE, size]);
        }
    }

    if (restore) {
        say_status("Previously backed up prim positions and sizes restored.");
    }
    else {
        say_status("Prims resized.");
    }
}

finish() {
    say_status("Deleting Resizer script.");
    llRemoveInventory(llGetScriptName());
}

menu() {
    llDialog(llGetOwner(),
    "Resizer\n\nMake a backup of your object first.\n\nPlease choose an option:\n",
    ["Revert", "-", "Finish", "-1%", "-5%", "-10%", "+1%", "+5%", "+10%"], MENU_CHANNEL);
}

handle_message(integer channel, string name, key id, string message)
{
    if (channel == CHAT_CHANNEL) {
        if (message == "resizer") {
            menu();
        }
        else if (llSubStringIndex(message, "resizer") == 0) {
            list params = llParseString2List(message, [" "], [] );
            if (llGetListLength(params) == 2) {
                string scale_param = llList2String(params, 1);
                if (llGetSubString(scale_param, -1, -1) == "%") {
                    scale = (((float)llGetSubString(scale_param, 0, -2)) / 100);
                    scale = max(scale, MIN_SCALE);
                    process(FALSE);
                }
            }
        }
    }
    else if (channel == MENU_CHANNEL) {
        if (message == "Revert") {
            process(TRUE);
            menu();
        }
        else if (message == "Finish") {
            finish();
        }
        else if (llGetSubString(message, -1, -1) == "%") {
            scale = scale + (((float)llGetSubString(message, 0, -2)) / 100);
            scale = max(scale, MIN_SCALE);
            process(FALSE);
            menu();
        }
    }

}

default
{
    state_entry()
    {
        if (START_ON_TOUCH) {
            // we only want a touch_start handler if we're going to use it
            // so change state rather than just testing inside touch_start
            // for START_ON_TOUCH to be true.
            state start_on_touch;
        }
        else {
            llListen(CHAT_CHANNEL, "", llGetOwner(), "");

            init_menu_channel();
            llListen(MENU_CHANNEL, "", llGetOwner(), "");

            llOwnerSay("Resizer Ready");
            llOwnerSay("Type /" + (string)CHAT_CHANNEL + "resizer for menu.");
        }
    }

    on_rez(integer start_param) {
        llOwnerSay("Resizer Installed");
        llOwnerSay("Type /" + (string)CHAT_CHANNEL + "resizer for menu.");
    }

    listen(integer channel, string name, key id, string message)
    {
        handle_message(channel, name, id, message);
    }
}

state start_on_touch
{
    state_entry()
    {
        llListen(CHAT_CHANNEL, "", llGetOwner(), "");

        init_menu_channel();
        llListen(MENU_CHANNEL, "", llGetOwner(), "");

        llOwnerSay("Resizer Ready");
        llOwnerSay("Touch for resizer menu.");
    }

    on_rez(integer start_param) {
        llOwnerSay("Resizer Installed");
        llOwnerSay("Touch for resizer menu.");
    }

    listen(integer channel, string name, key id, string message)
    {
        handle_message(channel, name, id, message);
    }

    touch_start(integer num_detected)
    {
        menu();
    }

}
```