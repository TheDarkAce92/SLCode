---
name: "Builders Buddy v1"
category: "example"
type: "example"
language: "LSL"
description: "This is a repost of the current Builder's Buddy scripts, as originally released on the prior LSL wiki. There are two scripts; One goes in a \"base\" prim, which is the piece that is moved/rotated/etc. The component script goes into each linked set that makes up the rest of the large build. In short, only one base script, many component scripts."
wiki_url: "https://wiki.secondlife.com/wiki/Builders_Buddy_v1"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

- 1 Help Documentation
- 2 Obligatory Copyright Notice
- 3 The Base Script
- 4 The Component Script
- 5 Change Log

This is a repost of the current Builder's Buddy scripts, as originally released on the prior LSL wiki.  There are two scripts; One goes in a "base" prim, which is the piece that is moved/rotated/etc.  The component script goes into each linked set that makes up the rest of the large build.  In short, only one base script, many component scripts.

**The most current "official" version of these scripts is 1.10.**



## Help Documentation

Complete Step-by-Step help is posted here: Builder's Buddy Help Document . The help document also includes a short quick end-user guide for you to distribute to end-users of your products.



## Obligatory Copyright Notice

There are only a few points here:

- Use this script as you wish, to modify, sell, etc.
- If you use this script in a for-sale product, please give credit to Newfie Pendragon as the creator of the script.
- If you wish to modify this script and release the changes for public use, please submit changes to Newfie Pendragon.  This is to ensure a consistent version numbering on releases, and to ensure changes are not wiped out in future releases.

## The Base Script

```lsl
///////////////////////////////////////////////////////////////////////////////
// Builders' Buddy 1.10 (Base Script)
// by Newfie Pendragon, 2006-2008
///////////////////////////////////////////////////////////////////////////////
//
// Script Purpose & Use
// Functions are dependent on the "component script"
//
// QUICK USE:
// - Drop this script in the Base.
// - Drop the "Component" Script in each building part.
// - Touch your Base, and choose RECORD
// - Take all building parts into inventory
// - Drag building parts from inventory into Base Prim
// - Touch your base and choose BUILD
//
// OTHER COMMANDS from the Touch menu
// - To reposition, move/rotate Base Prim choose POSITION
// - To lock into position (removes scripts) choose DONE
// - To delete building pieces: choose CLEAN
///////////////////////////////////////////////////////////////////////////////
// This script is copyrighted material, and has a few (minor) restrictions.
// For complete details, including a revision history, please see
//  http://wiki.secondlife.com/wiki/Builders_Buddy
///////////////////////////////////////////////////////////////////////////////

// Channel used by Base Prim to talk to Component Prims
// This channel must be the same one in the component script
// A negative channel is used because it elimited accidental activations
// by an Avatar talking on obscure channels
integer DefaultPRIMCHAN = -192567;     // Default channel to use
integer PRIMCHAN = DefaultPRIMCHAN;    // Channel used by Base Prim to talk to Component Prims;
                                       // ***THIS MUST MATCH IN BOTH SCRIPTS!***

//The UUID of the creator of the object
//Leave this as "" unless SL displays wrong name in object properties
key creatorUUID = "";

// Set to TRUE to allow group members to use the dialog menu
// Set to FALSE to disallow group members from using the dialog menu
integer ingroup = TRUE;

// Set to TRUE to delete piece from inventory when rezzed
// (WARNING) If set to FALSE, user will be able to rez multiple copies
integer deleteOnRez = FALSE;

// Allow non-creator to use CLEAN command?
// (WARNING) If set to TRUE, it is recommended to set
// deleteOnRez to FALSE, or user could lose entire building
integer allowClean = TRUE;

//When user selects CLEAN, delete the base prim too?
integer dieOnClean = FALSE;

// Set to TRUE to record piece's location based on sim
// coordinates instead of relationship to base prim
integer recordSimLocation = FALSE;

// Set to TRUE to rez all building pieces before positioning,
// or FALSE to do (slower?) one at a time
integer bulkBuild = TRUE;

//Set to FALSE if you dont want the script to say anything while 'working'
integer chatty = TRUE;

//How long to listen for a menu response before shutting down the listener
float fListenTime = 30.0;

//How often (in seconds) to perform any timed checks
float fTimerRate = 0.25;

//How long to sit still before exiting active mode
float fStoppedTime = 30.0;

//SL sometimes blocks rezzing to prevent "gray goo" attacks
//How long we wait (seconds) before we assume SL blocked our rez attempt
integer iRezWait = 10;

//Specify which Menu Options will be displayed
//FALSE will restrict full options to creator
//TRUE will offer full options to anyone
integer fullOptions = FALSE;

//Set to TRUE if you want ShapeGen channel support
// (Last 4 digits of channel affected)
integer SGCompatible = FALSE;

///////////////////////////////////////////////////////////////////////////////
//Part of KEYPAD CODE BY Andromeda Quonset....More added below in seevral places
list Menu2 = [ "-", "0","enter","7","8","9","4","5","6","1","2","3"];
string Input = "";
string Sign = "+";
string SignInput = " ";
string Caption = "Enter a number, include any leading 0's: ";

///////////////////////////////////////////////////////////////////////////////
// DO NOT EDIT BELOW THIS LINE.... NO.. NOT EVEN THEN
///////////////////////////////////////////////////////////////////////////////

//Name each option-these names will be your button names.
string optRecord = "Record";
string optReset = "Reset";
string optBuild = "Build";
string optPos = "Position";
string optClean = "Clean";
string optDone = "Done";
string optChannel = "Channel";

//Menu option descriptions
string descRecord = ": Record the position of all parts\n";
string descReset = ": Forgets the position of all parts\n";
string descBuild = ": Rez inv. items and position them\n";
string descPos = ": Reposition the parts to a new location\n";
string descClean = ": De-Rez all pieces\n";
string descDone = ": Remove all BB scripts and freeze parts in place.\n";
string descChannel = ": Change Channel used on base and parts.\n";

integer MENU_CHANNEL;
integer MENU2_CHANNEL;
integer MENU_HANDLE;
integer MENU2_HANDLE;
key agent;
key objectowner;
integer group;
string title = "";
list optionlist = [];
integer bMoving;
vector vLastPos;
rotation rLastRot;
integer bRezzing;
integer iListenTimeout = 0;
integer iLastRez = 0;
integer iRezIndex;

InvertSign()
{
    if(Sign == "+")
        Sign = "-";
    else
        Sign = "+";
}

//To avoid flooding the sim with a high rate of movements
//(and the resulting mass updates it will bring), we used
// a short throttle to limit ourselves
announce_moved()
{
    llRegionSay(PRIMCHAN, "MOVE " + llDumpList2String([ llGetPos(), llGetRot() ], "|"));
    llResetTime();        //Reset our throttle
    vLastPos = llGetPos();
    rLastRot = llGetRot();
    return;
}

rez_object()
{
    //Rez the object indicated by iRezIndex
    llRezObject(llGetInventoryName(INVENTORY_OBJECT, iRezIndex), llGetPos(), ZERO_VECTOR, llGetRot(), PRIMCHAN);
    iLastRez = llGetUnixTime();

    if(!bRezzing) {
        bRezzing = TRUE;
        //timer_on();
    }
}

post_rez_object()
{
    if ( creatorUUID != llGetOwner() ) {
        if(deleteOnRez) llRemoveInventory(llGetInventoryName(INVENTORY_OBJECT, iRezIndex));
    }
}

heard(integer channel, string name, key id, string message)
{
    if( channel == PRIMCHAN ) {
        if( message == "READYTOPOS" ) {
            //New prim ready to be positioned
            vector vThisPos = llGetPos();
            rotation rThisRot = llGetRot();
            llRegionSay(PRIMCHAN, "MOVESINGLE " + llDumpList2String([ vThisPos, rThisRot ], "|"));

        } else if( message == "ATDEST" ) {
            //Rez the next in the sequence (if any)
            iRezIndex--;
            if(iRezIndex >= 0) {
                //Attempt to rez it
                rez_object();
            } else {
                //We are done building, reset our listeners
                iLastRez = 0;
                bRezzing = FALSE;
                state reset_listeners;
            }
        }
        return;

    } else if( channel == MENU_CHANNEL ) {   //Process input from original menu
        if ( message == optRecord ) {
            PRIMCHAN = DefaultPRIMCHAN;
            llOwnerSay("Recording positions...");
            if(recordSimLocation) {
                //Location in sim
                llRegionSay(PRIMCHAN, "RECORDABS " + llDumpList2String([ llGetPos(), llGetRot() ], "|"));
            } else {
                //Location relative to base
                llRegionSay(PRIMCHAN, "RECORD " + llDumpList2String([ llGetPos(), llGetRot() ], "|"));
            }
            return;
        }
        if( message == optReset ) {
            llOwnerSay("Forgetting positions...");
            llShout(PRIMCHAN, "RESET");
            return;
        }
        if ( message == optBuild ) {
            if(chatty) llOwnerSay("Rezzing build pieces...");

            //If rezzing/positioning one at a time, we need
            // to listen for when they've reached their dest
            if(!bulkBuild) {
                llListen(PRIMCHAN, "", NULL_KEY, "READYTOPOS");
                llListen(PRIMCHAN, "", NULL_KEY, "ATDEST");
            }

            //Start rezzing, last piece first
            iRezIndex = llGetInventoryNumber(INVENTORY_OBJECT) - 1;
            rez_object();
            return;
        }
        if ( message == optPos ) {
            if(chatty) llOwnerSay("Positioning");
            vector vThisPos = llGetPos();
            rotation rThisRot = llGetRot();
            llRegionSay(PRIMCHAN, "MOVE " + llDumpList2String([ vThisPos, rThisRot ], "|"));
            return;
        }
        if ( message == optClean ) {
            llRegionSay(PRIMCHAN, "CLEAN");
            if(dieOnClean) llDie();
            return;
        }
        if ( message == optDone ) {
            llRegionSay(PRIMCHAN, "DONE");
            if(chatty) llOwnerSay("Removing Builder's Buddy scripts.");
            return;
        }
        if ( message == optChannel ) {
            Sign = "+"; //default is a positive number
            Input = "";
            llDialog( agent, Caption, Menu2, MENU2_CHANNEL );
        }

    } else if ( channel == MENU2_CHANNEL ) {    //process input from MENU2
        // if a valid choice was made, implement that choice if possible.
        // (llListFindList returns -1 if Choice is not in the menu list.)
        if ( llListFindList( Menu2, [ message ]) != -1 ) {
            if( llListFindList(["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"], [message]) != -1) {
                Input += message;
                SignInput = Sign + Input;
                llDialog( agent, Caption + SignInput, Menu2, MENU2_CHANNEL );

            } else if( message == "-" ) {
                InvertSign();
                SignInput = Sign + Input;
                llDialog( agent, Caption + SignInput, Menu2, MENU2_CHANNEL );

            } else if( message == "enter" ) {     //terminate input from menu2
                string CalcChan = Input;

            	//Apply ShapeGen compatibility?
            	if(SGCompatible) {
                    //new assign channel number, forcing last 4 digits to 0000
                	integer ChanSize = llStringLength(Input); //determine number of digits (chars)
	                if(ChanSize > 5) {
    	                CalcChan = llGetSubString(Input, 0, 4);    //Shorten to 5 digits
        	        }
                	CalcChan += "0000"; //append 0000
                    if(Sign == "-")
	                    CalcChan = Sign + CalcChan;
            	}
            	PRIMCHAN = (integer)CalcChan; //assign channel number
            	llOwnerSay("Channel set to " + (string)PRIMCHAN + ".");
            }

        } else {
            llDialog( agent, Caption, Menu2, MENU2_CHANNEL );
        }
    }
}

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
default {
    ///////////////////////////////////////////////////////////////////////////////
    changed(integer change) {
        if(change & CHANGED_OWNER)
        llResetScript();
    }

    ///////////////////////////////////////////////////////////////////////////////
    state_entry () {
        //Determine the creator UUID
        if(creatorUUID == "") creatorUUID = llGetCreator();

        //Use which menu?
        if (creatorUUID == llGetOwner() || fullOptions) {
            //Display all options
            optionlist = [optPos, optClean, optDone, optRecord, optReset, optBuild, optChannel];
            title = optRecord + descRecord;
            title += optReset + descReset;
            title += optBuild + descBuild;
            title += optPos + descPos;
            title += optClean + descClean;
            title += optDone + descDone;
            title += optChannel + descChannel;

        } else {
            //Display limited options
            if(allowClean) {
                optionlist = [optBuild, optPos, optClean, optDone];
                title = optBuild + descBuild;
                title += optPos + descPos;
                title += optClean + descClean;
                title += optDone + descDone;
            } else {
                optionlist = [optBuild, optPos, optDone];
                title = optBuild + descBuild;
                title += optPos + descPos;
                title += optDone + descDone;
            }
        }

        //Record our position
        vLastPos = llGetPos();
        rLastRot = llGetRot();

        llSetTimerEvent(fTimerRate);
    }

    ///////////////////////////////////////////////////////////////////////////////
    touch_start (integer total_number) {
        group = llDetectedGroup(0); // Is the Agent in the objowners group?
        agent = llDetectedKey(0); // Agent's key
        objectowner = llGetOwner(); // objowners key
        // is the Agent = the owner OR is the agent in the owners group
        if ( (objectowner == agent) || ( group && ingroup )  )  {
            iListenTimeout = llGetUnixTime() + llFloor(fListenTime);
            MENU_CHANNEL = llFloor(llFrand(-99999.0 - -100));
            MENU2_CHANNEL = MENU_CHANNEL + 1;
            MENU_HANDLE = llListen(MENU_CHANNEL,"","","");
            MENU2_HANDLE = llListen(MENU2_CHANNEL,"","","");
            if ( creatorUUID == llGetOwner() || fullOptions) {
                llDialog(agent,title + "Now on Channel " + (string)PRIMCHAN, optionlist, MENU_CHANNEL); //display channel number if authorized
            } else {
                llDialog(agent, title, optionlist, MENU_CHANNEL);
            }
            //timer_on();
        }
    }

    ///////////////////////////////////////////////////////////////////////////////
    listen(integer channel, string name, key id, string message) {
    	heard(channel, name, id, message);
    	return;
    }

    ///////////////////////////////////////////////////////////////////////////////
    moving_start()
    {
        if( !bMoving )
        {
            bMoving = TRUE;
            //timer_on();
            announce_moved();
        }
    }

    ///////////////////////////////////////////////////////////////////////////////
    object_rez(key id) {
        //The object rezzed, perform any post-rez processing
        post_rez_object();

        //Rezzing it all before moving?
        if(bulkBuild) {
            //Move on to the next object
            //Loop through backwards (safety precaution in case of inventory change)
            iRezIndex--;
            if(iRezIndex >= 0) {
                //Attempt to rez it
                rez_object();

            } else {
                //Rezzing complete, now positioning
                iLastRez = 0;
                bRezzing = FALSE;
                if(chatty) llOwnerSay("Positioning");
                llRegionSay(PRIMCHAN, "MOVE " + llDumpList2String([ llGetPos(), llGetRot() ], "|"));
            }
        }
    }

    ///////////////////////////////////////////////////////////////////////////////
    timer() {
        //Did we change position/rotation?
        if( (llGetRot() != rLastRot) || (llGetPos() != vLastPos) )
        {
            if( llGetTime() > fTimerRate ) {
                announce_moved();
            }
        }

        //Are we rezzing?
        if(bRezzing) {
            //Did the last one take too long?
            if((llGetUnixTime() - iLastRez) >= iRezWait) {
                //Yes, retry it
                if(chatty) llOwnerSay("Reattempting rez of most recent piece");
                rez_object();
            }
        }

        //Open listener?
        if( iListenTimeout != 0 )
        {
            //Past our close timeout?
            if( iListenTimeout <= llGetUnixTime() )
            {
                iListenTimeout = 0;
                llListenRemove(MENU_HANDLE);
            }
        }
    }

    ///////////////////////////////////////////////////////////////////////////////
    on_rez(integer iStart)
    {
        //Reset ourselves
        llResetScript();
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

## The Component Script

```lsl
///////////////////////////////////////////////////////////////////////////////
// Builders' Buddy 1.10 (Component Script)
// by Newfie Pendragon, 2006-2008
///////////////////////////////////////////////////////////////////////////////
//
// Script Purpose & Use
// Functions are dependent on the "component script"
//
// QUICK USE:
// - Drop this script in the Base.
// - Drop the "Component" Script in each building part.
// - Touch your Base, and choose RECORD
// - Take all building parts into inventory
// - Drag building parts from inventory into Base Prim
// - Touch your base and choose BUILD
//
// OTHER COMMANDS from the Touch menu
// - To reposition, move/rotate Base Prim choose POSITION
// - To lock into position (removes scripts) choose DONE
// - To delete building pieces: choose CLEAN
///////////////////////////////////////////////////////////////////////////////
// This script is copyrighted material, and has a few (minor) restrictions.
// For complete details, including a revision history, please see
//  http://wiki.secondlife.com/wiki/Builders_Buddy
///////////////////////////////////////////////////////////////////////////////

//////////////////////////////////////////////////////////////////////////////////////////
// Configurable Settings
float fTimerInterval = 0.25;        // Time in seconds between movement 'ticks'
integer DefaultChannel = -192567; // Andromeda Quonset's default channel
integer PRIMCHAN = DefaultChannel;  // Channel used by Base Prim to talk to Component Prims;
                                    // ***THIS MUST MATCH IN BOTH SCRIPTS!***

//////////////////////////////////////////////////////////////////////////////////////////
// Runtime Variables (Dont need to change below here unless making a derivative)
vector vOffset;
rotation rRotation;
integer bNeedMove;
vector vDestPos;
rotation rDestRot;
integer bMovingSingle = FALSE;
integer bAbsolute = FALSE;
integer bRecorded = FALSE;

////////////////////////////////////////////////////////////////////////////////
string first_word(string In_String, string Token)
{
    //This routine searches for the first word in a string,
    // and returns it.  If no word boundary found, returns
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
    // an empty string.
    if( Token == "" ) Token = " ";

    integer pos = llSubStringIndex(In_String, Token);

    //Found it?
    if( pos >= 1 )
        return llGetSubString(In_String, pos + 1, llStringLength(In_String));
    else
        return "";
}

////////////////////////////////////////////////////////////////////////////////
do_move()
{
    integer i = 0;
    vector vLastPos = ZERO_VECTOR;
    while( (i < 5) && (llGetPos() != vDestPos) )
    {
        list lParams = [];

        //If we're not there....
        if( llGetPos() != vDestPos )
        {
            //We may be stuck on the ground...
            //Did we move at all compared to last loop?
            if( llGetPos() == vLastPos )
            {
                //Yep, stuck...move straight up 10m (attempt to dislodge)
                lParams = [ PRIM_POSITION, llGetPos() + <0, 0, 10.0> ];
                //llSetPos(llGetPos() + <0, 0, 10.0>);
            } else {
                //Record our spot for 'stuck' detection
                vLastPos = llGetPos();
            }
        }

        //Try to move to destination
        //Upgraded to attempt to use the llSetPrimitiveParams fast-move hack
        //(Newfie, June 2006)
        integer iHops = llAbs(llCeil(llVecDist(llGetPos(), vDestPos) / 10.0));
        integer x;
        for( x = 0; x < iHops; x++ ) {
            lParams += [ PRIM_POSITION, vDestPos ];
        }
        llSetPrimitiveParams(lParams);
        //llSleep(0.1);
        i++;
    }

    //Set rotation
    llSetRot(rDestRot);
}

start_move(string sText, key kID)
{
    //Don't move if we've not yet recorded a position
    if( !bRecorded ) return;

    //Also ignore commands from bases with a different owner than us
    //(Anti-hacking measure)
    if( llGetOwner() != llGetOwnerKey(kID) ) return;

    //Calculate our destination position relative to base?
    if(!bAbsolute) {
        //Relative position
        //Calculate our destination position
        sText = other_words(sText, " ");
        list lParams = llParseString2List(sText, [ "|" ], []);
        vector vBase = (vector)llList2String(lParams, 0);
        rotation rBase = (rotation)llList2String(lParams, 1);

        vDestPos = (vOffset * rBase) + vBase;
        rDestRot = rRotation * rBase;
    } else {
        //Sim position
        vDestPos = vOffset;
        rDestRot = rRotation;
    }

    //Make sure our calculated position is within the sim
    if(vDestPos.x < 0.0) vDestPos.x = 0.0;
    if(vDestPos.x > 255.0) vDestPos.x = 255.0;
    if(vDestPos.y < 0.0) vDestPos.y = 0.0;
    if(vDestPos.y > 255.0) vDestPos.y = 255.0;
    if(vDestPos.z > 4096.0) vDestPos.x = 4096.0;

    //Turn on our timer to perform the move?
    if( !bNeedMove )
    {
        llSetTimerEvent(fTimerInterval);
        bNeedMove = TRUE;
    }
    return;
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
        llListen(PRIMCHAN, "", NULL_KEY, "");
        llRegionSay(PRIMCHAN, "READYTOPOS");
    }

    //////////////////////////////////////////////////////////////////////////////////////////
    on_rez(integer iStart)
    {
        //Set the channel to what's specified
        if( iStart != 0 )
        {
            PRIMCHAN = iStart;
            state reset_listeners;
        }
    }

    //////////////////////////////////////////////////////////////////////////////////////////
    listen(integer iChan, string sName, key kID, string sText)
    {
        string sCmd = llToUpper(first_word(sText, " "));

        if( sCmd == "RECORD" )
        {
            //Record position relative to base prim
            sText = other_words(sText, " ");
            list lParams = llParseString2List(sText, [ "|" ], []);
            vector vBase = (vector)llList2String(lParams, 0);
            rotation rBase = (rotation)llList2String(lParams, 1);

            vOffset = (llGetPos() - vBase) / rBase;
            rRotation = llGetRot() / rBase;
            bAbsolute = FALSE;
            bRecorded = TRUE;
            llOwnerSay("Recorded position.");
            return;
        }

        if( sCmd == "RECORDABS" )
        {
            //Record absolute position
            rRotation = llGetRot();
            vOffset = llGetPos();
            bAbsolute = TRUE;
            bRecorded = TRUE;
            llOwnerSay("Recorded sim position.");
            return;
        }

        //////////////////////////////////////////////////////////////////////////////////////////
        if( sCmd == "MOVE" )
        {
            start_move(sText, kID);
            return;
        }

        if( sCmd == "MOVESINGLE" )
        {
            //If we haven't gotten this before, position ourselves
            if(!bMovingSingle) {
                //Record that we are a single-prim move
                bMovingSingle = TRUE;

                //Now move it
                start_move(sText, kID);
                return;
            }
        }

        //////////////////////////////////////////////////////////////////////////////////////////
        if( sCmd == "DONE" )
        {
            //We are done, remove script
            llRemoveInventory(llGetScriptName());
            return;
        }

        //////////////////////////////////////////////////////////////////////////////////////////
        if( sCmd == "CLEAN" )
        {
            //Clean up
            llDie();
            return;
        }

        //////////////////////////////////////////////////////////////////////////////////////////
        if( sCmd == "RESET" )
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
        if( bNeedMove )
        {
            //Perform the move and clean up
            do_move();

            //If single-prim move, announce to base we're done
            if(bMovingSingle) {
                llRegionSay(PRIMCHAN, "ATDEST");
            }

            //Done moving
            bNeedMove = FALSE;
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

## Change Log

- v1.0 - March 28, 2006 - Newfie Pendragon

  - Original Version

- v1.1 - March 31, 2006 - Kalidor Lazarno

  - Added a Dialog Engine to the base script

- v1.5 - June 12, 2006 - Androclese Antonelli

  - Base Script:

  - Added a random number generator to the dialog engine to eliminate problems with multiple BB boxes cross-talking
  - Added a timer to the listen command to put it asleep after 10sec.
  - Added a Menu Description
  - Added a "creator" flag so the owner could use the same object with full menu options and only a single flag change
  - Added an "ingroup" flag to enable/disable the same group use function
  - Non-Admin usage cleans the inventory items as they spawn

- v1.6 - 20060624 - Newfie Pendragon

  - Base Script:

  - Added active repositioning (building moves as the base piece moves)
  - Added "Reset" Option to unlink parts from base temporarily
  - Modified creator flag to automatically set based if owner is creator
  - Minor changes to improve code readability (for those learning LSL)
  - Component Script:

  - Added active repositioning (pieces move as the base piece moves)
  - Pieces use WarpPos technique to instantanetly move large distances
  - Pieces no longer move until the the "Record" option has been used at least once
  - Pieces will not move if base is not same owner as the pieces
  - Pieces no longer 'bounce' when hitting the ground

- v1.7  - August 21, 2006

  - Component Script:

  - Correction for non-zero rotation (thanks Ed44 Gupta!)

- v1.8 - 20070429 - Newfie Pendragon

  - Base Script:

  - Added a variable to allow a user to tweak how long a listener is open, and changed the default to 30 seconds.

- v1.9 - 20070630 - Newfie Pendragon

  - Base Script:

  - Changed to use llRegionSay - no more 96m max distance (same sim)
  - Changed rez sequence to be less affected by lag/gray goo fence
  - Timer always on, less code/more reliable
  - Component Script:

  - Added check to keep within sim edges

- v1.10 - February 9, 2008

  - Base Script:

  - New setting **creatorUUID** - allows user to explicitly state creator of object, in case it differs from base prim
  - New setting **deleteOnRez** - Determines if script is to delete building prims from inventory as they are rezzed (setting to FALSE means building can be rezzed multiple times)
  - New setting **allowClean** - Determines if end user can use the 'CLEAN' menu option
  - New setting **dieOnClean** - Include base prim when cleaning
  - New setting **recordSimLocation** - when TRUE using 'RECORD' menu option, location is in exact sim coordinates instead of relative to base prim.
  - New setting **bulkBuild** - when set to FALSE, will rez/position each prim individually, ala Rez-Faux/etc
  - Bumped lag-wait timeout to 10 seconds (original was 3 seconds, way too short)
  - New setting **SGCompatible** - set to TRUE to enable ShapeGen support (see contributions by Andromeda Quonset)
  - Contributions by Huney Jewell:

  - Added configurable constant to determine, which Menu Options will be displayed
  - Menu Option 'Clean' now also deletes the prim which contains this script
  - Contributions by Andromeda Quonset:

  - Added Channel command to dialog box
  - Added second dialog box for inputting channel
  - Added changing to default channel when invoking RECORD function
  - Changed channel assignment on-rez, default channel, so ends with 0000
  - Component Script:

  - Added logic to recognize sim-exact vs. relative position recording.
  - Added logic to aid in single prim rez/move feature