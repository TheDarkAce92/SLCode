---
name: "RLV Viewer Titler"
category: "example"
type: "example"
language: "LSL"
description: "With upcoming new third party viewer policy, displaying of viewer tags is no more allowed and was also deactivated. Before the TPV changes, with some viewers it was possible to see what viewer other residents are using, which is seen as injuring of privacy on the other side, but on the other side an improvement in giving viewer-dependant residental support. This advantage of viewer tags is taken by the TPV changes."
wiki_url: "https://wiki.secondlife.com/wiki/RLV_Viewer_Titler"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

With upcoming new third party viewer policy, displaying of viewer tags is no more allowed and was also deactivated. Before the TPV changes, with some viewers it was possible to see what viewer other residents are using, which is seen as injuring of privacy on the other side, but on the other side an improvement in giving viewer-dependant residental support. This advantage of viewer tags is taken by the TPV changes.

The Viewer Titler tries to help here. It works with RLV technology and requests the viewer version by using its RLV interface. After viewer response, the type and version of the viewer is shown as hover text.

The comment block inside the script provides further info about features and usage of the script.

```lsl
//----------------------------------------------------------------------------
// This program is free software; you can redistribute it and/or
// modify it under the terms of the GNU General Public License as
// published by the Free Software Foundation; either version 3 of
// the License, or (at your option) any later version.
//
// You may ONLY redistribute this program with copy, mod and transfer
// permissions and ONLY if this preamble is not removed.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program; if not, see .
//----------------------------------------------------------------------------
//----------------------------------------------------------------------------
//
// Script: RLVVersionTitler
//
// Features
//
//   1. Displays the viewr version and additional message as hover text.
//   2. Requests Viewer and version by using it's RLV interface.
//      This works only by using on a RLV-capable viewer.
//   3. Hides, shows the title and allows setting a color.
//   4. Freezing reduces lag by releasing listeners.
//
// RLV API (version checking part)
//
//   http://wiki.secondlife.com/wiki/LSL_Protocol/RestrainedLifeAPI
//
// Usage
//
//   1. Rezz a prim (any shape and size) and rename it nicelly.
//   2. Put the script inside, the prim turns invisible.
//   3. Pick up the prim (highlight transparency.)
//   4. To use finally, just wear on HUD or avatar.
//
// User control
//
//   /111 VERSION     - Checks the RLV version (if startup check failed.)
//   /111 HIDE        - Hides the titler.
//   /111 SHOW        - Shows the titler.
//   /111 STOP        - Removes listen. To reactivate, simply reattach.
//   /111 COLOR Name  - Sets titler color. Name is a LSL vector or one of
//                      White, Grey Black, Red, Green, Blue, Yellow, Magenta,
//                      Cyan, Default.
//   /111 Text        - Sets an additional titler text.
//   /111 CLEAR       - Removes the additional text, shows title.
//
// Note
//
// After script modifications and calculation of the memory usage, you may
// comment out the test code - this reduces script spam and script code.
//
//----------------------------------------------------------------------------
// Author  Jenna Felton
// Version 1.0.1
//----------------------------------------------------------------------------

integer CHANNEL = 111;

list NAMES = [
    "WHITE", "GREY", "BLACK",
    "RED", "GREEN", "BLUE",
    "YELLOW", "MAGENTA", "CYAN",
    "DEFAULT"];

list COLORS = [
    <1.0, 1.0, 1.0>, <0.5, 0.5, 0.5>, ZERO_VECTOR,
    <1.0, 0.0, 0.0>, <0.0, 1.0, 0.0>, <0.0, 0.0, 1.0>,
    <1.0, 1.0, 0.0>, <1.0, 0.0, 1.0>, <0.0, 1.0, 1.0>,
    <0.98, 0.69, 0.36>];

integer hUserListen;
integer hRLVCListen;
integer gRLVCChan;

string sViewer = "";
string sTitle = "";
vector vColor = <0.98, 0.69, 0.36>;

key kOwner;

// Added by Kireji Haiku to reduce memory usage and improve readability
reset_listeners_and_timer()
{
    llListenRemove(hRLVCListen);
    gRLVCChan   = 1000000 + (integer)llFrand(100000.0);
    hRLVCListen = llListen(gRLVCChan, "", kOwner, "");

    llOwnerSay("detecting viewer...");
    llOwnerSay("@version=" + (string)gRLVCChan);

    // set timer to go off every other minute
    llSetTimerEvent(60.0);
}

default {
    // init::UsedMem = 12312
    state_entry() {
        // set transparent
        llSetAlpha(.0, ALL_SIDES);

        kOwner  = llGetOwner();
        sViewer = "";
        sTitle  = "";

        hUserListen = llListen(CHANNEL, "", kOwner, "");

        reset_listeners_and_timer();

        // Checks the memory usage and reduces by setting less
        llOwnerSay("init::UsedMem = "+(string)llGetUsedMemory());
        llSetMemoryLimit(24000);
    }

    // onrez::UsedMem = 12410
    on_rez(integer start_param) {
        // Memory test
        llScriptProfiler(PROFILE_SCRIPT_MEMORY);

        if (kOwner != llGetOwner()) llResetScript();

        reset_listeners_and_timer();

        // Memory test
        llScriptProfiler(PROFILE_NONE);
        llOwnerSay("onrez::UsedMem = " + (string)llGetSPMaxMemory());
    }

    // listen::UsedMem = 12378 (rougly min)
    // listen::UsedMem = 13490 (rougly max)
    listen(integer chan, string name, key id, string message) {
        // Memory test
        llScriptProfiler(PROFILE_SCRIPT_MEMORY);

        // User control
        if (chan == CHANNEL) {
            llSetTimerEvent(.0);
            llListenRemove(hRLVCListen);

            name = llToUpper(message);

            if (name == "HIDE") {
                llSetText("", vColor, .0);
            }

            else if (name == "SHOW") {
                llSetText(sViewer+sTitle, vColor, 1.0);
            }

            else if (name == "VERSION") {
                reset_listeners_and_timer();
            }

            else if (name == "STOP") {
                llOwnerSay("/me is frozen. To unfreeze, please reattach");
                llListenRemove(hUserListen);
            }

            else if (llGetSubString(name, 0, 5) == "COLOR ") {
                name = llGetSubString(name, 6, -1);
                name = llStringTrim(name, STRING_TRIM_HEAD);

                // Look for color names. If found - use color value
                chan = llListFindList(NAMES, [name]);
                if (chan > -1) {
                    vColor = llList2Vector(COLORS, chan);
                }

                // Not found - parse the given vector to color value
                else {
                    list tmp = llParseString2List(name, ["<", ",", " ", ">"], []);
                    vColor   = ;
                }

                llSetText(sViewer+sTitle, vColor, 1.0);
            }

            else if (name == "CLEAR") {
                sTitle = "";
                llSetText(sViewer, vColor, 1.0);
            }

            // Unknown command. Fine, the user gets a title.
            else {
                sTitle = message;
                llSetText(sViewer+sTitle, vColor, 1.0);
            }
        }

        // Viewer version response. Example answers:
        // message = "RestrainedLife viewer v1.17 (CV 1.22.11.0)"
        //           "RestrainedLife viewer v1.18 (SL 1.23.4)"
        //           "RestrainedLife viewer v1.22.0 (Emerald Viewer - RLVa 1.0.5)"
        //           "RestrainedLife viewer v1.22.1 (1.22.12.0)
        //           "RestrainedLove viewer v2.2.0 (Phoenix Viewer 1.5.2.908 - RLVa 1.1.3)"
        //           "RestrainedLife viewer v2.7.0 (Firestorm 3.3.0.24880 - RLVa 1.4.3)"
        else if (chan == gRLVCChan) {
            llSetTimerEvent(0.0);
            llListenRemove(hRLVCListen);

            // Separate the name:
            // message = "RLV version (viewer signature)"
            //  -> tmp = ["RLV version", "viewer signature"]
            list tmp = llParseString2List(message, [" (", ")"], []);
            message  = llList2String(tmp, 1);

            // If no viewer name set, "(1.22.12.0)", use RLV version
            name = llGetSubString(message, 0, 0);
            if (name == "" || name == "0" || (integer)name != 0) {
                sViewer = llList2String(tmp, 0) + "\n";
            }
            else {
                sViewer = message + "\n";
            }

            // Use extracted data
            llSetText(sViewer+sTitle, vColor, 1.0);
        }

        // Memory test
        llScriptProfiler(PROFILE_NONE);
        llOwnerSay("listen::UsedMem = " + (string)llGetSPMaxMemory());
    }

    // Viewer Check Timeout
    // timer::UsedMem = 12224
    timer() {
        // Memory test
        llScriptProfiler(PROFILE_SCRIPT_MEMORY);

        llSetTimerEvent(.0);
        llListenRemove(hRLVCListen);

        sViewer = "";
        llSetText(sTitle, vColor, 1.0);

        llOwnerSay(
            "No RLV-capable viewer detected (or RLV is off).\n"+
            "To repeat the ckeck, please reattach or chat this:\n"+
            "/"+(string)CHANNEL+" VERSION");

        // Memory test
        llScriptProfiler(PROFILE_NONE);
        llOwnerSay("timer::UsedMem = " + (string)llGetSPMaxMemory());
    }
}
```