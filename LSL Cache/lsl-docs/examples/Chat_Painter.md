---
name: "Chat Painter"
category: "example"
type: "example"
language: "LSL"
description: "This script allows to change such properties as texture, color, transparency, fullbright, glow and shiny of one special face or all faces ot one special prim or all prims in the linkset. The commands are received via chat and can be sent by the owner themselves (e.g. using an emote) or a device belonging to them, like a HUD. The script for the HUD or the emote are not provided, though."
wiki_url: "https://wiki.secondlife.com/wiki/Chat_Painter"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

This script allows to change such properties as texture, color, transparency, fullbright, glow and shiny of one special face or all faces ot one special prim or all prims in the linkset. The commands are received via chat and can be sent by the owner themselves (e.g. using an emote) or a device belonging to them, like a HUD. The script for the HUD or the emote are not provided, though.

The script supports up to 256 prims linkset, although changing "all prims" at once is not reccomended for large linksets because the changes will not be visible on all prims due capping the updates (I suspect it is an interest list problem and not a problem of this script.)

Can only address prims by name when no space or comma "," character is used in the prim name. When used, can only address the prim by number.

- 1 Usage

  - 1.1 Commands

  - 1.1.1 Control command
  - 1.1.2 Paint command

  - 1.1.2.1 Color value
  - 1.1.3 Examples

  - 1.1.3.1 Given a single prim.
  - 1.1.3.2 Given a linkset with more than one prim.
  - 1.2 Configuration
- 2 Painter Script

Usage

Put the script into the linkset under control. It will scan the linkset for the prim names (build up the dictionary) and then tell it is ready.

To activate the script, touch the linkset at any prim. It will start the listen and tell the command to close the listen.

To reset the script, touch again and hold the mouse button for about 2 seconds (long touch.)

Rezzing the prim resets the script (needs touching again to open the listen.)

Changing the linkset by linking or delinking prims or sitting upon the object resets the script too.

Renaming prims in the linkset will **not** update the dictionary (this remembers the prim names and their numbers) so after renaming any prim a script reset is required, either manually or by taking into invntory and rezzing or by sitting upon the build.

## Commands

The commands are sent on the channel denoted into the script, by default it is 1901.

### Control command

The only special command "close" is used to close the listen:

```lsl
/1901 close
```

This command closes the listen so the script will not respond on the further chat commands until the listen is open by touching the object. When the listen is open this way, the script prints info about this command in chat.

### Paint command

This is a regular command to paint the build. The command shema is

```lsl
/channel prim face commandlist
```

*prim* is name or number of the addressed prim. *Should be omitted when running in a single prim* (no child prims in the linkset.) Special names and possible cases:

- "all" means all prims are addressed in a single command (please avoid for large linksets, 200 prims and more.)
- "set" means the prim running the script, mostly its the root prim.
- Name (e.g. "door_bell") name of the prim to be changed. Must be lower-cased and contain no space " " and comma "," chars.
- Number (e.g. "14") Number of the prim to change. Root prim has the number 1, child prims have higher numbers.

face is the name or number of the face to change. The face names are given into the script and can be changed due configuration. Names and possible cases: - "each" means all faces are changed. - Number (e.g. "2") is the face number. Face numbers go from 0 to 8. - -1 is the number used for "all faces", the same as using "each". - Name (e.g. "top") name of the face, given by the list **FACE_NUMS** in the script configuration. commandlist is the list of commands and values, separated by comma and space chars. The commands and parameters are - "color" hex - value is given by hexadecimal value like "A7B8C9", as known from HTML. You can obtain it from paint programs or the color editor in some viewers (e.g. Firestorm has it.) - "fullb" Y/N/1/0 - "Y" or "1" switch fullbright on, "N" or "0" switch off. - "shiny" 0..3 - "0" means no shiny, "3" means max shiny. - "image" key - Use the key of the image to assign. - "glow" float - The value goes from "0" (no glow) to "1" (max glow), e.g. "0.25". - "alpha" float - The value goes from "0" (opaque) to "1" (transparent.) #### Color value The hexadecimal color values are used in HTML, most if not all paint programs can print them and some viewers may give the value directly. When no such program or viewer is on hand, you can try an online RGB to HTML converter, for example these: HTML Color Picker or RGB Color Codes Chart. Please do not use the char "#" in the value, only the chars 0123456789ABCDEF, otherwise the value will be read wrong. ### Examples #### Given a single prim. The script is installed and the listen is open (the prim is touched.) a) To make the top face red, glowing, fullbright active and see-trough, use this command: ```lsl /1901 top color ff0000, glow .75, fullb Y, alpha 0.5 ``` When the script says "no such face 'top'" than the name "top" is not used as face name in the script configuration. b) This command puts a blank image on each face and sets it medium shiny: ```lsl /1901 each image ae52440b-478e-0af8-a249-e759ab0b744b, shiny 2 ``` c) When we know the number of the face to change, we can use it directly: ```lsl /1901 2 shiny 0 ``` This deactivates shiny on the face with the number 2. #### Given a linkset with more than one prim. The script is installed e.g. into the root prim and the listen is also open. d) This command changes color only on the root prim (all faces) where the script is installed: ```lsl /1901 set each color ff0000 ``` e) This commnd does the same with each prim of the linkset: ```lsl /1901 all each color ff0000 ``` f) When there is a prim with name "Prim-15" into the linkset, this command changes that one: ```lsl /1901 prim-15 each color ff8040 ``` g) Sometimes we want change a prim with given number, e.g. 15, for example when it's name has forbidden characters like "left door": ```lsl /1901 15 each color ff8040 ``` ## Configuration The configuration is done inside the SETTINGS section into the script. There are two variables to configure: CHANNEL

The constant CHANNEL stores the number of the chat channel used to send the commands. By default it is 1901. Any number is possible, but better to avoid using the public channel 0 except for testing purposes: When public channel is used, everything said on this channel will be taken as a command: While you talk to your friend, the sctipt will complain about not known face or prim names or commands.

**FACE_NUMS**

This one needs a bit better explanation. Basically, this list is a fixed face dictionary that stores the face names and their numbers. This list explains what the face names mean. For example you have to tell the script that the face "top" has the number 0 before you can use the face name "top" in the paint commands.

You can assign different face names to the same face number but you may not assign different face numbers to the same face name. When you use the same face name two or more times in the list, probably the first occurance will win (this depends how the LSL processor searches for strings in a list.)

The script below has currently this definition:

```lsl
list    FACE_NUMS  = [
    // these names we can use for the one group of prims
    "top",    0,
    "front",  1,
    "right",  2,
    "back",   3,
    "left",   4,
    "bottom", 5,

    // and these names for the other group of prims
    "alpha",  0,
    "beta",   1,
    "gamma",  2,

    // this is also possible, but for addressing ALL_SIDES
    // we better use the special face name "each" instead
    "omega", -1
    ];
```

Here we explain the script that the names "top", "front", ..., "bottom" will be translated to the numbers 0, 1, ..., 5 while the names "alpha", "beta", "gamma" will be also translated to the numbers 0, 1, 2. The same face number 1 can be addressed by the both names "front" and "beta".

The script will not know what name we use for what prim, every face name can be used for every prim. But we could feel more comfortable when we use one group of defined names for one group of prims and the other group of name definitions for an other group of prims. For example it may feel more convenient when we use the names "top" to "bottom" for cubes and the names "alpha", "beta", "gamma" for cylinders.

The name "omega" is here just for completeness. A number -1 means in LSL 'all faces', so we can have a name for this number, too. But using the special name "each" to address each face of the addressed prim(s) is faster, hence rather reccomemded.

Painter Script

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
// Script: ChatPainter
//
// Allows to change the texture and collor properties of named faces
// of named prims in a linkset by using chat commands.
//
//----------------------------------------------------------------------------
// Version:       1.0.0
// Contributors:  Jenna Felton - initial release
//----------------------------------------------------------------------------

// --- [ SETTINGS ] ----------------------------------------------------------

// Channel for chat commands
integer CHANNEL    = 1901;

// Face names and numbers. Format: Name, number, name, number...
// * Every face name must appear once, i.e. address one number.
// * More than one face name can address same face number.
// * Face names must use lower-case letters.
list    FACE_NUMS  = [
    // these names we can use for the one group of prims
    "top",    0,
    "front",  1,
    "right",  2,
    "back",   3,
    "left",   4,
    "bottom", 5,

    // and these names for the other group of prims
    "alpha",  0,
    "beta",   1,
    "gamma",  2,

    // this is also possible, but for addressing ALL_SIDES
    // we better use the special face name "each" instead
    "omega", -1
    ];

// --- [ SETTINGS END ]  -----------------------------------------------------

key     kOwner     = NULL_KEY;
integer gPrims     = 0;

integer hListen    = 0;

list    lLinks     = [];

// --- -----------------------------------------------------------------------

// updates shiny on given face(s) of given link (only single prim)
// without touching the bump of the faces

changeShiny(integer link, integer face, integer shiny) {
    // result : [ integer shiny, integer bump ] per face.
    list bumps = llGetLinkPrimitiveParams(link, [PRIM_BUMP_SHINY, face]);

    if (face != ALL_SIDES) {
        llSetLinkPrimitiveParams(link,
            [PRIM_BUMP_SHINY, face, shiny, llList2Integer(bumps, 1)]);
    }
    else {
        integer num = llGetLinkNumberOfSides(link);
        for (face = 0 ; face < num ; face++) {
            llSetLinkPrimitiveParams(link,
                [PRIM_BUMP_SHINY, face, shiny, llList2Integer(bumps, face*2+1)]);
        }
    }
}

// --- -----------------------------------------------------------------------

default {
    // --- administration ----------------------------------------------------

    state_entry() {
        kOwner  = llGetOwner();
        gPrims  = llGetNumberOfPrims();

        // fill up the dictionary
        integer link;
        integer links = llGetNumberOfPrims();
        lLinks        = [];
        for (link = 0 ; link <= links ; link++) {
            lLinks += llToLower(llGetLinkName(link));
        }

        llOwnerSay("Painter started. Touch to open listen, long touch to reset");

        //// 256 prims, 63 chars -> 52 kB used
        //// 256 prims, 8 chars  -> 23 kB used
        //// 1 prim,    63 chars -> 14 kB used
        //llOwnerSay("state_entry: used "+(string)llGetUsedMemory()+" Bytes");
    }

    on_rez(integer param) {
        llResetScript();
    }

    touch_start(integer number) {
        if (llDetectedKey(0) != kOwner) return;
        llResetTime();
    }

    touch_end(integer number) {
        if (llDetectedKey(0) != kOwner) return;

        if (llGetTime() > 1.5) llResetScript();

        else if (hListen == 0) {
            hListen = llListen(CHANNEL, "", NULL_KEY, "");
            llOwnerSay("listen open (/"+(string)CHANNEL+"close to close again)");
        }
    }

    changed(integer change) {
        if (change & CHANGED_LINK) llResetScript();
    }

    // --- chat interface ----------------------------------------------------

    listen(integer channel, string name, key id, string message) {
        if (llGetOwnerKey(id) != kOwner) return;
        message = llToLower(llStringTrim(message, STRING_TRIM));

        // 1. Supercommand "close"

        if (message == "close") {
            llListenRemove(hListen);
            hListen = 0;
            llOwnerSay("listen closed (touch to open again)");
            return;
        }

        // 2. Regular command "prim face commandlist"
        //    while prim is "set", "all" or a prim number or name.
        //                  Omitted for a single prim build
        //    and   face is "each", face number or face name from da list

        list    cmds = llParseString2List(message, [" ", ",", ";"], []);
        integer link;
        integer face;
        if (gPrims > 1) {
            name     = llList2String(cmds, 0);  // prim
            message  = llList2String(cmds, 1);  // face
            cmds     = llDeleteSubList(cmds, 0, 1);
        }
        else {
            name     = "set";                   // prim
            message  = llList2String(cmds, 0);  // face
            cmds     = llDeleteSubList(cmds, 0, 0);
        }

        // a. testing face is faster

        if      (message == "each") face = ALL_SIDES;
        else if (message == "0")    face = 0;
        else {
            face = (integer)message;
            if (face == 0) {
                face  = llListFindList(FACE_NUMS, [message]);
                if (face < 0) {
                    llOwnerSay("No such face: '"+message+"'");
                    return;
                }
                else {
                    face = llList2Integer(FACE_NUMS, face+1);
                }
            }
        }

        // b. testing target prim "set", "all" or number

        if      (name == "set") link  = LINK_THIS;
        else if (name == "all") link  = LINK_SET;
        else if (name == "0")   link  = 0;
        else {
            link = (integer)name;
            if (link == 0) {
                link = llListFindList(lLinks, [name]);
                if (link < 0) {
                    llOwnerSay("No such link: '"+name+"'");
                    return;
                }
            }
        }

        // 3. processing commandlist
        //    List : color A7B8C9, fullb Y/N/1/0, shiny num,
        //           image key, glow value, alpha value
        //

        while (cmds != []) {
            name     = llList2String(cmds, 0);  // command
            message  = llList2String(cmds, 1);  // parameter
            cmds     = llDeleteSubList(cmds, 0, 1);

            // color hex-value
            if (name == "color") {
                message   = "0x"+message;
                channel   = (integer)message;

                integer r = (channel>>16)&0xFF;
                integer g = (channel>>8)&0xFF;
                integer b = channel&0xFF;

                llSetLinkColor(link,
                    <(float)r, (float)g, (float)b>/255.0, face);
            }

            // alpha float
            else if (name == "alpha") {
                float val = (float)message;
                if      (val < 0.0) val = 0.0;
                else if (val > 1.0) val = 1.0;

                llSetLinkAlpha(link, val, face);
            }

            // glow float
            else if (name == "glow") {
                float val = (float)message;
                if      (val < 0.0) val = 0.0;
                else if (val > 1.0) val = 1.0;

                llSetLinkPrimitiveParamsFast(link,
                    [PRIM_GLOW, face, val]);
            }

            // shiny 0..3
            else if (name == "shiny") {
                channel = (integer)message;
                if      (channel < 0) channel = 0;
                else if (channel > 3) channel = 3;

                // Work on entire linkset
                if (link == LINK_SET) {
                    for (link = 1 ; link <= gPrims ; link++) {
                        changeShiny(link, face, channel);
                    }
                }

                // Only a single prim
                else {
                    changeShiny(link, face, channel);
                }
            }

            // fullb boolean
            else if (name == "fullb") {
                if      (message == "y") channel = 1;
                else if (message == "n") channel = 0;
                else                     channel = (integer)message;

                llSetLinkPrimitiveParamsFast(link,
                    [PRIM_FULLBRIGHT, face, channel]);
            }

            // image key
            else if (name == "image") {
                llSetLinkTexture(link, message, face);
            }

            else llOwnerSay("No such command: '"+name+"'");

        }
    }
}

// --- ------------------------------------------
```