---
name: "Sim Restart Notifyer"
category: "example"
type: "example"
language: "LSL"
description: "When the region (with object that runs this script) restarts, the script sends all registered residents an instant message telling the sim is online and what channel and version the sim is now. It also displays how many restarts the sim had since the script itself was restarted."
wiki_url: "https://wiki.secondlife.com/wiki/Sim_Restart_Notifyer"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

When the region (with object that runs this script) restarts, the script sends all registered residents an instant message telling the sim is online and what channel and version the sim is now. It also displays how many restarts the sim had since the script itself was restarted.

This is practical when you want to know when you can return to your sim and continue working on your projects. Registered residents do not be online — when IM-to-mail service is activated for their account, they will receive the notification via email.

Usage

Create an object or use any created already as container for the script. Put the script into. In this case you only will receive restart reports. When you want register other residents, or your partner or alts as message recipient (please ask if they want to), create a notecard and fill it with names or keys, one key a line.

For example:

```lsl
# Put the keys of the recipients or the names here.
#
# Using keys is more effective — names need resolving!
# You can combine keys and names by using a comment,
# like this:
#
eb66b7b7-7ddb-4c5a-95ad-bfeb9837ae29 # Jenna Felton
#
# Less effective but also possible:
Jenna Felton
```

Each key and name must go in a different line. You can give the notecard any name. Then put it into the container and reset the script. After it reads the keys and resolves the avatar names, the script is ready.

The script writes as floating text the current sim version and restart counts. By clicking the prim, the script also whispers the restart report without sending it to other recipients (no provoked IM spam).

Notifyer script

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

string  URL = "http://w-hat.com/name2key";

integer gStarts = 0;
string  sSince  = "";

list    lNotify = [];
integer gNotify = 0;

string  sNote;
integer gLine;
key     kRead;

list    lNames  = [];
integer gNames  = 0;

// --- -----------------------------------------------------------------------

notifyRestarts(integer whinfo) {
    string region  = llGetRegionName();
    string channel = llGetEnv("sim_channel");
    string version = llGetEnv("sim_version");

    llSetText(
        (string)gStarts+" restarts since "+sSince
        +"\n----------------"
        +"\nChannel: "+channel
        +"\nVersion: "+version, <1.0, 1.0, 1.0>, 1.0);

    // Second Life RC LeTigre * 12.08.23.263929
    // http://wiki.secondlife.com/wiki/Release_Notes/Second_Life_RC_LeTigre/12#12.08.23.263929

    list   channsl = llParseString2List(channel, [" "], []);
    string srvlink = llDumpList2String(channsl, "_");

    srvlink = "http://wiki.secondlife.com/wiki/Release_Notes/"
        + srvlink + "/" + llGetSubString(version, 0, 1)
        + "#" + version;

    string message = "[RESTART MESSAGE]: Sim "+region
        +" is restarted and back online now."
        +"\nRestarts: "+(string)gStarts+" since "+sSince
        +"\nSimulator: "+channel+", v"+version
        +"\nRelease notes: "+srvlink;

    if (whinfo) llWhisper(0, message);
    else {
        integer pos = gNotify;
        while (pos-- > 0) {
            llInstantMessage((key)llList2String(lNotify, pos), message);
        }
    }
}

// --- -----------------------------------------------------------------------

integer resolveNextName() {
    ++gLine;
    if (gLine >= gNames) return FALSE;

    sNote = llList2String(lNames, gLine);

    // "Jenna Felton" -> "jenna felton"
    // "jenna.felton" -> "jenna felton"
    // "Jenna"        -> "jenna resident"
    integer pos = llSubStringIndex(sNote, ".");
    if (pos > 0) {
        sNote = llGetSubString(sNote, 0, pos-1)+" "+llGetSubString(sNote, pos+1, -1);
    }
    else {
        pos = llSubStringIndex(sNote, " ");
        if (pos < 0) sNote += " Resident";
    }

    llSleep(0.2);

    kRead = llHTTPRequest( URL + "?terse=1&name=" + llEscapeURL(sNote), [], "" );

    return TRUE;
}

// === =======================================================================

default {
    state_entry() {
        llSetText("Reading notification list", <1.0, .0, .0>, 1.0);

        // 1. Resolving the date
        if (sSince == "") {
            // The date is given as "YYY-MM-DD"
            sSince = llGetDate();

            // Date Format conversion
            list tmp = llParseString2List(sSince, ["-"], []);

            // EU format: "DD.MM.YYYY"
            sSince   = llList2String(tmp, 2)+"."+llList2String(tmp, 1)+"."+llList2String(tmp, 0);

            // US format: "MM-DD-YYYY"
            //sSince   = llList2String(tmp, 1)+"-"+llList2String(tmp, 2)+"-"+llList2String(tmp, 0);
        }

        // 2. Starting reading notecard

        sNote = llGetInventoryName(INVENTORY_NOTECARD, 0);
        if (sNote != "") {
            if (llGetInventoryKey(sNote) == NULL_KEY) sNote = "";
        }

        if (sNote == "") {
            llOwnerSay("To allow others to receive restart notifications as well, "
                + "please provide a notecard with stored names or keys "
                + "of the recepients, than reset the script or pick up "
                + "the notificator and rezz it again.");

            state Running;
        }
        else {
            gLine = 0;
            kRead = llGetNotecardLine(sNote, gLine);
        }
    }

    on_rez(integer start_param) {
        llResetScript();
    }

    dataserver(key requested, string data)  {
        if (requested != kRead) return;

        if (data == EOF) {
            if (lNames == []) state Running;
            else              state Resolving;
        }
        else kRead = llGetNotecardLine(sNote, ++gLine);

        integer pos = llSubStringIndex(data, "#");
        if      (pos == 0) data = "";
        else if (pos > 0)  data = llGetSubString(data, 0, pos -1);

        data = llStringTrim(data, STRING_TRIM);

        if (data != "") {
            // The recepient is a valide key?
            if (llStringLength(data) == 36) {
                key agent = (key)data;
                if (agent) {
                    if (llListFindList(lNotify, [agent]) < 0) lNotify += [agent];
                }
                else {
                    llOwnerSay("ERROR ("+sNote+":"+(string)gLine
                        +") String '"+data+"' is no valide key.");
                }
            }

            // Otherwise could be name, save to resolve
            else lNames += [data];
        }
    }
}

// === =======================================================================

state Resolving {
    state_entry() {
        llSetText("Resolving recepient keys", <1.0, 1.0, 0.0>, 1.0);

        gNames = llGetListLength(lNames);
        llOwnerSay("Resolving "+(string)gNames+" keys.");

        gLine = -1;
        if (!resolveNextName()) state Running;
    }

    on_rez(integer start_param) {
        llResetScript();
    }

    http_response(key id, integer status, list meta, string body) {
        if ( id != kRead ) return;

        if ( status == 499 ){
            llOwnerSay("WARNING: name2key request timed out");
        }
        else if ( status != 200 ){
            llOwnerSay("WARNING: the internet exploded!!");
        }
        else if ( (key)body == NULL_KEY ){
            llOwnerSay("WARNING: No key found for " + sNote);
        }

        // Agent found
        else {
            kRead = (key)body;
            llOwnerSay("INFO: Key resolved: " + sNote + " = " + body);
            if (llListFindList(lNotify, [kRead]) < 0) lNotify += [kRead];
        }

        if (!resolveNextName()) state Running;
    }
}

// === =======================================================================

state Running {
    state_entry() {
        llSetText("Sim not restartet yet", <1.0, 1.0, 1.0>, 1.0);

        kRead = llGetOwner();
        if (llListFindList(lNotify, [kRead]) < 0) lNotify += [kRead];

        gNotify = llGetListLength(lNotify);

        llOwnerSay((string)gNotify+" recepients registered.");
    }

    on_rez(integer start_param) {
        llResetScript();
    }

    touch_start(integer total_number) {
        notifyRestarts(TRUE);
    }

    changed(integer change) {
        if (change & CHANGED_REGION_START) {
            ++gStarts;
            notifyRestarts(FALSE);
        }
    }
}

// === =======================================================================
```