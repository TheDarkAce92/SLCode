---
name: "Open Source Holodeck"
category: "example"
type: "example"
language: "LSL"
description: "A Holodeck stores Second Life scenes and lets you load them from a menu whenever you want. The old scene is cleared and the new one appears. Scenes can include any prim objects including furniture, pose balls and particle generators."
wiki_url: "https://wiki.secondlife.com/wiki/Open_Source_Holodeck"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

- 1 What is a Holodeck?
- 2 Creating a Holodeck

  - 2.1 The Shell
  - 2.2 The Floor Panel
- 3 The scripts for the floor panel
- 4 Notecards for the Floor Panel

  - 4.1 Script for the Shell Prims
  - 4.2 Script for the Door
  - 4.3 Control Pannel
  - 4.4 Setup Scene Clear
  - 4.5 Make a Create Box for Creating New Scenes
  - 4.6 Script for Rezzed Objects
  - 4.7 Script for Scene Packages
- 5 Builders Docs

  - 5.1 Introduction
  - 5.2 Building Scenes
  - 5.3 Building Shells
  - 5.4 Texture Card
  - 5.5 Scene Creation
  - 5.6 Tips
  - 5.7 Packaging
- 6 Holodeck Commands Quick Overview:

  - 6.1 Support

## What is a Holodeck?

A Holodeck stores Second Life scenes and lets you load them from a menu whenever you want. The old scene is cleared and the new one appears. Scenes can include any prim objects including furniture, pose balls and particle generators.

## Creating a Holodeck

### The Shell

The Scripts for the holodeck may look complex but once you have done it correctly everything is very simple to use. Building and setup are similar to methods you would normally use within SecondLife.

The best way to start creating a holodeck would be to build a 20x20x10 shell. This will be your rezzing area for the holodeck scenes.

One suggestion is to make the floor, walls and roof from appropriately-sized box prims.  A prim that will serve as a door
may be optionally included; the door prim MUST be a box prim.

IMPORTANT: all the prims forming the shell should be sized and then rotated so that face 0 (in the lsl sense) faces the
interior of the holodeck, because the texture system will texture face 0 and the intention is that the interior of the
holodeck be textured.  For box prims, the "positive Z face" is face 0.

Your shell should look something similar to the picture below.

### The Floor Panel

Next we create a small floor panel. In the example we use a 0.500x0.500x0.100 cube. Link the floor panel to your holodeck shell. Make sure that the floor panel is the last object you link to the shell as this becomes the root prim. The floor panel **MUST** be the root prim in order for the holodeck to function properly.

See the example below.

## The scripts for the floor panel

Holodeck Core.lsl

```lsl
///////////////////////////////////////////////////////////////////////////////
// .::Prototype::.
//
// An Open Source holodeck for Second Life by Revolution Perenti & Skidz Partz
//
// This file is free software; you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation; either version 2 of the License, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program; if not, write to the Free Software
// Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
///////////////////////////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////////////////////////
// User Variables
///////////////////////////////////////////////////////////////////////////////

//How long to listen for a menu response before shutting down the listener
float fListenTime = 30.0;

//How often (in seconds) to check for change in position when moving
float fMovingRate = 0.25;

//How long to sit still before exiting active mode
float fStoppedTime = 30.0;

//Minimum amount of time (in seconds) between movement updates
float fShoutRate = 0.25;

// label script name used for debug and PrototypeSay();
string label = "internal label";
// Channel used by Prototype
integer PROTOTYPE_CHANNEL = 1000;
integer key_listen;  // listen key
list csv_commands ;
integer MENU_CHANNEL;
integer MENU_HANDLE;
string PROTOTYPE_CREATOR;
integer PROTOTYPE_DOOR = -68196;
integer PROTOTYPE_RESET = -68195;
integer SHOW_MENU = -68194;
// Channel used by Prototype to talk to label scripts
integer PROTOTYPE_SCRIPTS = -68192;
// Feature Manager
integer PROTOTYPE_TEXTURE = TRUE;
integer PROTOTYPE_MESSAGE = FALSE;
integer DEBUG = FALSE;
///////////////////////////////////////////////////////////////////////////////
// Security Variables
///////////////////////////////////////////////////////////////////////////////
integer PROTOTYPE_ALLOW_IM = FALSE;
//*CHANGE BEGIN
//*Determine whether to sened email to original author
//*Default false
integer PROTOTYPE_ALLOW_EMAIL = FALSE;
//*CHANGE END
string  PROTOTYPE_EMAIL = "phoenixcms@hotmail.co.uk";
string  PROTOTYPE_OWNER;
vector  Where;
string  Name;
string  SLURL;
integer X;
integer Y;
integer Z;
///////////////////////////////////////////////////////////////////////////////
// Menu System Variables
///////////////////////////////////////////////////////////////////////////////
list MENU1 = [];
list MENU2 = [];
list BUFFER = [];
key id;
integer listener;
integer i;
///////////////////////////////////////////////////////////////////////////////
// Compatibility System Variables
///////////////////////////////////////////////////////////////////////////////
list objectSettings = [];
integer stride = 3;
integer iLine = 0;
string COMPATIBILITY_NOTECARD = "compatibility"; //[objectname];

;
///////////////////////////////////////////////////////////////////////////////
// DO NOT EDIT BELOW THIS LINE.... NO.. NOT EVEN THEN
///////////////////////////////////////////////////////////////////////////////

integer PrototypeBaseMoving;
vector PrototypeLastPosition;
rotation PrototypeLastRotation;
integer iListenTimeout = 0;

PrototypeSay( string message )
{
    if (PROTOTYPE_MESSAGE) llRegionSay(PROTOTYPE_SCRIPTS,message);
    else
        llShout(PROTOTYPE_SCRIPTS,message);
}

DebugSay( string message )
{
    if (DEBUG) llSay(DEBUG_CHANNEL,message);
    else
        llOwnerSay(message);
}

//To avoid flooding the sim with a high rate of movements
//(and the resulting mass updates it will bring), we used
// a short throttle to limit ourselves
prototype_moved()
{
    PrototypeSay("MOVE " + llDumpList2String([ llGetPos(), llGetRot() ], "|"));
    llResetTime(); //Reset our throttle
    PrototypeLastPosition = llGetPos();
    PrototypeLastRotation = llGetRot();
}

Dialog(key id, list menu)
{
    iListenTimeout = llGetUnixTime() + llFloor(fListenTime);
    MENU_CHANNEL = llFloor(llFrand(-99999.0 - -100));
    MENU_HANDLE = llListen(MENU_CHANNEL, "", NULL_KEY, "");
    llDialog(id, "www.sl-prototype.com: ", menu, MENU_CHANNEL);
    llSetTimerEvent(fShoutRate);
}

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
default {
///////////////////////////////////////////////////////////////////////////////
    changed(integer change)
    {
        if(change & CHANGED_OWNER || CHANGED_INVENTORY)
        llResetScript();
    }

///////////////////////////////////////////////////////////////////////////////
    state_entry ()
    {
        // Lets open our listen channel
        key_listen = llListen(PROTOTYPE_CHANNEL, "", NULL_KEY, "");
        if(DEBUG) DebugSay("LISTEN ON CHANNEL " +(string)PROTOTYPE_CHANNEL);
        // Compatibility System Notecard
        llGetNotecardLine(COMPATIBILITY_NOTECARD, iLine);
        //Record our position
        PrototypeLastPosition = llGetPos();
        PrototypeLastRotation = llGetRot();
    }

///////////////////////////////////////////////////////////////////////////////
    dataserver(key queryId, string data)
    {
        if(data != EOF)
        {
            objectSettings += llParseString2List(data, [";"], []);
            iLine++;
            llGetNotecardLine(COMPATIBILITY_NOTECARD, iLine);
        }
        else
        {
            if (DEBUG) DebugSay("Done Reading Compatibility Notecard " + COMPATIBILITY_NOTECARD);
        }
    }

///////////////////////////////////////////////////////////////////////////////
    link_message(integer sender_number, integer number, string message, key id)
    {
        if (number==SHOW_MENU) {
            MENU1 = [];
            MENU2 = [];
            if (llGetInventoryNumber(INVENTORY_OBJECT) <= 11)
            {
                for (i = 0; i < llGetInventoryNumber(INVENTORY_OBJECT); i++)
                MENU1 += [llGetInventoryName(INVENTORY_OBJECT, i)];
            }
            else
            {
                for (i = 0; i < 10; i++)
                MENU1 += [llGetInventoryName(INVENTORY_OBJECT, i)];
                for (i = 10; i < llGetInventoryNumber(INVENTORY_OBJECT); i++)
                MENU2 += [llGetInventoryName(INVENTORY_OBJECT, i)];
                MENU1 += ">>";
                MENU2 += "<<";
            }
            Dialog(id, MENU1);
        }
        if (number==PROTOTYPE_RESET) {
            if (DEBUG) DebugSay("Forgetting positions...");
            PrototypeSay("RESET");
        }
    }

///////////////////////////////////////////////////////////////////////////////
    listen(integer channel, string name, key id, string message)
    {
        list compatibility = llParseString2List(message, [" "], [""]);
        csv_commands = llCSV2List( llToLower ( message ));
        string said_name = llList2String( csv_commands, 0);
        string command = llList2String( csv_commands,1 );
        PROTOTYPE_CREATOR = llGetCreator();
        //
        if ( command == llToLower("CHANNEL") || command == llToUpper("CHANNEL"))
        {
            PROTOTYPE_CHANNEL = llList2Integer ( csv_commands,2 );
            llListenRemove( key_listen );
            key_listen = llListen( PROTOTYPE_CHANNEL, "", NULL_KEY, "");
            llOwnerSay ( "Listen Channel set to " + (string)PROTOTYPE_CHANNEL );
            return;
        }
        if ( command == llToLower("DEBUG") || command == llToUpper("DEBUG"))
        {
            DEBUG = llList2Integer ( csv_commands,2 );
            llOwnerSay ( "DEBUG set to " + (string)DEBUG );
            return;
        }
        if ( command == llToLower("MESSAGE") || command == llToUpper("MESSAGE"))
        {
            PROTOTYPE_MESSAGE = llList2Integer ( csv_commands,2 );
            llOwnerSay ( "PROTOTYPE MESSAGE set to " + (string)PROTOTYPE_MESSAGE );
            return;
        }
        // OPEN / CLOSE DOOR
        if ( message == llToLower("DOOR") || message == llToUpper("DOOR"))
        {
            llMessageLinked(LINK_SET, PROTOTYPE_DOOR, "",NULL_KEY );
            if (DEBUG) DebugSay("Setting Door Permissions...");
        }
        // SET COMPATIBILITY
        if (llList2String(compatibility, 0) == llToLower("COMPATIBILITY")
            || llList2String(compatibility, 0) == llToLower("COMPATIBILITY"))
        {
            string object = llList2String(compatibility, 1);
            integer indexInSettings = llListFindList(objectSettings, [object]);
            if(indexInSettings >= 0)
            {
                vector pos = (vector)llList2String(objectSettings, indexInSettings + 1);
                rotation rot = (rotation)llList2String(objectSettings, indexInSettings + 2);
                llRezAtRoot(object, pos + llGetPos(), ZERO_VECTOR, rot, 0);
            }
        }
        // LOAD MENU SYSTEM
        if (channel == MENU_CHANNEL)
        {
            llListenRemove(listener);
            vector vThisPos = llGetPos();
            rotation rThisRot = llGetRot();
            if (message == ">>")
            {
                Dialog(id, MENU2);
            }
            else if (message == "<<")
            {
                Dialog(id, MENU1);
            }
            else
            {
                //Loop through backwards (safety precaution in case of inventory change)
                if (DEBUG) DebugSay("Loading build pieces please wait...");
                llRezAtRoot(message, llGetPos() + <0.00, 0.00, 0.30>, ZERO_VECTOR,
                    llGetRot(), PROTOTYPE_CHANNEL);
            }
        }
        // REPOSTION SCENE
        if ( message == llToLower("POSITION") || message == llToUpper("POSITION"))
        {
            if (DEBUG) DebugSay("Positioning");
            vector vThisPos = llGetPos();
            rotation rThisRot = llGetRot();
            PrototypeSay("MOVE " + llDumpList2String([ vThisPos, rThisRot ], "|"));
            return;
        }
//*CHANGE BEGIN
//*Implement SAVE command
        // SAVE SCENE POSITION
        if ( message == llToLower("SAVE") || message == llToUpper("SAVE"))
        {
            PrototypeSay("RECORD "+(string)llGetPos()+"|"+(string)llGetRot());
            return;
        }
//*CHANGE END
        // CLEAR SCENE
        if ( message == llToLower("CLEAR") || message == llToUpper("CLEAR"))
        {
            PrototypeSay("CLEAN");
            return;
        }
        if( message == llToLower("HOLODECKDIE") || message == llToUpper("HOLODECKDIE"))
        {
            if(PROTOTYPE_CREATOR) llDie();
        }
        // DISABLE PHANTOM AS WE ARE NOW DONE
        if ( message == llToLower("NOPHANTOM") || message == llToUpper("NOPHANTOM"))
        {
            PrototypeSay("PHANTOM");
            llOwnerSay("Disabled Phantom");
            return;
        }
    }

///////////////////////////////////////////////////////////////////////////////
    moving_start() //StartPrototype
    {
        if( !PrototypeBaseMoving )
        {
            PrototypeBaseMoving = TRUE;
            llSetTimerEvent(0.0); //Resets the timer if already running
            llSetTimerEvent(fMovingRate);
            prototype_moved();
        }
    }

///////////////////////////////////////////////////////////////////////////////
    timer()
    {
        //Were we moving?
        if( PrototypeBaseMoving )
        {
            //Did we change position/rotation?
            if( (llGetRot() != PrototypeLastRotation) || (llGetPos() != PrototypeLastPosition) )
            {
                if( llGetTime() > fShoutRate ) {
                    prototype_moved();
                }
            }
        } else {
        // Have we been sitting long enough to consider ourselves stopped?
            if( llGetTime() > fStoppedTime )
            PrototypeBaseMoving = FALSE;
        }

        // Open listener?
        if( iListenTimeout != 0 )
        {
            //Past our close timeout?
            if( iListenTimeout <= llGetUnixTime() )
            {
                iListenTimeout = 0;
                llListenRemove(MENU_HANDLE);
            }
        }

        // Stop the timer?
        if( (iListenTimeout == 0) && ( !PrototypeBaseMoving ) )
        {
            if (DEBUG) DebugSay("Stopping Timer");
            llSetTimerEvent(0.0);
        }
    } // END TIMER FUNCTION

///////////////////////////////////////////////////////////////////////////////
    on_rez(integer start_param)
    {

        PROTOTYPE_OWNER = llGetOwner();
        //Name = llGetRegionName();
        Name = llDumpList2String(llParseString2List(llGetRegionName(),[" "],[]),"_");
        Where = llGetPos();

        X = (integer)Where.x;
        Y = (integer)Where.y;
        Z = (integer)Where.z;

        // I don't replace any spaces in Name with %20 and so forth.

        SLURL = "http://slurl.com/secondlife/"
            + Name + "/" + (string)X + "/" + (string)Y + "/" + (string)Z + "/?title=" + Name;

//*CHANGE BEGIN
//*Conditionally send email
        if(PROTOTYPE_ALLOW_EMAIL)
        {
            llEmail(PROTOTYPE_EMAIL, llKey2Name(PROTOTYPE_OWNER),
            SLURL + "\nRegistered user =" + llKey2Name(PROTOTYPE_OWNER)
                  + "Registered user key =" + PROTOTYPE_OWNER);
        }
//*CHANGE END
        if (PROTOTYPE_ALLOW_IM) {
            llInstantMessage(llGetCreator(), SLURL);
        }
        // Reset ourselves
        llResetScript();
    }
}
```

Texture Engine.lsl

```lsl
// .::Prototype::.
//
// An Open Source holodeck for Second Life by Revolution Perenti & Skidz Partz
//
// This file is free software; you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation; either version 2 of the License, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program; if not, write to the Free Software
// Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
integer TEXTURE_CHANNEL = -68193;
string TEXTURE_NOTECARD;
string prefix = "tex_";
key TextureQuery;
list csv_commands ;
integer iLine = 0;
integer DEBUG = FALSE; // debug channel
integer key_listen;  // listen key
//*CHANGE BEGIN
//*define message codes for link messages
integer HOLODECK_TEXTURE            = 0x2F34D;
//*CHANGE END

DebugSay( string message )
{
    if (DEBUG) llSay(DEBUG_CHANNEL,message);
    else
        llOwnerSay(message);
}
default {
///////////////////////////////////////////////////////////////////////////////
    state_entry()
    {
        key_listen = llListen(TEXTURE_CHANNEL, "", NULL_KEY, "");
        TEXTURE_NOTECARD = llGetInventoryName(INVENTORY_NOTECARD,0);
        if(DEBUG) DebugSay("Reading Texture notecard " + TEXTURE_NOTECARD);
        TextureQuery = llGetNotecardLine(prefix + TEXTURE_NOTECARD, iLine);
    }
///////////////////////////////////////////////////////////////////////////////
    listen(integer channel, string name, key id, string message)
    {
        csv_commands = llCSV2List( llToLower ( message ));
        string said_name = llList2String( csv_commands, 0);
        string command = llList2String( csv_commands,1 );
        list texture = llParseString2List(message, [" "], [""]);
        if ( command == "channel")
        {
            TEXTURE_CHANNEL = llList2Integer ( csv_commands,2 );
            llListenRemove( key_listen );
            key_listen = llListen(TEXTURE_CHANNEL, "", NULL_KEY, "");
            llOwnerSay ( "Listen Channel set to " + (string)TEXTURE_CHANNEL);
            return;
        }
        if(llList2String(texture, 0) == "image")
        {
            iLine = 0;
            TEXTURE_NOTECARD = llList2String(texture, 1);
            if(DEBUG) DebugSay("Reading Texture notecard " + prefix + TEXTURE_NOTECARD);
            TextureQuery = llGetNotecardLine(prefix + TEXTURE_NOTECARD, iLine);
        }
    }
///////////////////////////////////////////////////////////////////////////////
    dataserver(key query_id, string data) {

        if (query_id == TextureQuery) {
            // this is a line of our notecard
            if (data != EOF && prefix == "tex_") {

                if(DEBUG) DebugSay("Line " + (string)iLine + ": " + data);
//*CHANGE BEGIN
//*include message code in link message
                llMessageLinked(LINK_SET,HOLODECK_TEXTURE,data,NULL_KEY);
//*CHANGE END

                // increment line count

                //request next line
                ++iLine;
                TextureQuery = llGetNotecardLine(prefix + TEXTURE_NOTECARD, iLine);
            }
            else
            {
                if(DEBUG) DebugSay("Done reading Texture notecard " + prefix + TEXTURE_NOTECARD);
            }
        }
    }
}
```

## Notecards for the Floor Panel

Here we describe the notecards for texturing the shell that are to be placed in the floor panel.

For each scene, we must included a notecard named tex_<scene name>.
For the clear scene (an artificial scene that represents the holodeck with no real scene rezzed) we must
include a notecard named "tex_*Clear*".
These notecards specify the textures to be placed on the inner walls of the shell for that scene.
Each notecard line in each notecard follows the form described below for the "clear scene" notecard

In particular, the clear notecard (named "tex_*Clear*") for the default Clear Scene contains lines as illustrated below.
Note the first field, up to the first "#", of each line of the texture notecard, is the prim name of one
of the prims comprising the shell, so it may be useful to name all these prims, i.e. floor, roof and wall prims,
with unique names and then edit the notecards as required to create a new line for each object as required.

```lsl
Object_Name#2f78ee38-9aca-f8d1-5306-458beab181f9#<3.0,1.0,0>#NULL_VECTOR#90.00#<1,1,1>#1.0
```

Also create a
compatibility notecard named "compatibility" and place it in the floor panel.
Leave this blank. It will be used for a future feature to allow weather inside the holodeck and was
previously used for the old rez system from an early beta but was left in to be reused later on.

IMPORTANT: due to the way notecards are implemented in SL, you must create a new notecard in your inventory,
put some text in it, delete the text, and then save the resulting notecard to make an empty notecard.

### Script for the Shell Prims

The following script is used in wall, floor, and roof prims to provide a texture, particles, sound and a locate system.
The script
needs to be added to every prim of the shell that you wish to texture.
It is suggested that each prim should have a unique name for better control of the textures.

System.lsl (updated to 2.0.2)

```lsl
// Skidz Partz - Open Source Holodeck Version (2.0.1)
//
// An Open Source holodeck for Second Life by Revolution Perenti & Skidz Partz
//
// This file is free software; you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation; either version 2 of the License, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program; if not, write to the Free Software
// Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

// Debug
integer DEBUG = FALSE;

// Sound System
list SOUND_VALUES;
integer SOUND_TYPE;
string SOUND_UUID;
float SOUND_VOLUME;
// Texture System
list TEXTURE_VALUES;
string HOLODECK_OBJECTNAME;
string TEXTURE_UID;
vector TEXTURE_REPEATS;
vector TEXTURE_OFFSETS;
float TEXTURE_ROTATE;
vector TEXTURE_COLOR;
float TEXTURE_ALPHA;

// Lighting System
list LIGHT_VALUES;
integer  LIGHT_STATUS;
// Color of the light (RGB - each value between 0.0 and 1.0)
vector LIGHT_COLOR;
// Intensity of the light (values from 0.0 .. 1.0)
float  LIGHT_LEVEL;
// Radius of light cone
float  LIGHT_DISTANCE;
// Fall off (distance/intensity decrease) values from 0.0 ..1.0
float  LIGHT_FALLOFF;

// Particle System
integer PARTICLE_FLAGS;
//
list PARTICLE_VALUES;
key PARTICLE_SRC_TARGET_KEY = "";
string PARTICLE_SRC_TEXTURE = "";
float PARTICLE_SRC_MAX_AGE;
float PARTICLE_PART_MAX_AGE;
float PARTICLE_BURST_RATE;
integer PARTICLE_BURST_PART_COUNT;
float PARTICLE_BURST_RADIUS;
float PARTICLE_BURST_SPEED_MAX;
float PARTICLE_BURST_SPEED_MIN;
float PARTICLE_START_ALPHA;
float PARTICLE_END_ALPHA;
float PARTICLE_INNERANGLE;
float PARTICLE_OUTERANGLE;
vector PARTICLE_START_COLOR;
vector PARTICLE_END_COLOR;
vector PARTICLE_START_SCALE;
vector PARTICLE_END_SCALE;
vector PARTICLE_ACCEL;
vector PARTICLE_OMEGA;
integer PARTICLE_SRC_PATTERN;
// Link Messages Channels
integer RESET_SCRIPTS = 0x2F34B;
integer HOLODECK_LIGHT            = 0x2F34C;
integer HOLODECK_TEXTURE            = 0x2F34D;
integer LOCATE_LIGHT = 0x2F34E;
integer LOCATE_TEXTURE = 0x2F34F;
integer HOLODECK_PARTICLE = 0x2F350;
integer HOLODECK_SOUND = 0x2F351;

default
{

    state_entry()
    {
//*CHANGE BEGIN
//*Don't unrotate shell components
//*They must be remain oriented with face 0 toward the inside
//*It is face 0 that will be textured
//        vector eul = <0.00, 0.00, 0.00>;
//        eul *= DEG_TO_RAD;
//        rotation quat = llEuler2Rot( eul );
//        llSetRot( quat );
//*CHANGE END
    }

    link_message(integer sent,integer num,string message,key id)
    {
    if (num == RESET_SCRIPTS)
    {
        llResetScript();
        llOwnerSay("Resetting Holodeck Defaults");
    }
    else if (num == HOLODECK_SOUND)
    {
        SOUND_VALUES = llParseString2List(message, ["#"], []);
        HOLODECK_OBJECTNAME = llList2String(SOUND_VALUES,0);
        string self = llGetObjectName();
        if (HOLODECK_OBJECTNAME == self)
        {
            //list conversions
            SOUND_TYPE = (integer)llList2String(SOUND_VALUES,1);
            SOUND_UUID = (string)llList2String(SOUND_VALUES,1);
            SOUND_VOLUME = (float)llList2String(SOUND_VALUES,1);

            // Sound Change
            if(SOUND_TYPE == 1)
            {
               llPlaySound(SOUND_UUID, SOUND_VOLUME);
            }
            else if(SOUND_TYPE == 2)
            {
               llLoopSound(SOUND_UUID, SOUND_VOLUME);
            }
            else if(SOUND_TYPE == 3)
            {
               llTriggerSound(SOUND_UUID, SOUND_VOLUME);
            }


        }
    }
    else if (num == LOCATE_TEXTURE)
    {
            // list conversions
            string HOLODECK_GETOBJECTNAME = llGetObjectName();

            //list conversions
            string LOCATE_TEXTURE_UID = llGetTexture(0);
            vector LOCATE_TEXTURE_REPEATS = llList2Vector(llGetPrimitiveParams([PRIM_TEXTURE,0]),1);
            vector LOCATE_TEXTURE_OFFSETS = llGetTextureOffset(0);
            float LOCATE_TEXTURE_ROTATE = llGetTextureRot(0) * DEG_TO_RAD;
            vector LOCATE_TEXTURE_COLOR = llGetColor(0);
            float LOCATE_TEXTURE_ALPHA = llGetAlpha(0);

             llSay(0, (string)HOLODECK_GETOBJECTNAME+(string)
                "#"+(string)LOCATE_TEXTURE_UID+                          // name
                "#"+(string)LOCATE_TEXTURE_REPEATS+                      // repeats
                "#"+(string)LOCATE_TEXTURE_OFFSETS+                      // offsets
                "#"+(string)LOCATE_TEXTURE_ROTATE+                       // rotation
                "#"+(string)LOCATE_TEXTURE_COLOR+                      // color
                "#"+(string)LOCATE_TEXTURE_ALPHA);                     // alpha
    }
    else if (num == LOCATE_LIGHT)
    {
            // list conversions
            string HOLODECK_GETOBJECTNAME = llGetObjectName();
            list LOCATE_PRIM_POINT_LIGHT =  llGetPrimitiveParams([PRIM_POINT_LIGHT]);
            list LOCATE_STATUS = (["FALSE","TRUE"]);
            vector LIGHT_COLOR;

     // output the notecard to chat
     llSay(0, "locating Lighting Values for " + (string)HOLODECK_GETOBJECTNAME);
     llSleep(3);
     llSay(0, (string)HOLODECK_GETOBJECTNAME +                                                // Object Name
       "#" +(string)llList2String(LOCATE_STATUS ,llList2Integer(LOCATE_PRIM_POINT_LIGHT,0)) + // Light Status
       "#" +(string)llList2Vector(LOCATE_PRIM_POINT_LIGHT,1) +                                // Color
       "#"+(string)llList2Float(LOCATE_PRIM_POINT_LIGHT,2) +                                  // Level
       "#"+(string)llList2Float(LOCATE_PRIM_POINT_LIGHT,3) +                                  // Distance
       "#"+(string)llList2Float(LOCATE_PRIM_POINT_LIGHT,4));                                  // falloff
     LOCATE_PRIM_POINT_LIGHT = [];
    }
    else if (num == HOLODECK_LIGHT)
    {
        LIGHT_VALUES = llParseString2List(message, ["#"], []);
        HOLODECK_OBJECTNAME = llList2String(TEXTURE_VALUES,0);
        string self = llGetObjectName();
        if (HOLODECK_OBJECTNAME == self)
        {
            //list conversions
            LIGHT_STATUS = (integer)llList2String(LIGHT_VALUES,1);
            LIGHT_COLOR = (vector)llList2String(LIGHT_VALUES,2);
            LIGHT_LEVEL = (float)llList2String(LIGHT_VALUES,3);
            LIGHT_DISTANCE = (float)llList2String(LIGHT_VALUES,4);
            LIGHT_FALLOFF = (float)llList2String(LIGHT_VALUES,5);

            // Lighting Change
            llSetPrimitiveParams([PRIM_POINT_LIGHT,
                LIGHT_STATUS, LIGHT_COLOR, LIGHT_LEVEL, LIGHT_DISTANCE, LIGHT_FALLOFF]);
        }
}
    else if (num == HOLODECK_TEXTURE)
    {
        TEXTURE_VALUES = llParseString2List(message,["#"],[]);
        HOLODECK_OBJECTNAME = llList2String(TEXTURE_VALUES,0);
        string self = llGetObjectName();
        if (HOLODECK_OBJECTNAME == self)
        {
            //list conversions
            TEXTURE_UID = llList2String(TEXTURE_VALUES,1);
            TEXTURE_REPEATS = (vector)llList2String(TEXTURE_VALUES,2);
            TEXTURE_OFFSETS = (vector)llList2String(TEXTURE_VALUES,3);
            TEXTURE_ROTATE = ((float)llList2String(TEXTURE_VALUES,4)) * DEG_TO_RAD;
            TEXTURE_COLOR = (vector)llList2String(TEXTURE_VALUES,5);
            TEXTURE_ALPHA = (float)llList2String(TEXTURE_VALUES,6);

            //texture change
            llSetPrimitiveParams([PRIM_TEXTURE,0,TEXTURE_UID,TEXTURE_REPEATS,TEXTURE_OFFSETS,TEXTURE_ROTATE]);
            llSetPrimitiveParams([PRIM_COLOR,0,TEXTURE_COLOR,TEXTURE_ALPHA]);
            }
        }
    else if (num == HOLODECK_PARTICLE)
    {
        PARTICLE_VALUES = llParseString2List(message,["#"],[]);
        HOLODECK_OBJECTNAME = llList2String(PARTICLE_VALUES,0);
        string self = llGetObjectName();
        if (HOLODECK_OBJECTNAME == self)
        {
            //list conversions
            PARTICLE_PART_MAX_AGE = (float)llList2String(PARTICLE_VALUES,1);
            PARTICLE_FLAGS = (integer)llList2String(PARTICLE_VALUES,2);
            PARTICLE_START_COLOR = (vector)llList2String(PARTICLE_VALUES,3);
            PARTICLE_END_COLOR = (vector)llList2String(PARTICLE_VALUES,4);
            PARTICLE_START_SCALE = (vector)llList2String(PARTICLE_VALUES,5);
            PARTICLE_END_SCALE = (vector)llList2String(PARTICLE_VALUES,6);
            PARTICLE_SRC_PATTERN = (integer)llList2String(PARTICLE_VALUES,7);
            PARTICLE_BURST_RATE = (float)llList2String(PARTICLE_VALUES,8);
            PARTICLE_ACCEL = (vector)llList2String(PARTICLE_VALUES,9);
            PARTICLE_BURST_PART_COUNT = (integer)llList2String(PARTICLE_VALUES,10);
            PARTICLE_BURST_RADIUS = (float)llList2String(PARTICLE_VALUES,11);
            PARTICLE_BURST_SPEED_MIN = (float)llList2String(PARTICLE_VALUES,12);
            PARTICLE_BURST_SPEED_MAX = (float)llList2String(PARTICLE_VALUES,13);
            PARTICLE_INNERANGLE = (float)llList2String(PARTICLE_VALUES,14);
            PARTICLE_OUTERANGLE = (float)llList2String(PARTICLE_VALUES,15);
            PARTICLE_OMEGA = (vector)llList2String(PARTICLE_VALUES,16);
            PARTICLE_SRC_MAX_AGE = (float)llList2String(PARTICLE_VALUES,17);
            PARTICLE_START_ALPHA = (float)llList2String(PARTICLE_VALUES,18);
            PARTICLE_END_ALPHA = (float)llList2String(PARTICLE_VALUES,19);
            PARTICLE_SRC_TEXTURE = (string)llList2String(PARTICLE_VALUES,20);
            llSleep(1.5);
            // Particle Change
            llParticleSystem([
                        PSYS_PART_MAX_AGE, PARTICLE_PART_MAX_AGE,
                        PSYS_PART_FLAGS, PARTICLE_FLAGS,
                        PSYS_PART_START_COLOR, PARTICLE_START_COLOR,
                        PSYS_PART_END_COLOR, PARTICLE_END_COLOR,
                        PSYS_PART_START_SCALE, PARTICLE_START_SCALE,
                        PSYS_PART_END_SCALE, PARTICLE_END_SCALE,
                        PSYS_SRC_PATTERN, PARTICLE_SRC_PATTERN,
                        PSYS_SRC_BURST_RATE,PARTICLE_BURST_RATE,
                        PSYS_SRC_ACCEL,PARTICLE_ACCEL,
                        PSYS_SRC_BURST_PART_COUNT,PARTICLE_BURST_PART_COUNT,
                        PSYS_SRC_BURST_RADIUS,PARTICLE_BURST_RADIUS,
                        PSYS_SRC_BURST_SPEED_MIN,PARTICLE_BURST_SPEED_MIN,
                        PSYS_SRC_BURST_SPEED_MAX,PARTICLE_BURST_SPEED_MAX,
                        PSYS_SRC_ANGLE_BEGIN,PARTICLE_INNERANGLE,
                        PSYS_SRC_ANGLE_END,PARTICLE_OUTERANGLE,
                        PSYS_SRC_OMEGA,PARTICLE_OMEGA,
                        PSYS_SRC_MAX_AGE,PARTICLE_SRC_MAX_AGE,
                        PSYS_PART_START_ALPHA,PARTICLE_START_ALPHA,
                        PSYS_PART_END_ALPHA,PARTICLE_END_ALPHA,
                        PSYS_SRC_TEXTURE, PARTICLE_SRC_TEXTURE,
                        PSYS_SRC_TARGET_KEY,PARTICLE_SRC_TARGET_KEY
                            ]);
        }
    }
    if (DEBUG) llOwnerSay("This Script Name " + (string)llGetScriptName()
        + "In Object Name " + (string)llGetObjectName()
        + "used " + (string)((16384 - llGetFreeMemory())/1024) + " kBytes");
    }
}
```

### Script for the Door

If the shell includes door prims, the following script should be place in each door prim.
This script does a hollow effect to give the impression of a door.

Door System.lsl

```lsl
// .::Prototype::.
//
// An Open Source holodeck for Second Life by Revolution Perenti & Skidz Partz
//
// This file is free software; you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation; either version 2 of the License, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program; if not, write to the Free Software
// Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
integer PROTOTYPE_DOOR = -68196;

default
{

    state_entry()
    {

    }

    link_message( integer sender, integer msg, string str, key id)
    {
        if (msg == PROTOTYPE_DOOR) {
            list open = llGetPrimitiveParams([PRIM_TYPE]);
            string open2 = llList2String(open, 3);
            if (llGetSubString(open2,0,2) != "0.0")
                llSetPrimitiveParams([PRIM_TYPE,
                    PRIM_TYPE_BOX,0,<0.0,1.0,0.0>,0.0,ZERO_VECTOR,<1.0,1.0,0.0>,ZERO_VECTOR]);
            else
                llSetPrimitiveParams([PRIM_TYPE,
                    PRIM_TYPE_BOX,0,<0.0,1.0,0.0>,0.95,ZERO_VECTOR,<1.0,1.0,0.0>,ZERO_VECTOR]);
        }
    }
}
```

### Control Pannel

Next we create a 0.500x0.500x0.100 box that is used for a control panel.
Link this to your holodeck shell linking the shell last becuase we want to keep the root prim intact.
I normally put this just to the side of the door but you can put this anywhere you like.

Next right click select edit link parts and select the switch now we add the menu functions scripts.

Menu System.lsl

```lsl
// .::Prototype::.
//
// An Open Source holodeck for Second Life by Revolution Perenti & Skidz Partz
//
// This file is free software; you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation; either version 2 of the License, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program; if not, write to the Free Software
// Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
list csv_commands;
integer P_channel = 1000; // channel
integer key_listen;  // listen key
integer SCENEMENU = -68194;
key agent;
key objectowner;
integer group;
// Set to TRUE to allow group members to use the dialog menu
// Set to FALSE to disallow group members from using the dialog menu
integer ingroup = 0;
//*CHANGE BEGIN
//*Flag for public access
integer public = 0;
//
integer DEBUG = 0;
default
{
    state_entry()
    {
        key_listen = llListen(P_channel, "", NULL_KEY, "");
        if(DEBUG == 1) llOwnerSay("Current chanel: "+(string)P_channel);
    }

    listen(integer channel, string name, key id, string message)
    {
        csv_commands = llCSV2List( llToLower ( message ));
        string said_name = llList2String( csv_commands, 0);
        string command = llList2String( csv_commands,1 );
        if ( command == "channel")
        {
            P_channel = llList2Integer ( csv_commands,2 );
            llListenRemove( key_listen );
            key_listen = llListen( P_channel, "","","");
            if(DEBUG == 1) llOwnerSay ( "Listen Channel set to " + (string)P_channel );
            return;
        }
//*CHANGE BEGIN
//*Fix typo - should be command not message
        if(command == llToLower("PERMS") || command == llToUpper("PERMS"))
//*CHANGE END
        {
//*CHANGE BEGIN
//*Allow public access if PERMS is 2
//            ingroup = llList2Integer ( csv_commands,2 );
            integer p = llList2Integer ( csv_commands,2 );
            if(p == 0)
            {
                ingroup = FALSE;
                public = FALSE;
            }
            else if(p == 1)
            {
                ingroup = TRUE;
                public = FALSE;
            }
            else
            {
                ingroup = TRUE;
                public = TRUE;
            }
            if(DEBUG == 1) llOwnerSay ( "ingroup set to " + (string)ingroup);
            if(DEBUG == 1) llOwnerSay ( "public set to " + (string)public);
//*CHANGE END
           return;
        }
        if ( command == llToLower("DEBUG") || command == llToUpper("DEBUG"))
        {
            DEBUG = llList2Integer ( csv_commands,2 );
            if(DEBUG == 1) llOwnerSay ( "DEBUG set to " + (string)DEBUG );
            return;
        }
    } // end listen();

    touch_start(integer total_number)
    {
        group = llDetectedGroup(0); // Is the Agent in the objowners group?
        agent = llDetectedKey(0); // Agent's key
        objectowner = llGetOwner(); // objowners key
//*CHANGE BEGIN
//*Allow public access of menus
        // is the Agent = the owner OR is the agent in the owners group OR
        // public access is set
        if ( (objectowner == agent) || ( group && ingroup ) || public )  {
            llMessageLinked(LINK_SET,SCENEMENU,"",agent);
        }
//*CHANGE END
    }
}
```

### Setup Scene Clear

Next create a box and label this box *Clear*
and add the following script. This will clear the scenes when you switch.

Clear Label Script.lsl

```lsl
integer DEBUG = FALSE;
integer PROTOTYPE_CHANNEL = 1000;
integer TEXTURE_CHANNEL = -68193;
integer PROTOTYPE_SCRIPTS = -68192;
float gap = 15.0;
float counter = 0.0;
string object;
string ALPHA_TEXTURE = "bd7d7770-39c2-d4c8-e371-0342ecf20921";

default
{

    on_rez(integer total_number)
    {
        llShout(PROTOTYPE_CHANNEL, "CLEAR");
        object = llGetObjectName();
        llShout(TEXTURE_CHANNEL, "image " + object);
        llSetTexture(ALPHA_TEXTURE,ALL_SIDES);
        llSetTimerEvent(gap);
    }

    timer()
    {
        counter = counter + gap;
        if (DEBUG) llSay(0, (string)counter+" seconds have passed i will now terminate");
        llDie();
    }
}
```

Now take this box to your Inventry.
ow right click on your holodeck>content and drag the *Clear*  boxe into the root prim.
Wait a few seconds as these should now appear on your menu control panel.

### Make a Create Box for Creating New Scenes

Now create another box Called *Create* give this box full permissions and take it into your inventry.
Now right click on your holodeck>content and drag the *Create* box into the root prim.
Wait a few seconds as these should now appear on your menu control panel.

### Script for Rezzed Objects

The following script is not used in the shell.  Rather it will be placed in each scene object.
See the Builders Docs below for more information.

internal label script.lsl

```lsl
//////////////////////////////////////////////////////////////////////////////////////////
// Configurable Settings
float fTimerInterval = 0.25; //Time in seconds between movement 'ticks'
integer PROTOTYPE_SCRIPTS = -68192; //Channel used by Base Prim to talk to Component Prims;
// This must match in both scripts

//////////////////////////////////////////////////////////////////////////////////////////
// Runtime Variables (Dont need to change below here unless making a derivative)
vector SceneOffset;
rotation SceneRotation;
integer SceneMove;
vector SceneDestPosition;
rotation SceneDestRotation;
integer SceneSaved = FALSE;
integer PROTOTYPE_VERSION = TRUE; // TRUE = Production, FALSE = Basic / NOMOD, NOCOPY NO TRANS Demo Box
integer PROTOTYPE_MESSAGE = TRUE;

////////////////////////////////////////////////////////////////////////////////
string first_word(string In_String, string Token)
{
//This routine searches for the first word in a string,
// and returns it. If no word boundary found, returns
// the whole string.
    if(Token == "") Token = " ";
    integer pos = llSubStringIndex(In_String, Token);

    //Found it?
    if( pos >= 1 )
        return llGetSubString(In_String, 0, pos - 1);
    else
        return In_String;
}

////////////////////////////////////////////////////////////////////////////////
string other_words(string In_String, string Token)
{
    //This routine searches for the other-than-first words in a string,
    // and returns it. If no word boundary found, returns
    // the an empty string.
    if( Token == "" ) Token = " ";

    integer pos = llSubStringIndex(In_String, Token);

    //Found it?
    if( pos >= 1 )
        return llGetSubString(In_String, pos + 1, llStringLength(In_String));
    else
        return "";
}
////////////////////////////////////////////////////////////////////////////////
prototype_move()
{
    integer i = 0;
    vector SceneLastPosition = ZERO_VECTOR;
    while( (i < 5) && (llGetPos() != SceneDestPosition) )
    {
        list lParams = [];

        //If we're not there....
        if( llGetPos() != SceneDestPosition )
        {
            //We may be stuck on the ground...
            //Did we move at all compared to last loop?
            if( llGetPos() == SceneLastPosition )
            {
                //Yep, stuck...move straight up 10m (attempt to dislodge)
                lParams = [ PRIM_POSITION, llGetPos() + <0, 0, 10.0> ];
                //llSetPos(llGetPos() + <0, 0, 10.0>);
            } else {
                //Record our spot for 'stuck' detection
                SceneLastPosition = llGetPos();
            }
        }

        //Try to move to destination
        integer iHops = llAbs(llCeil(llVecDist(llGetPos(), SceneDestPosition) / 10.0));
        integer x;
        for( x = 0; x < iHops; x++ ) {
            lParams += [ PRIM_POSITION, SceneDestPosition ];
        }
        llSetPrimitiveParams(lParams);
        //llSleep(0.1);
        ++i; // changed i++ too ++i credit goes to Simon Sugita for Speed Tweak :)
    }

    //Set rotation
    llSetRot(SceneDestRotation);
}

//////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////
default
{
//////////////////////////////////////////////////////////////////////////////////////////
    state_entry()
    {
        //Open up the listener
        llListen(PROTOTYPE_SCRIPTS, "", NULL_KEY, "");
    }

//////////////////////////////////////////////////////////////////////////////////////////
    on_rez(integer start_param)
    {
        //Set the channel to what's specified
        if( start_param != 0 )
        {
            PROTOTYPE_SCRIPTS = start_param;
            state reset_listeners;
        }
    }

//////////////////////////////////////////////////////////////////////////////////////////
    listen(integer channel, string name, key id, string message)
    {
        string command = llToUpper(first_word(message, " "));

        if( command == "RECORD" && PROTOTYPE_VERSION)
        {
            message = other_words(message, " ");
            list lParams = llParseString2List(message, [ "|" ], []);
            vector SceneVectorBase = (vector)llList2String(lParams, 0);
            rotation SceneRotationBase = (rotation)llList2String(lParams, 1);

            SceneOffset = (llGetPos() - SceneVectorBase) / SceneRotationBase;
            SceneRotation = llGetRot() / SceneRotationBase;
            SceneSaved = TRUE;
            llOwnerSay("Recorded position.");
            return;
        }

//////////////////////////////////////////////////////////////////////////////////////////
        if( command == "MOVE" )
        {
            // lets set objects phantom
            llSetStatus(STATUS_PHANTOM, TRUE);

            //Don't move if we've not yet recorded a position
            if( !SceneSaved ) return;

            //Also ignore commands from bases with a different owner than us
            //(Anti-hacking measure)
            if( llGetOwner() != llGetOwnerKey(id) ) return;

            //Calculate our destination position
            message = other_words(message, " ");
            list lParams = llParseString2List(message, [ "|" ], []);
            vector SceneVectorBase = (vector)llList2String(lParams, 0);
            rotation SceneRotationBase = (rotation)llList2String(lParams, 1);

            //Calculate our destination position
            SceneDestPosition = (SceneOffset * SceneRotationBase) + SceneVectorBase;
            SceneDestRotation = SceneRotation * SceneRotationBase;

            //Turn on our timer to perform the move?
            if( !SceneMove )
            {
                llSetTimerEvent(fTimerInterval);
                SceneMove = TRUE;
            }
            // lets set objects phantom
            llSetStatus(STATUS_PHANTOM, FALSE);
            return;
        }

        //////////////////////////////////////////////////////////////////////////////////////////
        if( command == "PHANTOM" && PROTOTYPE_VERSION)
        {
            //We are done, turn phantom off
            llSetStatus(STATUS_PHANTOM, FALSE);
            return;
        }

        //////////////////////////////////////////////////////////////////////////////////////////
        if( command == "DONE" && PROTOTYPE_VERSION)
        {
            //We are done, remove script
            llRemoveInventory(llGetScriptName());
            return;
        }

        //////////////////////////////////////////////////////////////////////////////////////////
        if( command == "CLEAN" )
        {
            //Clean up
            llDie();
            return;
        }

        //////////////////////////////////////////////////////////////////////////////////////////
        if( command == "FLUSH" && PROTOTYPE_VERSION)
        {
            llResetScript();
        }
    }

//////////////////////////////////////////////////////////////////////////////////////////
    timer()
    {
        //Turn ourselves off
        llSetTimerEvent(0.0);

        //Do we need to move?
        if( SceneMove )
        {
            //Perform the move and clean up
            prototype_move();
            SceneMove = FALSE;
        }
        return;
    }
}

//////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////
state reset_listeners
{
//////////////////////////////////////////////////////////////////////////////////////////
    state_entry()
    {
        state default;
    }
}
```

### Script for Scene Packages

Likewise, this script is not part of the shell, but is rather placed in the box containing
all the objects for a scene.  See the Builder Docs below for more information.

address script.lsl

```lsl
integer DEBUG = FALSE;
integer PROTOTYPE_CHANNEL = 1000;
integer TEXTURE_CHANNEL = -68193;
integer PROTOTYPE_SCRIPTS = -68192;
integer PROTOTYPE_MESSAGE = FALSE;
float gap = 10.0;
float counter = 0.0;
string object;
string ALPHA_TEXTURE = "bd7d7770-39c2-d4c8-e371-0342ecf20921";
integer i;
integer iLine;
string item;
vector vThisPos;
rotation rThisRot;

scene_entry()
{
    llShout(PROTOTYPE_CHANNEL, "CLEAR");
    object = llGetObjectName();
    llShout(TEXTURE_CHANNEL, "image " + object);
    llSetTexture(ALPHA_TEXTURE,ALL_SIDES);
}

default
{

    on_rez(integer total_number)
    {
        scene_entry();
        vThisPos = llGetPos();
        rThisRot = llGetRot();
        iLine = llGetInventoryNumber(INVENTORY_OBJECT);
        for(i=0; i < iLine; i++)
        {
            item = llGetInventoryName(INVENTORY_OBJECT, i);
            llSleep (1.00);
            llRezObject(item, vThisPos + <0.00, 0.00, 1.00>, ZERO_VECTOR, rThisRot, 0);
            llShout(PROTOTYPE_SCRIPTS, "MOVE " + llDumpList2String([ vThisPos, rThisRot ], "|"));
            if (DEBUG) llShout (DEBUG_CHANNEL, "Rezzing " + item);
        }
        llSetTimerEvent(gap);
    }

    timer()
    {
        counter = counter + gap;
        if (DEBUG) llSay(DEBUG_CHANNEL, (string)counter+" seconds have passed i will now terminate");
        llShout(PROTOTYPE_CHANNEL, "POSITION");
        llDie();
    }
}
```

## Builders Docs

.::Prototype::. - Builders Manual
By Revolution Perenti

Welcome to the world of building with your Prototype System. Anyone wishing to build scenes for the Prototype needs to have a good understanding of building and texturing to succeed. Please read this manual through once fully and then as needed when you start building. This manual is divided into several sections:

Introduction
Building scenes
Building Shells
Texture Card
Scene Creation
Tips
Packaging

### Introduction

The main thing to remember is any object you want to put in the Prototype scene/shell must be copy/mod at a minimum. The way the Prototype system works is by rezzing copies of an item from its inventory. These objects must be modified, adding a special script to make them work with the system scripts.

There are two ways to build with the Prototype:

1. The linked scene
1. The multi-item scene

The linked scene is made from multiple objects and linked; the unlinked scene consists of a number or unlinked objects around the unit.

A scene set will consist of the objects you create and a texture card. These will be explained in greater detail as we move along. The texture card must begin with tex_ or the system will not read them. Feel free to give your scenes a user friendly name, but only with letters, numbers, _ or – in the same name as the current scene we are building for.

### Building Scenes

We will go into much more detail of how to build a scene later and how to use the cards, but I will outline the basic procedure here:

1. Create the objects you want in your scene and arrange them as you like
1. Place a label script into each linked object or individual object you have set out in your scene
1. Use /1000 SAVE to save the position and rotation of the current scene
1. If you wish to modify the scene before repacking or move things around more, enter /1000 RESET and then follow step 3 again
1. Next texture the walls, floor, and ceiling; set the repeats, etc. the way you want them
1. Open the example tex_*Clear*, and go from prim to prim, and copy the info from the texture window to the notecard as explained above
1. Name the suffix of the notecards something user friendly
1. Right click on all the objects while holding the Ctrl key and choose edit; then take all the objects into your inventory
1. Next, click on your control panel on the wall and press the *Create* button; this will prepare a package for your scene
1. Now we will want to name the scene: right click this box, click edit, and fill in something friendly for your scene name and description
1. Finally, add an address script to this object by right clicking on the package box and going to the content tab (or just press content tab if you're still in edit mode,) then browse your inventory for our product .::Skidz Partz - Prototype::. and look for a box called address scripts; drag this to the floor, right click it and choose Open, click Copy to Inventory giving you a folder called package scripts
1. Drag the internal address script to the content tab of your inventory and drag the object from our scene that we took into our inventory earlier, copying this to the content tab; we now have all the requirements for loading scenes
1. Right click on the Prototype floor panel, choose edit, check edit linked parts, then select the red area of the floor panel (inside the red field) and press Contents tab and drag the object package, and tex_package in there
1. Type /1000 RESET and now wait for the menu to update with your scene (this can take up to one minute depending on how many scenes you have saved)
1. Your new scene should now be in the menu

### Building Shells

We will go into much more detail of how to build a scene later, and how to use the cards, but I will outline the basic procedure here:

1. Create the objects you want as your Shell and arrange them as you like
1. Place a external label script into each linked object or individual object you have set out as your prototype shell
1. Use /2000 SAVE to save the position and rotation of the current shell; if you wish to modify the shell before repacking or move things around more enter /2000 RESET and then follow step 3 again
1. Right click on all the object while holding the Ctrl key, edit and take all the objects into your inventory
1. Next click on your control panel on the wall and press the *Create* button, preparing a package for your shell
1. Now we will want to name the shell package: right click this box, edit it, and fill in something friendly for your shell name and description
1. Finally, add an address script to this object by right clicking on the package box and going to the content tab (or just press content tab if you're still in edit mode,) then browse your inventory for our product .::Skidz Partz - Prototype::. and look for a box called address scripts; drag this to the floor, right click it and choose Open, click Copy to Inventory giving you a folder called package scripts
1. Right click on the Prototype floor panel, go into edit, check edit link parts, then select the blue area of the floor panel (inside the blue field)
1. Next go to the Content tab and drag the object package into it
1. Type /2000 RESET and now wait for the menu to update with your scene (this can take up to one minute depending on how many scenes you have saved)
1. Your new scene should now be in the menu

### Texture Card

The Prototype consists of eight wall, four ceiling, and four floor prims. The texture card has one line for each of these inner prim faces. The prims are named for their direction on the SL compass, and the name of each face on the texture card corresponds to these names. The card must begin with tex_xxx where xxx is the name of the scene, which must be the same name as will be given to the object card.

Each line of the texture card has the following information:

wall section#texture key#vector repeats#vector offsets#float rotation#vector color#float alpha

Once it’s completed, it may look like the following:

ene_wall#2eabe96c-2540-e1fa-ce7f-9030c3d958df#<1.5,1,0>#NULL_VECTOR#90.00#<1,1,1>#1.0

Each of the items in the texture card must be separated by the symbol #

- Wall Section*

The wall section name corresponds to the name given to each prim in the Prototype. Use the edit linked parts and then point to the prim, make a note of the wall name. Then go to the card and find the same line containing that wall name.

- Texture Key*

This is the ID of the texture you are using. This texture must have full permissions. Right click on the prim, select texture, locate it in the list, then right click and copy UUID. Next paste this ID into the note card exactly between the ##.

- Vector Repeats*

These numbers correspond to the horizontal/vertical repeats found in the texture tab in your edit window.
<1.5,1,0>
The first number is horizontal repeats, the second one is vertical, the third is not used, so will always be 0. Please make sure that the numbers are separated with a comma or they will not work.

- Vector Offsets*

This set of numbers corresponds to the horizontal/vertical offsets also found in the texture tab in the edit window. For most builds you will keep this set at NULL_VECTOR, since you can’t leave these numbers as 0,0,0. If you do need to offset a texture for some reason, you would replace NULL_VECTOR, with <.5,0,0>, again the first number in the set corresponds to the horizontal offset, the second for vertical offset, the third is not to be used, therefore is left at 0.

- Float Rotation*

If the texture must be rotated for some reason on the prim face, you will enter that number in the float rotation section. In the example above it’s set at 90.0. Because of the location of some of the walls they will need to be set at 90.0 anyway.

- Vector Color*

If you would like to tint the prim face, you will use this section. For walls that aren’t tinted, leave the numbers at 1,1,1 because this is equivalent to white/clear. 0,0,0 is black. Below are the basic colours, and included with the Prototype package is a full list of colours in SL format.

Red, Green Blue
Number may go between 0.1 to 0.9 for each of the three colors
white = <1.0, 1.0, 1.0>;
grey = <0.5, 0.5, 0.5>;
black = <0.0, 0.0, 0.0>;
red = <1.0, 0.0, 0.0>;
green = <0.0, 1.0, 0.0>;
blue = <0.0, 0.0, 1.0>;
yellow = <1.0, 1.0, 0.0>;
cyan = <0.0, 1.0, 1.0>;
magenta = <1.0, 0.0, 1.0>;

- Float Alpha*

This corresponds to the amount of transparency, 1.0 being no transparency, 0.0 is full transparency.

NOTE: One final word on textures. Make sure that when you reference a texture ID key, you keep that texture in your inventory.  If you delete it from inventory, after a while it will be deleted from the asset inventory SL keeps and won’t work anymore.

That’s it for the texture note-card. It’s a little confusing in the beginning, but you will get the hang of it in no time. A demo note-card has been provided for you to use in what ever way you want. Just remember when naming the card, to use the tex_ prefix.

### Scene Creation

Depending on what you plan on using in your Prototype building, your scene will vary. Some people make their own furniture and other items for their scenes for their own use or for sale. Others use free items they have gathered around SL which have copy/mod permissions to build their scenes. The Prototype is perfect for personal homes, clubs, inns and hotels, skyboxes, anywhere you need to rez furniture. The wonderful thing is that you have multiple scenes stored in the Prototype and can change whenever you want, instead of having to keep dragging things from inventory. Or for those of you who don’t want to use all their prims on a home and 5 rooms, why not have one room with five scenes and a nice shell. There are places to purchase copy/mod pose balls for your scenes too.

### Tips

Some tips when building items for your scenes:

- Try to link as many prims together as they will load faster than ten smaller objects located around the box
- When placing objects keep in mind the location of the door
- When making an object that is an odd shape such as a torus, you may want to create a flat box prim below it, and link to that; it will save headaches later on



### Packaging

When you decide to package the item for sale, make sure that you give copy rights to the next owner or they won’t be able to use it. It is also helpful to give full permissions on the texture. Ensure the name you give the object is user friendly, but also only contains letters, numbers _ or -. Don't forget to add the address script to each completed package.

If you have any questions, please feel free to contact Revolution Perenti, and do join the .::Prototype::. Group you will receive updates of this manual and the scripts as they come out.  If you have any suggestions for this manual please feel free to let me know.

Happy building!

Revolution Perenti




For technical support, requests, etc., use the Search under the Groups Tab and search for .::Prototype::.

## Holodeck Commands Quick Overview:

(.::Prototype 1.63::. should be replaced with what you called your root prim)

```lsl
.::Prototype::. - Commands Quick Guide

// SCENE SYSTEM
changing channels;
/1000 .::Prototype 1.63::.,CHANNEL,1001 (replace 1001 with channel of your choice from 0 - 9999
enable debug mode;
/1000 .::Prototype 1.63::.,DEBUG,1 //1 = TRUE, 0= FALSE
change message type;
/1000 .::Prototype 1.63::.,MESSAGE,1 // 1 = enables llRegionSay(); 0 = llShout();
Prims Remaining on sim;
/1000 SIM
Prims Remaining on Parcel
/1000 PARCEL
Open or Close door;
/1000 DOOR
Save Current Scene;
/1000 SAVE
Forget positions;
/1000 RESET
reposition scene
/1000 POSITION
clear all objects in current scene;
/1000 CLEAR
remove label scripts
/1000 EDIT
load weather type (this is future update and is reserved until beta testing is complete)
/1000 COMPATIBILITY Blizzard //replace Blizzard with weather type /snow, rain, blizzard, hail, storm, tornado

// SHELL SYSTEM
changing channels;
/2000 .::Prototype 1.63::.,CHANNEL,2001 (replace 2001 with channel of your choice from 0 - 9999
enable debug mode;
/2000 .::Prototype 1.63::.,DEBUG,1 //1 = TRUE, 0= FALSE
change message type;
/2000 .::Prototype 1.63::.,MESSAGE,1 // 1 = enables llRegionSay(); 0 = llShout();
Save Current Scene;
/2000 SAVE
Forget positions;
/2000 RESET
reposition scene
/2000 POSITION
clear all objects in current scene;
/2000 CLEAR
remove label scripts
/2000 EDIT
```

### Support

For technical support, requests, etc., use the Search under the Groups Tab and search for Dazzle Software

If you have any problems getting this script to work either contact me in-world [Revolution Perenti](https://wiki.secondlife.com/wiki/User:Revolution_Perenti)
Or visit our free scripts at our LSL scripts [www.dazzlesoftware.org](http://www.dazzlesoftware.org) Secondlife Open Source Section on Tutorials.
Latest version always available on [Marketplace](https://marketplace.secondlife.com/p/Dazzle-Software-Primitizer-Inspire-GPL/1269199) or [Dazzle Software via Wyrd](http://maps.secondlife.com/secondlife/Wyrd/230/83/97)