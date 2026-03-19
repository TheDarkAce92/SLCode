---
name: "Texture Repeater"
category: "example"
type: "example"
language: "LSL"
description: "Texture Repeater. Observes textures and texture parameters on the prim. As soon those have changed, updates other prims in the linkset to repeat the changes. This allows the user to texture the covered or hard to aim faces of that prims."
wiki_url: "https://wiki.secondlife.com/wiki/Texture_Repeater"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

Texture Repeater. Observes textures and texture parameters on the prim. As soon those have changed, updates other prims in the linkset to repeat the changes. This allows the user to texture the covered or hard to aim faces of that prims.

The script copies the texture UUID and parameters given the face 0 to the face 0 on of every other script in linkset. Than the texture UUID and parameters of the face 1 to the face 1 of other prims and so on until all faces are checked.

The script was created for my [GlassBox mesh tutorial](http://jennassl.blogspot.de/2012/11/mesh-tutorial-glassbox.html) – where we create mesh prims with faces that cover others completely and make them quite hard to texture inworld on regular way. The script was published here in hope it is also usable other wise, but also to keep my [blog post](http://jennassl.blogspot.de/2012/12/texture-repeater-glassbox-tutorial-part.html) shorter.

Usage

Create a box (or other appropriate form) via build tools and put the script into - this turns the prim into repeater tool. Now you can prepare the prim faces by texturing, or just link it with all prims you want bulk-texture. The face textures are copied immediately by linking. If needed you can now texture the repeater prim – all texture parameters are copied to other prims than.

The repeater must not be the root prim of the linket. You can also use two or more repeaters (not recommended), the script copies only changed parameters and avoids so a permanent texture updates by multiple repeaters.

After usage, click the repeater, the script will ask for link permission. If you accept, the repeater will unlink and destroy itself, but leaving back the textured linkset inworld (if you doubt prim loss, please comment out the llDie() command.) If you put something into the repeater prim, like a notecard, texture or another script, the repeater script skips self-destroying to prevent loosing that unexpected content.

Disclaimer

You can use this script in your project, if commercial or not. If you modify the script, please extend the script header by your name and update notes.

This script is provided as is. Although tested and found as error-free, no responsibility is taken for any misuse of the script, or damage caused by using it.

Repeater script

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
// $RCSfile: repeater.lslp,v $
//
// Texture repeater. Observes textures and texture parameters
// on the prim. As soon those have changed, updates other prims
// to repeat the changes. This allows to texture covered or hard
// to aim prim faces.
//
// Version 1.2:
//  + Delay allows a clean deactivating of repeaters with lower priority.
//  + Data buffer allows to change all faces at once which runs faster.
//
// Version 1.1:
//  + Added support for all prim faces, not just 6.
//  + Changing shape resetts script - extending faces is observed.
//  + Pingpong texture updates prevented via inactive state.
//
//----------------------------------------------------------------------------
// Author  Jenna Felton
// Version 1.2, $Revision: 1.10 $
//         $Date: 2013/03/06 15:54:53 $
//----------------------------------------------------------------------------

//----------------------------------------------------------------------------

// Delay before asigning textures, the longer the number the more chance
// for going standby in time.
float   DELAY = .25;

// Inactive state is for the case, more repeaters are linked to same link
// set. Than to prevent the ping-pong texture update, all repeaters except
// one in prim with lowest link numbers change to this state and stop
// observing textures.
// State change is enforced in default state while script reset. Leaving
// this state is possible only due relinking and rezzing the object.
// Update rev.1.7: Used variable instead of state to prevent loosing
//   link messages due state change.
integer inActive = FALSE;

// The lists prevent change of values that are always changed.
// To do so we fill up the lists by dummy values that are never
// something used for texture settings. This way the script will
// notice the difference between the set texture and stored dummy
// value.

list    lImage = []; // e.g. [10, 10, 10, 10, 10, 10] for 6 faces.
list    lFBrgt = [];
list    lColor = [];
list    lBumps = [];
list    lTextg = [];
list    lPGlow = [];

integer gLength;

// Prepares cache to observe every face.
prepareCache() {
    integer face;
    gLength = llGetNumberOfSides();

    for (face = 0 ; face < gLength ; face++) {
        lImage += [10];
        lFBrgt += [10];
        lColor += [10];
        lBumps += [10];
        lTextg += [10];
        lPGlow += [10];
    }
}

//----------------------------------------------------------------------------

updateTextures() {
    // Quit work when not allowed or inposible
    if (inActive)                 return;
    if (llGetNumberOfPrims() < 2) return;

    list    write = [];
    integer face;
    for (face = 0 ; face < gLength ; face++) {
        list    read  = llGetPrimitiveParams([
            PRIM_TEXTURE,    face, // [ s texture, v repeats, v offsets, f rotation ] : 0, 3
            PRIM_FULLBRIGHT, face, // [ i value ]                                     : 4
            PRIM_COLOR,      face, // [ v color, f alpha ]                            : 5, 6
            PRIM_BUMP_SHINY, face, // [ i shiny, i bump ]                             : 7, 8
            PRIM_TEXGEN,     face, // [ i mode ]                                      : 9
            PRIM_GLOW,       face  // [ f intensity ]                                 : 10
        ]);

        // [ PRIM_TEXTURE, i face, s texture, v repeats, v offsets, f rotation ]
        list   tmp   = llList2List(read, 0, 3);
        string image = llDumpList2String(tmp, "|");
        if (llList2String(lImage, face) != image) {
            lImage = llListReplaceList(lImage, [image], face, face);
            write += [PRIM_TEXTURE, face]+tmp;
        }

        // [ PRIM_FULLBRIGHT, i face, i value ]
        integer fbrgt = llList2Integer(read, 4);
        if (llList2Integer(lFBrgt, face) != fbrgt) {
            lFBrgt = llListReplaceList(lFBrgt, [fbrgt], face, face);
            write += [PRIM_FULLBRIGHT, face, fbrgt];
        }

        // [ PRIM_COLOR, i face, v color, f alpha ]
        tmp          = llList2List(read, 5, 6);
        string color = llDumpList2String(tmp, "|");
        if (llList2String(lColor, face) != color) {
            lColor = llListReplaceList(lColor, [color], face, face);
            write += [PRIM_COLOR, face]+tmp;
        }

        // [ PRIM_BUMP_SHINY, i face, i shiny, i bump ]
        tmp          = llList2List(read, 7, 8);
        string bumps = llDumpList2String(tmp, "|");
        if (llList2String(lBumps, face) != bumps) {
            lBumps = llListReplaceList(lBumps, [bumps], face, face);
            write += [PRIM_BUMP_SHINY, face]+tmp;
        }

        // [ PRIM_TEXGEN, i face, i type ]
        integer textg = llList2Integer(read, 9);
        if (llList2Integer(lTextg, face) != textg) {
            lTextg = llListReplaceList(lTextg, [textg], face, face);
            write += [PRIM_TEXGEN, face, textg];
        }

        // [ PRIM_GLOW, i face, f intensity ]
        float pglow = llList2Float(read, 10);
        if (llList2Float(lPGlow, face) != pglow) {
            lPGlow = llListReplaceList(lPGlow, [pglow], face, face);
            write += [PRIM_GLOW, face, pglow];
        }
    }

    // flush texture properties
    if (write != []) {
        llSetLinkPrimitiveParamsFast(LINK_ALL_OTHERS, write);
        write = [];
    }
}

//----------------------------------------------------------------------------

default {
    // Full update: Send all texture settings to other prims,
    // but give first a while to process standby command
    // from eventually linked major repeater.
    state_entry() {
        // 2018031213 = TRCLM
        llMessageLinked(LINK_ALL_OTHERS, -2018031213, "!go", "standby");

        prepareCache();

        llSetTimerEvent(DELAY);
    }

    // Deactivate if standby comand came from a prim with
    // lower link number, so only that one repeater remains
    // active and textures the linkset. Tell also about
    // deactivating so the user can notice the occasional
    // linking of multiple repeaters.
    link_message(integer sender, integer num, string str, key id) {
        if (num != -2018031213) return;
        num = llGetLinkNumber();

        if (sender < num) {
            if (str == "!go" && id == "standby") {
                llOwnerSay("/me goes standby (link "+(string)num+")");
                inActive = TRUE;

                // Stop outstanding updates
                llSetTimerEvent(0.0);
            }
        }
    }

    // Reset script to repeat full texture updates
    on_rez(integer start) {
        llResetScript();
    }

    // Check what is changed, if relinked - full update
    // if just texture change - partial update
    changed(integer change) {
        if (change & CHANGED_LINK) {
            llResetScript();
        }
        if (change & CHANGED_SHAPE) {
            if (!inActive) llResetScript();
        }

        // Before starting update textures, give a moment
        // to receive and process the standby command.
        if (change & CHANGED_COLOR || change & CHANGED_TEXTURE) {
            if (!inActive) llSetTimerEvent(DELAY);
        }
    }

    timer() {
        llSetTimerEvent(0.0);
        updateTextures();
    }

    // Ask the owner if to unlink the repeater,
    // but only if script is active
    touch_start(integer total_number) {
        if (inActive) return;
        if (llDetectedKey(0) == llGetOwner()) {
            llRequestPermissions(llGetOwner(), PERMISSION_CHANGE_LINKS);
        }
    }

    // If allowed, unlink repeater and if possible - destroy
    run_time_permissions(integer perms) {
        if (llGetNumberOfPrims() > 1 && perms & PERMISSION_CHANGE_LINKS) {
            perms = llGetLinkNumber();
            if (perms > 0) {
                llBreakLink(perms);
            }

            if (llGetNumberOfPrims() > 1) {
                llOwnerSay("ERROR: Could not unlink the prim."
                     +" Please try again");
                return;
            }

            if (llGetInventoryNumber(INVENTORY_ALL) == 1) {
                llDie();
            }
            else {
                llOwnerSay("WARNING: There is unexpected content"
                    +" into the prim. Destroying aborted");
            }
        }
    }
}

//----------------------------------------------------------------------------
```