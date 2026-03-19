---
name: "Keyframe Animator"
category: "example"
type: "example"
language: "LSL"
description: "This is a KeyFrame Animator Script to simplify construction of keyframed animations. To get the much better PRO version with after frame editing features and more, contact --Jasper Flossberg"
wiki_url: "https://wiki.secondlife.com/wiki/Key_Frame_Animator"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

This is a KeyFrame Animator Script to simplify construction of keyframed animations. To get the much better PRO version with after frame editing features and more, contact
--Jasper Flossberg

```lsl
integer  channel;
list     keys=[];
vector   last_pos;
rotation last_rot;
vector   start_pos;
rotation start_rot;

default
{
    state_entry()
    {
        llSay(0, "Welcome to the KeyFrame Setter v2.0 by Jasper Flossberg and others\nTouch to start");
        llListen(0, "", llGetOwner(), "");      // Listen on channel 0 for 'set' commands from owner only
        channel = (integer) llFrand(4000000);
        llListen(channel, "", llGetOwner(), "");

        // Must use 'prim equivalency' for KFM
        llSetPrimitiveParams([PRIM_PHYSICS_SHAPE_TYPE, PRIM_PHYSICS_SHAPE_CONVEX]);
        llSetKeyframedMotion([],[]);
        last_pos = start_pos = llGetPos();
        last_rot = start_rot = llGetRot();
    }
    on_rez(integer p)
    {
        llResetScript();
    }
    touch_start(integer total_number)
    {
        if (llDetectedKey(0)  != llGetOwner() )
            return;
        llDialog(llDetectedKey(0), "Please choose option",["Init","Run","Export"],channel);
    }
    listen(integer channel, string name, key id, string message)
    {
        if(message == "Init")
        {
            llSay(0, "Re-Intializing KeyFrame Setter");
            llSleep(1);
            llResetScript();
        }
        if(llToLower(llGetSubString(message,0,2) ) == "set")
        {
            string time = llList2String(llParseString2List(message, [" "], []), 1);
            llSay(0, "Setting new KeyFrame with " + time);
            keys += [llGetPos() - last_pos, llGetRot() / last_rot, (integer) time];
            last_pos = llGetPos();
            last_rot = llGetRot();
        }
        if(message == "Run")
        {
            llSetPrimitiveParams([PRIM_POSITION, start_pos, PRIM_ROTATION, start_rot]);
            llSetKeyframedMotion(keys,[KFM_MODE,KFM_LOOP]);
        }
        if(message == "Export")
        {
            llSay(0, llList2CSV(keys) );
        }
    }
}
```