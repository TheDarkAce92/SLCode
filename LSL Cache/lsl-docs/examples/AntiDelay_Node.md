---
name: "AntiDelay Node"
category: "example"
type: "example"
language: "LSL"
description: "Almost every function in Second Life has a delay associated with it. Ranging from 20 seconds to .2 seconds - delays can get on anyones' nerves. Even the most basic scripters know the easy way to get around this is to have a script and use llMessageLinked to tell it to do something. Below is a more a"
source_url: "https://github.com/Outworldz/LSL-Scripts/blob/master/AntiDelay_Node/AntiDelay_Node/Object/AntiDelay_Node_1.lsl"
source_name: "Outworldz LSL Scripts (GitHub) / AntiDelay_Node"
source_owner: "Outworldz"
source_repo: "LSL-Scripts"
source_branch: "master"
source_path: "AntiDelay_Node/AntiDelay_Node/Object/AntiDelay_Node_1.lsl"
source_project: "AntiDelay_Node"
source_part_total: "5"
first_fetched: "2026-03-18"
last_updated: "2026-03-19"
has_versions: "true"
active_version: "scraped-outworldz-lsl-scripts-github-antidelay-node-2026-03-19"
---

```lsl
// === Part 1/5 ===
// :CATEGORY:AntiDelay
// :NAME:AntiDelay_Node
// :AUTHOR:Xaviar Czervik
// :CREATED:2010-01-10 05:20:56.000
// :EDITED:2013-09-18 15:38:47
// :ID:43
// :NUM:57
// :REV:1.0
// :WORLD:Second Life
// :DESCRIPTION:
// Almost every function in Second Life has a delay associated with it. Ranging from 20 seconds to .2 seconds - delays can get on anyones' nerves. Even the most basic scripters know the easy way to get around this is to have a script and use llMessageLinked to tell it to do something. Below is a more advanced version of that code - that allows for one script to handle almost any type of function with a delay.
// 
// How To Use: Use llMessageLinked - the integer is -123, the string is the list of arguments seperated by "~~~", and the key is the name of the function. 
// :CODE:
default {

    touch_start(integer total_number) {

        string s = llGetOwner();

        llMessageLinked(LINK_SET, -123, s + "~~~This is a dialog~~~With, Three, Options~~~0", "dialog");

    }

}

// === Part 2/5 ===
// :CATEGORY:AntiDelay
// :NAME:AntiDelay_Node
// :AUTHOR:Xaviar Czervik
// :CREATED:2010-01-10 05:20:56.000
// :EDITED:2013-09-18 15:38:47
// :ID:43
// :NUM:58
// :REV:1.0
// :WORLD:Second Life
// :DESCRIPTION:
// Example
// :CODE:
default {

    touch_start(integer total_number) {

        vector v =  <128,128,300>;

        integer i = 0;

        float vecDist = llVecDist(llGetPos(), v);

        vecDist /= 5;

        vecDist += 1;

        while (i < vecDist) {

            llMessageLinked(LINK_SET, -123, (string)v, "setpos");

            i++;

        }

    }

}

// === Part 3/5 ===
// :CATEGORY:AntiDelay
// :NAME:AntiDelay_Node
// :AUTHOR:Xaviar Czervik
// :CREATED:2010-01-10 05:20:56.000
// :EDITED:2013-09-18 15:38:47
// :ID:43
// :NUM:59
// :REV:1.0
// :WORLD:Second Life
// :DESCRIPTION:
// And now for the full and complete power of this code *drum roll*. Only 2 scripts are needed for the following code to work. 
// :CODE:
default {

    touch_start(integer total_number) {

        string s = llGetOwner();

        llMessageLinked(LINK_SET, -123, s + "~~~This is a dialog~~~With, Three, Options~~~0", "dialog");

        llMessageLinked(LINK_SET, -123, "youemail@theaddress.com~~~Subj~~~Body", "email");

        llSleep(1);

        llMessageLinked(LINK_SET, -123, s + "~~~This is a dialog~~~With, Three, Options~~~0", "dialog");

        llSleep(1);

        llMessageLinked(LINK_SET, -123, "youemail@theaddress.com~~~Subj~~~Body", "email");

 

    }

}

// === Part 4/5 ===
// :CATEGORY:AntiDelay
// :NAME:AntiDelay_Node
// :AUTHOR:Xaviar Czervik
// :CREATED:2010-01-10 05:20:56.000
// :EDITED:2013-09-18 15:38:47
// :ID:43
// :NUM:60
// :REV:1.0
// :WORLD:Second Life
// :DESCRIPTION:
// The code to make it all work:
// 
// 
// AntiDelay Node Manager: 
// :CODE:
list l = [];

list functions = ["email", "loadurl", "teleportagenthome", "remoteloadscriptpin", "remotedatareply", "giveinventorylist", 

                  "setparcelmusicurl", "instantmessage", "preloadsound", "mapdestination", "dialog", "createlink", "setpos",

                  "setrot", "settexture", "rezobject"];

list delays = [20000, 10000, 5000, 3000, 3000, 2000, 2000, 1000, 1000, 1000, 1000, 1000, 200, 200, 200, 100];

integer count = 1;

integer time() {

    string stamp = llGetTimestamp();

    return (integer) llGetSubString(stamp, 11, 12) * 3600000 +

           (integer) llGetSubString(stamp, 14, 15) * 60000 +

           llRound((float)llGetSubString(stamp, 17, -2) * 1000000.0)/1000;

}

integer nextFreeScript() {

    integer i = 0;

    integer curTime = time();

    while (i < llGetListLength(l)) {

        if (llList2Integer(l, i) - curTime <= 0) {

            return i;

        }

        ++i;

    }

    return -1;

}

 

default {

    state_entry() {

        llMessageLinked(LINK_SET, -112, "", "");

        llSleep(1);

        llMessageLinked(LINK_SET, -111, "", "");

    }

    link_message(integer send, integer i, string s, key k) {

        if (i == -2) {

            llMessageLinked(LINK_SET, (integer)s, (string)count, "");

            ++count;

            l += time();

            llSetTimerEvent(6);

        }

    }

    timer() {

        state run;

    }

}

 

state run {

    state_entry() {

    }

    link_message(integer send, integer i, string s, key k) {

        if (i == -123) {

            llOwnerSay("A");

            integer d = llList2Integer(delays, llListFindList(functions, [(string)k]));

            integer ii = nextFreeScript();

            l = llListReplaceList(l, [time() + d], ii, ii);

            llMessageLinked(LINK_SET, ii+1, s, k);

        }

    }

}

// === Part 5/5 ===
// :CATEGORY:AntiDelay
// :NAME:AntiDelay_Node
// :AUTHOR:Xaviar Czervik
// :CREATED:2010-01-10 05:20:56.000
// :EDITED:2013-09-18 15:38:47
// :ID:43
// :NUM:61
// :REV:1.0
// :WORLD:Second Life
// :DESCRIPTION:
// AntiDelay Node: 
// :CODE:
 

integer myId;

default {

    link_message(integer send, integer i, string s, key k) {

        if (i == myId && myId) {

            myId = (integer)s;

            state run;

        }

        if (i == -111) {

            myId = (integer)llFrand(0x7FFFFFFF);

            llSleep(llFrand(5));

            llMessageLinked(LINK_SET, -2, (string)myId, "");

        }

    }

}

 

state run {

    link_message(integer send, integer i, string s, key k) {

        list params = llParseString2List(s, ["~~~"], []);

        if (i == myId && myId) {

            if (llToLower(k) == "email") {

                llEmail(llList2String(params, 0),

                    llList2String(params, 1),

                    llList2String(params, 2));

            }

            if (llToLower(k) == "loadurl") {

                llLoadURL((key)llList2String(params, 0),

                    llList2String(params, 1),

                    llList2String(params, 2));

            }

            if (llToLower(k) == "teleportagenthome") {

                llTeleportAgentHome((key)llList2String(params, 0));

            }

            if (llToLower(k) == "remoteloadscriptpin") {

                llRemoteLoadScriptPin((key)llList2String(params, 0),

                    llList2String(params, 1),

                    (integer)llList2String(params, 2),

                    (integer)llList2String(params, 3),

                    (integer)llList2String(params, 4));

            }

            if (llToLower(k) == "remotedatareply") {

                llRemoteDataReply((key)llList2String(params, 0),

                    (key)llList2String(params, 1),

                    llList2String(params, 2),

                    (integer)llList2String(params, 3));

            }

            if (llToLower(k) == "giveinventorylist") {

                llGiveInventoryList((key)llList2String(params, 0),

                    llList2String(params, 1),

                    llCSV2List(llList2String(params, 2)));

            }

            if (llToLower(k) == "setparcelmusicurl") {

                llSetParcelMusicURL(llList2String(params, 0));

            }

            if (llToLower(k) == "instantmessage") {

                llInstantMessage((key)llList2String(params, 0),

                    llList2String(params, 1));

            }

            if (llToLower(k) == "preloadsound") {

                llPreloadSound(llList2String(params, 0));

            }

            if (llToLower(k) == "mapdestination") {

                llMapDestination(llList2String(params, 0),

                    (vector)llList2String(params, 1),

                    (vector)llList2String(params, 2));

            }

            if (llToLower(k) == "dialog") {

                llDialog((key)llList2String(params, 0),

                    llList2String(params, 1),

                    llCSV2List(llList2String(params, 2)),

                    (integer)llList2String(params, 3));

            }

            if (llToLower(k) == "createlink") {

                llCreateLink((key)llList2String(params, 0),

                    (integer)llList2String(params, 1));

            }

            if (llToLower(k) == "setpos") {

                llSetPos((vector)llList2String(params, 0));

            }

            if (llToLower(k) == "setrot") {

                llSetRot((rotation)llList2String(params, 0));

            }

            if (llToLower(k) == "settexture") {

                llSetTexture(llList2String(params, 0),

                    (integer)llList2String(params, 1));

            }

            if (llToLower(k) == "rezobject") {

                llRezObject(llList2String(params, 0),

                    (vector)llList2String(params, 1), 

                    (vector)llList2String(params, 2), 

                    (rotation)llList2String(params, 3), 

                    (integer)llList2String(params, 4));

            }

        }

        if (i == -112) {

            llResetScript();

        }

    }

}
```
