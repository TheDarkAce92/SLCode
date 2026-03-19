---
name: "Deed Tools"
category: "example"
type: "example"
language: "LSL"
description: "This script allows you some limited control over objects onces they have been deeded to group. This is helpful if you do not wish to re-create the object, or you do not have permissions to return deeded objects."
wiki_url: "https://wiki.secondlife.com/wiki/Deed_Tools"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

- 1 Description
- 2 Directions
- 3 Syntax
- 4 Commands

  - 4.1 Help
  - 4.2 Move/Rotation
  - 4.3 Kill
  - 4.4 Ghost
  - 4.5 Pin
  - 4.6 Drop
  - 4.7 Reset
  - 4.8 Run
  - 4.9 Stop
  - 4.10 Remove
- 5 Example Commands
- 6 DeedTools Script

## Description

This script allows you some limited control over objects onces they have been deeded to group.  This is helpful if you do not wish to re-create the object, or you do not have permissions to return deeded objects.

## Directions

Put the following script in the root prim of the item you are about to Deed to Group.**Note:** Make sure you are the Creator of the object you are deeding.

## Syntax

/1**<Name>** **<Command>** **<Parameters...>**

## Commands

### Help

Command: **help****Lists the commands via Instant Message. ### Move/Rotation Command: move** *<Position>***Command: rmove** *<Relative Position>***Command: rot** *<Rotation>***Command: rrot** *<Relative Rotation>***These commands move and rotate the Deeded object. Positions are given in region coordinates, rotation is in Degrees. The rmove** and **rrot** commands move and rotate the prim relative to its current position and rotation.

### Kill

Command: **kill****Instantly Kills the Deeded Object ### Ghost Command: ghost** *<Name/UUID>***The deeded object will follow the object specified either by Name or UUID. Useful for repositioning the Deeded Object. Command: unghost'**
Stops the Deeded object from following the other object.**Note:** If the other object is deleted this command is auto-ran.

### Pin

Command: **pin** *<Number>***Sets the Remote Load Script Pin to <Number>. Allows other scripts to load running scripts into the deeded object. Command: unpin****Disables remotely loaded scripts. ### Drop Command: drop****Allows items to be dropped into the Deeded object's inventory. Command: undrop****Disables items from being dropped into the Deeded object's inventory ### Reset Command: reset** *<Script>***Resets the <Script> inside the Deeded object. ### Run Command: run** *<Script>***Set the <Script> inside the Deeded object to Running. ### Stop Command: stop** *<Script>***Stops the <Script> inside the Deeded object. ### Remove Command: remove** *<Inventory>*

Deletes <Inventory> inside the Deeded object.

## Example Commands

```lsl
/1MyObject kill
/1MyObject ghost AnotherObject
/1MyObject reset SomeScript
/1MyObject rot <45,90,270>
```

## DeedTools Script

```lsl
integer CHANNEL = 1;
key gGhostPrim;
default
{
    state_entry()
    {
        llListen(CHANNEL,"",llGetCreator(),"");
        llInstantMessage(llGetCreator(),"For help, type: /" + (string)CHANNEL + llGetObjectName() + " help\n");
    }
    listen(integer channel, string name, key id, string msg)
    {
        string name = llToLower(llGetObjectName());

        if( llSubStringIndex(llToLower(msg),name) != 0) return;
        msg = llStringTrim(llGetSubString(msg,llStringLength(name),-1),STRING_TRIM);

        list params = llParseString2List(msg,[" "],[]);
        string command = llToLower(llList2String(params,0));
        string param = llDumpList2String(llDeleteSubList(params,0,0)," ");

        params = [];

        if( command == "help" )
        {
            llInstantMessage(id,"\nSyntax: /"+ (string)CHANNEL + llGetObjectName() + "

\n\n" +
                "kill: Kills the object\n" +
                "ghost : Follow the object and rotate along with in\n" +
                "unghost: Stop following an object\n" +
                "pin #: Sets script loading pin to <#>\n" +
                "unpin: Removes loading script pin"
            );
            llInstantMessage(id,"\n"+
                "drop: Allows objects to be dropped into the prim\n" +
                "undrop: Prevents objects from being dropped into the prim\n" +
                "reset : Resets the script named \n" +
                "run : Starts the script named \n" +
                "stop : Stopts the script named "
            );
        }

        else if( command == "kill" )
        {
            llInstantMessage(id,"Killing " + llGetObjectName() );
            llDie();
        }

        else if( command == "move" || command == "rmove")
        {
            vector p = (vector)param;
            if( command == "rmove" ) p += llGetPos();
            if( llVecMag( p - llGetPos() ) > 100 )
            {
                llInstantMessage(id,"Unable to move: Distance is too great");
                return;
            }
            while( llGetPos() != p ) {llSetPos(p);}
        }

        else if( command == "rot" || command == "rrot" )
        {
            rotation r = llEuler2Rot((vector)param*DEG_TO_RAD);
            if( command == "rrot" ) r = llGetRot() * r;

            llSetRot(r);
        }
        else if( command == "pin" )
        {
            llSetRemoteScriptAccessPin((integer)param);
        }
        else if( command == "unpin" )
        {
            llSetRemoteScriptAccessPin(0);
        }
        else if( command == "drop" ) llAllowInventoryDrop(TRUE);
        else if( command == "undrop") llAllowInventoryDrop(FALSE);

        else if( command == "reset" ) llResetOtherScript(param);
        else if( command == "run" ) llSetScriptState(param,TRUE);
        else if( command == "stop") llSetScriptState(param,FALSE);

        else if(command == "remove") {
            if( llGetInventoryType(param) != INVENTORY_NONE) {
                llRemoveInventory(param);
            }
        }

        else if( command == "ghost" )
        {
            gGhostPrim = param;
            if( llGetOwnerKey(param) == NULL_KEY )
            {
                llSensor(gGhostPrim,"",ACTIVE|PASSIVE,20.0,PI);
            } else {
                llSetTimerEvent(1.0);
            }
        }
        else if( command == "unghost" )
        {
            llSetTimerEvent(0.0);
        }
    }
    sensor(integer i)
    {
        gGhostPrim = llDetectedKey(0);
        llSetTimerEvent(1.0);
    }
    no_sensor()
    {
        llInstantMessage(llGetCreator(),(string)gGhostPrim + " not found");
    }

    timer()
    {
        list p = llGetObjectDetails(gGhostPrim,[OBJECT_POS,OBJECT_ROT]);
        if( llGetListLength(p) == 0 )
        {
            llSetTimerEvent(0.0);
            llInstantMessage(llGetCreator(),"Object Lost..");
        } else {
            llSetPos(llList2Vector(p,0));
            llSetRot(llList2Rot(p,1));
        }
    }
}
```