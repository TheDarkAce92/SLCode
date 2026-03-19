---
name: "Zero Lag Poseball"
category: "example"
type: "example"
language: "LSL"
description: "This is a script that I made, because I was sick and tired of everyone using the same bloated, laggy poseball scripts that listen on channel 1, to anybody or anything. This is zero lag, no listener, no frills. Drop it and an animation in a prim, and you are good to go!"
wiki_url: "https://wiki.secondlife.com/wiki/Zero_Lag_Poseball"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

This is a script that I made, because I was sick and tired of everyone using the same bloated, laggy poseball scripts that listen on channel 1, to anybody or anything. This is zero lag, no listener, no frills.
Drop it and an animation in a prim, and you are good to go!

```lsl
// Jippen Faddoul's Poseball script - Low ram/lag posepall thats just drag-and drop simple
// Copyright (C) 2007 Jippen Faddoul
//    This program is free software: you can redistribute it and/or modify
//    it under the terms of the GNU General Public License version 3, as
//    published by the Free Software Foundation.
//
//    This program is distributed in the hope that it will be useful,
//    but WITHOUT ANY WARRANTY; without even the implied warranty of
//    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//    GNU General Public License for more details.
//
//   You should have received a copy of the GNU General Public License
//    along with this program.  If not, see

//This text will appear in the floating title above the ball
string TITLE="Sit here";
//You can play with these numbers to adjust how far the person sits from the ball. (  )
vector offset=<0.0,0.0,0.5>;

///////////////////// LEAVE THIS ALONE \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
string ANIMATION;
integer visible = TRUE;
key avatar;

vector COLOR = <1.0,1.0,1.0>;
float ALPHA_ON = 1.0;
float ALPHA_OFF = 0.0;

show(){
    visible = TRUE;
    llSetText(TITLE, COLOR,ALPHA_ON);
    llSetAlpha(ALPHA_ON, ALL_SIDES);
}

hide(){
    visible = FALSE;
    llSetText("", COLOR,ALPHA_ON);
    llSetAlpha(ALPHA_OFF, ALL_SIDES);
}

default{
    state_entry() {
        llSitTarget(offset,ZERO_ROTATION);
        if((ANIMATION = llGetInventoryName(INVENTORY_ANIMATION,0)) == ""){
            llOwnerSay("Error: No animation");
            ANIMATION = "sit";
            }
        llSetSitText(TITLE);
        show();
    }

    touch_start(integer detected) {
        //llOwnerSay("Memory: " + (string)llGetFreeMemory());
        if(visible){ hide(); }
        else       { show(); }
    }

    changed(integer change) {
        if(change & CHANGED_LINK) {
            avatar = llAvatarOnSitTarget();
            if(avatar != NULL_KEY){
                //SOMEONE SAT DOWN
                hide();
                llRequestPermissions(avatar,PERMISSION_TRIGGER_ANIMATION);
                return;
            }else{
                //SOMEONE STOOD UP
                if (llGetPermissionsKey() != NULL_KEY){ llStopAnimation(ANIMATION); }
                show();
                return;
            }
        }
        if(change & CHANGED_INVENTORY) { llResetScript(); }
        if(change & CHANGED_OWNER)     { llResetScript(); }
    }

    run_time_permissions(integer perm) {
        if(perm & PERMISSION_TRIGGER_ANIMATION) {
            llStopAnimation("sit");
            llStartAnimation(ANIMATION);
            hide();
        }
    }
}
```

**Dae´s Version** with the new llSetPrimitiveParams and no script ERROR because crashing or logout Avatars by Sit on it.

```lsl
// Poseball & Furniture script
// by Daemonika Nightfire (2009/2010)
// NO License! that script is free for all.

// why poseball and Furniture?...
// ...just delete all funktions with show/hide and it works for Furniture too.
// llSitTarget(<-0.1,0.1,-0.43>... set the Avatar Position to the prim in meters,
// ...,llEuler2Rot(<00,-90,-90>*DEG_TO_RAD)); set the angle Rotation from the Avatar in 3 axis .

// why no script error at crashing Avatar?...
// ...llKey2Name ask for sitting Avatarname...
// ...is there no name, so nobody there for stop animation and the script will show the Ball only.

string anim;
integer sitting;
show()
{
    llSetPrimitiveParams([PRIM_TEXT,"SIT HERE",<0.9,0.6,0.2>,1.0, PRIM_COLOR, ALL_SIDES,<1,1,1>,1.0]);
}
hide()
{
    llSetPrimitiveParams([PRIM_TEXT,"",ZERO_VECTOR,0.0, PRIM_COLOR, ALL_SIDES,ZERO_VECTOR,0.0]);
}
default
{
    state_entry()
    {
        show();
        sitting = 0;
        anim = llGetInventoryName(INVENTORY_ANIMATION, 0);
        llSitTarget(<-0.1,0.1,-0.43>,llEuler2Rot(<00,-90,-90>*DEG_TO_RAD));
    }
    run_time_permissions(integer perm)
    {
        if (perm & PERMISSION_TRIGGER_ANIMATION)
        {
            sitting = 1;
            llStopAnimation("sit_generic");
            llStopAnimation("sit");
            llStartAnimation(anim);
            hide();
        }
    }
    changed(integer change)
    {
        if (change & CHANGED_LINK)
        {
            key avatar = llAvatarOnSitTarget();
            if (llKey2Name(avatar) != "")
            {
                llRequestPermissions(avatar, PERMISSION_TRIGGER_ANIMATION);
            }
            else
            {
                show();
                if ((llGetPermissions() & PERMISSION_TRIGGER_ANIMATION) && sitting && llKey2Name(avatar) != "")
                {
                    llStopAnimation(anim);
                }
                sitting = 0;
            }
        }
        if (change & CHANGED_OWNER + CHANGED_REGION_START + CHANGED_INVENTORY)
        {
            llResetScript();
        }
    }
    on_rez(integer start_param)
    {
        llResetScript();
    }
}
```