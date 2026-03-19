---
name: "Multirezzer"
category: "example"
type: "example"
language: "LSL"
description: "Rezzes (Spawns) up to ten objects upon collision with a user. Each object can be a maximum of 10 meters away from the rez point on any plane."
wiki_url: "https://wiki.secondlife.com/wiki/Multirezzer"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

## Description/Information

Rezzes (Spawns) up to ten objects upon collision with a user. Each object can be a maximum of 10 meters away from the rez point on any plane.

To make the rezzings occur on something other than a collision, change collision_start on line 25 to touch_start or another acceptable command.

## Script

```lsl
vector velocity;
integer shot = FALSE;
integer fade = FALSE;
float alpha = 1.0;

default
{
    state_entry()
    {
        llSetStatus(STATUS_DIE_AT_EDGE, TRUE);
    }

    on_rez(integer start_param)
    {
        llSetStatus(STATUS_DIE_AT_EDGE, TRUE);
        llSetBuoyancy(1.0);
        llCollisionSound("", 1.0);          //  Disable collision sounds
        velocity = llGetVel();
        float vmag;
        vmag = llVecMag(velocity);
        if (vmag > 0.1) shot = TRUE;
        llSetTimerEvent(0.0);
    }

    collision_start(integer num)
    {
        if (llDetectedType(0) & AGENT)
        {
           // llTriggerSound("frozen", 1.0);
            llRezObject(">:) invisible", llDetectedPos(0), ZERO_VECTOR, llGetRot(), 0);
                {
           integer i;
           for ( i=0; i, <0,0,0>, <0,0,0,1>, i );
               llRezObject( "Object", llGetPos()+<-3,-3,2>, <0,0,0>, <0,0,0,1>, i );
               llRezObject( "Object", llGetPos()+<-3,3,2>, <0,0,0>, <0,0,0,1>, i );
               llRezObject( "Object", llGetPos()+<3,-3,2>, <0,0,0>, <0,0,0,1>, i );

               llRezObject( "Object", llGetPos()+<-8,0,2>, <0,0,0>, <0,0,0,1>, i );
               llRezObject( "Object", llGetPos()+<8,0,2>, <0,0,0>, <0,0,0,1>, i );
               llRezObject( "Object", llGetPos()+<0,-8,2>, <0,0,0>, <0,0,0,1>, i );
               llRezObject( "Object", llGetPos()+<0,8,2>, <0,0,0>, <0,0,0,1>, i );

               llRezObject( "Object", llGetPos()+<0,0,9>, <0,0,0>, <0,0,0,1>, i );
               llRezObject( "Object", llGetPos()+<0,0,-9>, <0,0,0>, <0,0,0,1>, i );
               integer i;
           }}
        }
    }

    timer()
    {
        if (!fade)
        {
            if (shot)
            {
                llDie();
            }
        }
        else
        {
            llSetAlpha(alpha, -1);
            alpha = alpha * 0.95;
            if (alpha < 0.1)
            {
                llDie();
            }
        }
    }
}
```