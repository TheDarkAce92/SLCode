---
name: "Script Vitality plug-in"
category: "example"
type: "example"
language: "LSL"
description: "There are so-called dead areas around SL where scripts are not allowed to run. There are always reasons for the land owner to set their land that way but this can brake some devices. This is a work-around the dead areas. The idea is to use vehicle technology: As soon a script takes avatar control (like vehicle do) the script and all other scripts in same prim keep running."
wiki_url: "https://wiki.secondlife.com/wiki/Script_Vitality_plug-in"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

There are so-called dead areas around SL where scripts are not allowed to run. There are always reasons for the land owner to set their land that way but this can brake some devices. This is a work-around the dead areas. The idea is to use vehicle technology: As soon a script takes avatar control (like vehicle do) the script and all other scripts in same prim keep running.

However, this solution increases lag a few, and must be used with care. Use it only for devices that must **really** keep running at any place, and do not use this technology already by themselves.

For lag reasons, only the control of the PageUp key is taken (this key is seldom used) and the control event handler is empty, i.e. no code is executed whenever the key is hit. Also the refreshing timer is set on low rate (15 seconds) which makes the script vulnerable again releasing controls by mistake, but in most cases the script retakes the avatar control in time before entering dead area.

- 1 Disclaimer
- 2 Plugin script
- 3 How to use
- 4 Test script

Disclaimer

You can use this script in your project, if commercial or not. If you modify the script, please extend the script header by your name and update notes.

This script is provided as is. Although tested and found as error-free, no responsibility is taken for any misuse of the script, or damage caused by using it.

Plugin script

```lsl
//----------------------------------------------------------------------------
// Script Vitality - keeps the script itself and all scripts in same prim
// running also in 'dead' areas, those areas where scrpts are not allowed.
// This works simply by taking avatar controls. Should the resident click
// the "Release Controls" button, the vitality feature will break.
//
// To prevent this failure, if releasing controls hapened in an 'alive'
// area, i.e. where scripts are allowed, it retakes the control after 15
// seconds. If that happened in a dead area, there is no option for the
// script to become alive.
//
// Usage: Just put the script in the prim running scripts you want keep
// alive and avoid clicking the "Release Controls" button :) Please also
// keep in mind that this solution increases lag a bit. Every vehicle takes
// controls (it is how they work) and some AOs use also this technology.
// This script is hence not necessary for that devices. Thus, do not simply
// put this script in every scripted device, but check first if the device
// stops working in dead areas, and use this script than.
//
// Dead areas are not for fun no script areas, please respect it too.
//
// This script is universal, You will have to remove parts of the code
// depends on the special script purpose:
//
// * Remove the section [On/Off] (the event link_message) if you want the
//   script to run permanently.
//
// * Remove the section [Owner change] completely if you'l release the
//   device without transfer permission. Otherwise remove one of the
//   event handlers depend on if the owner always changes while the device
//   is not rezzed/worn or not.
//
// More info in the sections.
//
// Author  Jenna Felton
// Version 1.0
//----------------------------------------------------------------------------

key kOwner;

default {
    //--- [Core] -------------------------------------------------------------

    // Core section, basically script functionality.

    state_entry() {
        kOwner = llGetOwner();
        llRequestPermissions(kOwner, PERMISSION_TAKE_CONTROLS);
        llSetTimerEvent(15.0);
    }

    run_time_permissions(integer perm) {
        if(perm & PERMISSION_TAKE_CONTROLS) llTakeControls(CONTROL_DOWN, TRUE, TRUE);
    }

    timer() {
        if(llGetPermissions() & PERMISSION_TAKE_CONTROLS) return;
        llRequestPermissions(kOwner, PERMISSION_TAKE_CONTROLS);
    }

    // This is the magic. Even if empty the event handler makes the script
    // to keep the avatar's control. The script itself does not use it.
    control(key name, integer levels, integer edges) {;}

    //--- [On/Off] -----------------------------------------------------------

    // Allows to toggle the script (the vitality) on and off. You can
    // remove the event handler if you want the script run permanently.
    // If you keep this event, than you can use this code in other
    // script to toggle vitality on and off:
    //
    // llMessageLinked(LINK_SET, -1006192203, "1", ""); // vitality ON
    // llMessageLinked(LINK_SET, -1006192203, "0", ""); // vitality OFF
    //
    link_message(integer sender, integer number, string message, key id) {
        if (number != -1006192203) return; // JFSVC

        if (message == "1") {
            llRequestPermissions(kOwner, PERMISSION_TAKE_CONTROLS);
            llSetTimerEvent(15.0);
        }
        else {
            llReleaseControls();
            llSetTimerEvent(0.0);
        }
    }

    //--- [Owner change] -----------------------------------------------------

    // The changed and on_rez event handlers are used to notice the
    // owner change of the object. If you plan to make the object
    // no transfer, you can even remove both events. Handling the
    // owner change is important to keep control of right avatar.
    // Please use also one of the both handlers, never both. If you
    // are not sure what event handler to use, use the changed and
    // remove on_rez event handler.

    // The changed event is triggered if the object changes the
    // owner, but also if the object changes the shape or the
    // inventory or is simply moved to other sim. Use this event
    // if the device can be transferred to other avatar while it
    // is rezzed inworld, like a furniture or a scripted animal.
    changed(integer what) {
        if (what & CHANGED_OWNER) {
            llReleaseControls();
            llResetScript();
        }
    }

    // on_rez is triggered if the object is worn from inventory
    // or rezzed. Use this event if you build an attachment or
    // another device that is given between avatars or objects
    // but is never given/sold while it is rezzed inworld.
    on_rez(integer start)   {
        if (llGetOwner() != kOwner) {
            llReleaseControls();
            llResetScript();
        }
    }
}
```

How to use

Copy the code in a new script, use a mono script engine (the script takes less than 16kB memory). The script is universal, so you will have to remove parts of the script later in your real projects:

- You not need the *On/Off* section if you want run the script permanently.
- You not need the *Owner change* section if you will not give the device away, otherwise

  - You can remove the *on_rez* event if the device might be sold/given while being inworld,
  - otherwise you can remove the *changed* section.

Test script

The test script also demonstrates how to toggle the vitality plugin on and off. To test the (unchanged) plugin script above, create a wooden box and put this script into:

```lsl
default {
    state_entry() {
        llSetTimerEvent(0.0);
        llSetPrimitiveParams([
            PRIM_SIZE, <.15, .15, .15>,
            PRIM_TEXTURE, ALL_SIDES, "e470eec7-0c82-98b2-ac3c-dee6e2b3b4e7", <1.0, 1.0, .0>, ZERO_VECTOR, .0]);

        state ON;
    }
}

state ON {
    state_entry() {
        llOwnerSay("--- ON ---");
        llSetTimerEvent(10.0);
        llSetColor(<1.0, 1.0, .0>, ALL_SIDES);

        llMessageLinked(LINK_SET, -1006192203, "1", ""); // vitality ON
    }

    timer() {
        llOwnerSay("--- alive ---");
    }

    touch_start(integer number) {
        state OFF;
        }
}

state OFF {
    state_entry() {
        llOwnerSay("--- OFF ---");
        llSetTimerEvent(10.0);
        llSetColor(<.5, .5, .0>, ALL_SIDES);

        llMessageLinked(LINK_SET, -1006192203, "0", ""); // vitality OFF
    }

    timer() {
        llOwnerSay("--- alive ---");
    }

    touch_start(integer number) {
        state ON;
    }
}
```

Pick the box into your inventory and attach it to HUD. The box will say *alive* every 10 seconds and response on touches. Do not use the plugin script yet, but teleport in any dead area. The test script will stop reporting and response on touches, it is dead.

Now teleport back to a place where scripts are allowed to run, click the test box until it says *ON* and put the vitality plugin into the test box. The vitality plugin is running by default, so it is in sync with the test script that is in ON state.

Now teleport back into dead area. The test script continues running. If you click the test box now, the test script sends a deactivating message to the plugin script. The script deactivates and the test script stops running.

To reactivate the plugin script, you have to go back to an alive area and click the test box again. Hence, if you want keep the script toggle-able, do not toggle it off in a no-script area.