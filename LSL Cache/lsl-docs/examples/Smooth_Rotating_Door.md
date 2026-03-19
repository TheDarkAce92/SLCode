---
name: "Smooth Rotating Door"
category: "example"
type: "example"
language: "LSL"
description: "Smooth Rotating Door Script"
wiki_url: "https://wiki.secondlife.com/wiki/Smooth_Rotating_Door"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

Smooth Rotating Door Script

## Introduction

Most doors in SL use the same method for opening. They set the door's rotation in one or more steps, resulting in a somewhat choppy motion. This script uses a mixture of llTargetOmega() and llSetLocalRot() to achieve a very smooth, pleasant looking animation for the door. In laggy environments it might be that the script displays a somewhat flaky behavior, but for most cases it will work nicely.

For those unfamiliar with the typical swinging door, you use a box and do a path cut 0.375 / 0.875 to remove one-half of the prim. This will make appear as if it is swinging on its edge and not around it's middle.

```lsl
// Smooth Door Script - Version 1.2.1
// by Toy Wylie
// Distributed under the following licence:
// - You can use it in your own works
// - You can sell it with your work
// - This script must remain full permissions
// - This header notice must remain intact
// - You may modify this script as needed

float openingTime=3.0;      // in seconds
float openingAngle=90.0;    // in degrees
float autocloseTime=15.0;   // in seconds
integer steps=4;            // number of internal rotation steps
integer world=TRUE;         // align to world or root prim rotation

string soundOpen="door_open";
string soundClose="door_close";
string soundClosing="door_closing";

float omega=0.0;

vector axis;
rotation closedRot;
rotation openRot;

integer swinging;
integer open;

sound(string name)
{
    if(llGetInventoryType(name)==INVENTORY_SOUND)
        llTriggerSound(name,1.0);
}

openDoor(integer yes)
{
    if(yes)
        sound(soundOpen);
    else
        sound(soundClosing);

    vector useAxis=axis;
    open=yes;

    if(!yes)
        useAxis=-axis;

    llSetTimerEvent(openingTime/(float) steps);
    llTargetOmega(useAxis,omega,1.0);
}

go()
{
    if(swinging==0)
    {
        if(!open)
        {
            axis=<0.0,0.0,1.0>/llGetRootRotation();

            closedRot=llGetLocalRot();

            if(world)
                openRot=llGetRot()*llEuler2Rot(<0.0,0.0,openingAngle>*DEG_TO_RAD)/llGetRootRotation();
            else
                openRot=closedRot*llEuler2Rot(<0.0,0.0,openingAngle>*DEG_TO_RAD);
        }
        swinging=steps;
        openDoor(!open);
    }
}

rotation slerp(rotation source,rotation target,float amount)
{
   return llAxisAngle2Rot(llRot2Axis(target/=source),amount*llRot2Angle(target))*source;
}

default
{
    state_entry()
    {
        swinging=0;
        open=FALSE;
        omega=TWO_PI/360*openingAngle/openingTime;
        llTargetOmega(ZERO_VECTOR,1.0,1.0);
    }

    touch_start(integer dummy)
    {
        go();
    }

    collision_start(integer dummy)
    {
        go();
    }

    timer()
    {
        if(swinging>0)
        {
            swinging--;
            if(swinging!=0)
            {
                float amount=(float) swinging/(float) steps;
                if(open)
                    amount=1.0-amount;
                llSetLinkPrimitiveParamsFast(LINK_THIS,[PRIM_ROT_LOCAL,slerp(closedRot,openRot,amount)]);
                return;
            }

            llTargetOmega(axis,0.0,0.0);
            if(open)
            {
                llSetLinkPrimitiveParamsFast(LINK_THIS,[PRIM_ROT_LOCAL,openRot]);
                llSetTimerEvent(autocloseTime);
            }
            else
            {
                llSetLinkPrimitiveParamsFast(LINK_THIS,[PRIM_ROT_LOCAL,closedRot]);
                sound(soundClose);
                llSetTimerEvent(0.0);
            }
        }
        else // autoclose time reached
        {
            llSetTimerEvent(0.0);
            openDoor(!open);
            swinging=steps;
        }
    }
}
```

## Changelog

Version 1.2.1:

- Added a sound that plays when the door starts to close

Version 1.2:

- Now always aligns to the global coordinate system or root prim rotation, so you don't need two scripts anymore
- Added graceful sound handling

Version 1.1:

- Added rotation steps so people can start walking through the halfways-open door already
- Added opening on collision