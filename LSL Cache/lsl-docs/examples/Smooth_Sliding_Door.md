---
name: "Smooth Sliding Door"
category: "example"
type: "example"
language: "LSL"
description: "It really annoys me that there are so many bad looking doors out there that jerk around. While you can use llSetPos for a sliding door you have no control at what speed it moves. This sliding door script i created because i wanted to time my sliding door movements with the door sounds i had. It uses llMoveToTarget to move the door, with the door temporally turning phantom as it moves."
wiki_url: "https://wiki.secondlife.com/wiki/Smooth_Sliding_Door"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

- 1 Smooth Sliding Door Script

  - 1.1 Introduction

  - 1.1.1 For a script with fewer problems, see "Alternative Script" at the end of this page.
  - 1.2 The Script
  - 1.3 The Script with Auto-Close
  - 1.4 Alternative Script
  - 1.5 See also

Smooth Sliding Door Script

## Introduction

It really annoys me that there are so many bad looking doors out there that jerk around.  While you can use llSetPos for a sliding door you have no control at what speed it moves.  This sliding door script i created because i wanted to time my sliding door movements with the door sounds i had.  It uses llMoveToTarget to move the door, with the door temporally turning phantom as it moves.

In laggy sims it will behave a little bit funky .. the door sometimes seeming to zoom off to the side before popping into the correct final position as the door becomes a physical object. However, even with that defect it still looks much better IMHO

### For a script with fewer problems, see "Alternative Script" at the end of this page.

## The Script

```lsl
// ********************************************************************
//
// Basic Physical Sliding Door Script
// by SimonT Quinnell
// 11/07/2009
//
// NOTE: If you are going to reposition the door, do it while the door is closed.
//  Otherwise it will try and use the old close position as a reference point.
//
// Licensed under the "OpenCollar License"
// Ie. Licensed under the GPLv2, with the additional requirement that these scripts remain "full perms" in Second Life.
//
// Edit: Simplified the script to be just a basic move script .. removed the sound triggers (5/1/2010)
//
// ********************************************************************

// ********************************************************************
// CONSTANTS
// ********************************************************************

// Movement Constants
vector      OFFSET = <-2.0, 0.0, 0.0>;      // Directional offset for moving the door in x,y,z coordinates
float       OPENTIME = 3.5;                 // Time taken to open door
float       CLOSETIME = 3.5;                // Time taken to close door

// ********************************************************************
// Variables
// ********************************************************************

vector      vPosition;
rotation    rRot;
float       omega=0.0;
vector      vTargetPos;
integer     bOpen = FALSE;
integer     bMoving = FALSE;

// ********************************************************************
// Functions
// ********************************************************************

MoveDoor()
{
    if(!bOpen)
    {   // Initial conditions
        bOpen = TRUE;
        rRot = llGetRot();
        vPosition = llGetPos();

        // Target Position
        omega=OPENTIME/llVecDist(<0,0,0>,OFFSET);
        vTargetPos = vPosition+OFFSET*rRot;

        // Set the timer to cleanup position
        llSetTimerEvent(OPENTIME);
    }else
    {
        bOpen = FALSE;

        // Target Position
        omega=CLOSETIME/llVecDist(<0,0,0>,OFFSET);
        vTargetPos = vPosition;

        // Set the timer to cleanup position
        llSetTimerEvent(CLOSETIME);
    }

    // Set Door Physical and move it
    bMoving = TRUE;
    llSetStatus(STATUS_PHANTOM, TRUE);
    llSetStatus(STATUS_PHYSICS, TRUE);
    llMoveToTarget(vTargetPos,omega);
}

default
{
    state_entry()
    {   // Initial conditions
        rRot = llGetRot();
        vPosition = llGetPos();
    }

    touch_start(integer num_detected)
    {
        MoveDoor();
    }

    timer()
    {
        // Clean up Position
        bMoving = FALSE;
        llSetTimerEvent(0.0);
        llSetStatus(STATUS_PHYSICS, FALSE);
        llSetStatus(STATUS_PHANTOM, FALSE);
        llSetPrimitiveParams([ PRIM_POSITION, vTargetPos, PRIM_ROTATION, rRot ]);
    }
}
```

## The Script with Auto-Close

Flax Quirina: A minor off-spin of the script above would be to add an auto-close feature so that the door slides back after a certain user-defined period of time.

```lsl
// ********************************************************************
//
// Basic Physical Sliding Door Script
// by SimonT Quinnell (11/07/2009) edited by Flax Quirina
// for auto-close (17/06/2011).
//
// NOTE: If you are going to reposition the door, do it while the door is closed.
//  Otherwise it will try and use the old close position as a reference point.
//
// Licensed under the "OpenCollar License"
// Ie. Licensed under the GPLv2, with the additional requirement that these scripts remain "full perms" in Second Life.
//
// Edit: Simplified the script to be just a basic move script .. removed the sound triggers (5/1/2010)
//
// ********************************************************************


// ********************************************************************
// CONSTANTS
// ********************************************************************

// Movement Constants
vector      OFFSET = <-2.0, 0.0, 0.0>;      // Directional offset for moving the door in x,y,z coordinates
float       OPENTIME = 3.5;                 // Time taken to open door
float       CLOSETIME = 3.5;                // Time taken to close door
float       AUTO_CLOSE_TIME = 5;              // Time to auto-close the door

// ********************************************************************
// Variables
// ********************************************************************

vector      vPosition;
rotation    rRot;
float       omega=0.0;
vector      vTargetPos;
integer     bOpen = FALSE;
integer     bMoving = FALSE;
integer     destTarget;

// ********************************************************************
// Functions
// ********************************************************************


MoveDoor()
{
    if(!bOpen)
    {   // Initial conditions
        bOpen = TRUE;
        rRot = llGetRot();
        vPosition = llGetPos();

        // Target Position
        omega=OPENTIME/llVecDist(<0,0,0>,OFFSET);
        vTargetPos = vPosition+OFFSET*rRot;

        // Set the timer to cleanup position
        //llSetTimerEvent(OPENTIME);
    }else
    {
        bOpen = FALSE;

        // Target Position
        omega=CLOSETIME/llVecDist(<0,0,0>,OFFSET);
        vTargetPos = vPosition;

        // Set the timer to cleanup position
        //llSetTimerEvent(CLOSETIME);
    }

    // Set Door Physical and move it
    bMoving = TRUE;
    llSetStatus(STATUS_PHANTOM, TRUE);
    llSetStatus(STATUS_PHYSICS, TRUE);
    destTarget = llTarget(vTargetPos, llVecDist(<0,0,0>,OFFSET));
    llMoveToTarget(vTargetPos,omega);

}


default
{
    state_entry()
    {   // Initial conditions
        rRot = llGetRot();
        vPosition = llGetPos();
    }
    at_target(integer tnum, vector targetpos, vector ourpos) {
        if(llVecDist(targetpos, ourpos) < 0.1) {
            // Clean up Position
            bMoving = FALSE;
            llSetStatus(STATUS_PHYSICS, FALSE);
            llSetStatus(STATUS_PHANTOM, FALSE);
            llSetPrimitiveParams([ PRIM_POSITION, vTargetPos, PRIM_ROTATION, rRot ]);
            llTargetRemove(destTarget);
            if(bOpen) {
                llSetTimerEvent(AUTO_CLOSE_TIME);
            }
        }
    }
    touch_start(integer num_detected)
    {
        MoveDoor();
    }

    timer()
    {
        llSetTimerEvent(0.0);
        MoveDoor();
    }
}
```

## Alternative Script

```lsl
// A go-Physical+Phantom Sliding Door by Omei Qunhua
// with Auto-computation of movement axis and distance
// To avoid problems, the script ignores touches while the door is moving

vector     gHome;                       // Position of the door in its initial closed position
rotation   gRot;                        // The initial rotation of the door prim
vector     gOffset;                     // This will be populated with the move distance stored in the appropriate axis position
integer    AUTO_CLOSE_TIME = 8;         // Can be zero if no auto-close is desired

StartMove(vector Target)
{
    // Set the door PHANTOM and PHYSICAL and start moving it
    llMoveToTarget(Target, 3);             // Do this first, to avoid the door dropping
    llSetStatus(STATUS_PHANTOM, TRUE);
    llSetStatus(STATUS_PHYSICS, TRUE);
    llSetTimerEvent(5);                    // Start a timer. We will end the move after this time.
}
EndMove(vector Target)
{
    // Return the door to non-phantom, non-physical and do a final confirmatory move
    llSetTimerEvent(0);
    llSetStatus(STATUS_PHYSICS, FALSE);
    llSetStatus(STATUS_PHANTOM, FALSE);
    llSetPrimitiveParams([ PRIM_POSITION, Target, PRIM_ROTATION, gRot ]);
}

default
{
    state_entry()
    {
        gRot = llGetRot();
        gHome = llGetPos();
        vector Scale = llGetScale();
        // Find the middle sized dimension of the door prim
        // This determines the axis to move on, and the distance to move
        list lx = llListSort( [Scale.x, <1,0,0>, Scale.y, <0,1,0>, Scale.z, <0,0,1> ], 2, TRUE );
        gOffset = llList2Vector(lx, 3) * llList2Float(lx, 2);  // Apply the distance to move to the appropriate dimension
    }
    touch_end(integer total_number)
    {
        state opening;
    }
}

state opening      // In this state, the door is in process of opening
{
    state_entry()
    {
        StartMove(gHome + gOffset * gRot);
    }
    timer()
    {
        EndMove(gHome + gOffset * gRot);
        state open;
    }
}

state open         // The door is fully open
{
    state_entry()
    {
        llSetTimerEvent(AUTO_CLOSE_TIME);    // Close the door after this time (or not, if value is zero)
    }
    // We will close the door either if it's touched while fully open, or after a time
    touch_end(integer num)
    {
        state closing;
    }
    timer()
    {
        state closing;
    }
}

state closing         // State for when the door is in the process of closing
{
    state_entry()
    {
        StartMove(gHome);
    }
    timer()
    {
        EndMove(gHome);
        state default;
    }
}
```

## See also

- Script Library