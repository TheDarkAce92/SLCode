---
name: "Smooth Rotating Linked Door With Hinge"
category: "example"
type: "example"
language: "LSL"
description: "As we get more mesh doors that cannot be cut, the need rises for a door script that can rotate the door around another pivot point than the object's center. The script below offers that option, in addition to smoothly rotating, playing sounds and automatically closing."
wiki_url: "https://wiki.secondlife.com/wiki/Smooth_Rotating_Linked_Door_With_Hinge"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

- 1 Introduction
- 2 Hinge
- 3 Linked
- 4 Sounds
- 5 Auto close
- 6 Timers

## Introduction

As we get more mesh doors that cannot be cut, the need rises for a door script that can rotate the door around another pivot point than the object's center. The script below offers that option, in addition to smoothly rotating, playing sounds and automatically closing.

Hinge

Doors have hinges, my script uses a virtual hinge as a pivot point. The location of this hinge is defined by HINGE_POSITION. Usually, this will be half of the door's width and thickness.

Linked

This script works **only** on a door that is linked and **not** the root prim.

Sounds

The script will play a sound when it starts to open and when it finishes closing (if sound UUIDs have been provided).

Auto close

Although doors usually don't close automatically IRL, I added the option to have the door close automatically. If you wish to disable that, simply set AUTO_CLOSE_TIME to 0.0.

Timers

I decided **not** to use an actual timer, in stead I'm using llResetTime and llGetTime to determine at which point of the rotation stage the door is. This ensures a smooth rotation and also ensures the door will open and close in the desired time even if there is more lag (it will automatically move more or less smoothly depending on the time allocated to this script).



```lsl
/*
 * Smooth Rotating Linked Door With Hinge
 *
 * By: Lyn Mimistrobell
 * Version: 1.1
 * License: Do whatever you like with it, just don't blame me if you break it :)
 */

/*
 * Define the rotation in degrees, using the door prim's local coordinate
 * system
 */
vector      ROTATION            = <0.0, 0.0, 80.0>;

/*
 * Define the position of the virtual hinge; usually this is half the door
 * prim's width and thickness
 */
vector      HINGE_POSITION      = <-0.8, 0.05, 0.0>;

/*
 * Define how fast the door opens, in seconds
 */
float       SECONDS_TO_ROTATE   = 1.0;

/*
 * Define after how much time the door should close automatically, in seconds;
 * set to 0.0 to disable autolmatic closing
 */
float       AUTO_CLOSE_TIME     = 10.0;

/*
 * Define a sound that plays when the door starts to open; set to NULL_KEY
 * for no sound.
 */
key         SOUND_ON_OPEN       = "e5e01091-9c1f-4f8c-8486-46d560ff664f";

/*
 * Define a sound that plays when the door has closed; set to NULL_KEY
 * for no sound.
 */
key         SOUND_ON_CLOSE      = "88d13f1f-85a8-49da-99f7-6fa2781b2229";

/*
 * Define the volume of the opening and closing sounds
 */
float       SOUND_VOLUME        = 1.0;

/*
 * NORMALLY, THERE IS NO NEED TO CHANGE ANYTHING BELOW THIS COMMENT. IF YOU DO
 * YOU RISK BREAKING IT.
 */

integer     gClosed;            // Door state: TRUE = closed, FALSE = opened
rotation    gRotationClosed;    // Initial rotation of the door (closed)
vector      gPositionClosed;    // Initial position of the door (closed)
vector      gRotationPerSecond; // The amount to rotate each second

doOpenOrClose() {
    /*
     * Only perform the rotation if the door isn't root or unlinked
     */
    integer linkNumber = llGetLinkNumber();
    if (linkNumber < 2)
        return;

    if (gClosed) {
        /*
         * Store the initial rotation and position so we can return to it.
         *
         * Rotating back purely by calculations can in the longer term cause the door
         * to be positioned incorrectly because of precision errors
         *
         * We determine this everytime before the door is being opened in case it was
         * moved, assuming the door was closed whilst being manipulated.
         */
        gPositionClosed = llGetLocalPos();
        gRotationClosed = llGetLocalRot();

        /*
         * Play the opening sound and preload the closing sound
         */
        if (SOUND_ON_OPEN)
            llPlaySound(SOUND_ON_OPEN, SOUND_VOLUME);
    }

    vector hingePosition = gPositionClosed + HINGE_POSITION * gRotationClosed;

    /*
     * Reset the timer and start moving
     */
    llResetTime();
    while (llGetTime() < SECONDS_TO_ROTATE) {
        float time = llGetTime();
        if (! gClosed)
            /*
             * Invert the timer for closing direction
             */
            time = SECONDS_TO_ROTATE - time;

        rotation rotationThisStep = llEuler2Rot(gRotationPerSecond * time) * gRotationClosed;
        vector positionThisStep = hingePosition - HINGE_POSITION * rotationThisStep;
        llSetLinkPrimitiveParamsFast(linkNumber, [PRIM_ROT_LOCAL, rotationThisStep, PRIM_POS_LOCAL, positionThisStep]);
    }

    /*
     * Set the new state
     */
    gClosed = !gClosed;

    if (gClosed) {
        /*
         * Finalize the closing movement
         */
        llSetLinkPrimitiveParamsFast(linkNumber, [PRIM_ROT_LOCAL, gRotationClosed, PRIM_POS_LOCAL, gPositionClosed]);

        /*
         * Play the closing sound and preload the opening sound
         */
        if (SOUND_ON_CLOSE)
            llPlaySound(SOUND_ON_CLOSE, SOUND_VOLUME);
        if (SOUND_ON_OPEN)
            llPreloadSound(SOUND_ON_OPEN);
    } else {
        /*
         * Finalize the opening movement
         */
        rotation rotationOpened = llEuler2Rot(ROTATION * DEG_TO_RAD) * gRotationClosed;
        vector positionOpened = hingePosition - HINGE_POSITION * rotationOpened;
        llSetLinkPrimitiveParamsFast(linkNumber, [PRIM_ROT_LOCAL, rotationOpened, PRIM_POS_LOCAL, positionOpened]);

        /*
         * Preload the closing sound
         */
        if (SOUND_ON_CLOSE)
            llPreloadSound(SOUND_ON_CLOSE);

        /*
         * Set a timer to automatically close
         */
        llSetTimerEvent(AUTO_CLOSE_TIME);
    }
}

default {
    state_entry() {
        /*
         * Assume the door is closed when the script is reset
         */
        gClosed = TRUE;

        /*
         * These doesn't change unless the script is changed, calculate them once
         */
        gRotationPerSecond = (ROTATION * DEG_TO_RAD / SECONDS_TO_ROTATE);

        /*
         * Preload the opening sound
         */
        if (SOUND_ON_OPEN)
            llPreloadSound(SOUND_ON_OPEN);
    }
    touch_start(integer agentCount) {
        doOpenOrClose();
    }
    timer() {
        llSetTimerEvent(0.0);

        /*
         * Close the door if it isn't already closed
         */
        if (! gClosed)
            doOpenOrClose();
    }
}
```