---
name: "Wiki3DBuilder"
category: "example"
type: "example"
language: "LSL"
description: "Here a sample of using this tool (v0.1) by a Sloodle fan (Giancarla Loon) for teaching sloodle basics for Teachers:"
wiki_url: "https://wiki.secondlife.com/wiki/Wiki3DBuilder"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

- 1 Introduction

  - 1.1 Disclaimer
  - 1.2 QuickStart
  - 1.3 What it is
  - 1.4 How it works
  - 1.5 Internal architecture
- 2 llSetPin to put in "nodo" object
- 3 The Main Script
- 4 Having a copy from XStreetsl

## Introduction

Here a sample of using this tool (v0.1) by a Sloodle fan (Giancarla Loon) for teaching sloodle basics for Teachers:

(See also the enhanced version v1 Wiki3DBuilder1.0 with significative enhancements. I'm leaving this version on this wiki since somebody did like this version even with its limitations)

This had been built following the ideas (but not the code) of similar object "SpatialMap.org (MindMap 3D) v1.0.18" written by Jonny Bee Cioc and Vision Raymaker which was under a CC by,nc,sa license itself. You can get this object inworld free of charge (under the conditions of CC license) IMming me.
I'm NO MORE distributing anything on XStreetSL after the new policies in 2009 where Lindend made impossible to distribute freebies)

### Disclaimer

This is just a POC (Proof of Concept) and it is meant as a very alpha stage prototype I developed during last week.
It is not meant to satisfy security and high level coding standards.

In particular the following things are possibly dangerous and might be rethought and made it professionally:

- Using llSetPin using key2int is not good (final solution might have another copy of main script) which BTW will make the rezzing much rapid
- Using key2int to communicate with the rezzed cubes is to say the least quite "optimistic" and might lead to notworking and malfunctioning objects
- Need more sophisticated ways to Lock the object, to Link it in a unique linkset to simplify inventory operations and to avoid that everybody can hack or destroy the mindmap thing

### QuickStart

- Build a cube, name it "nodo" and put inside the llSetPin script
- Build another cube, name it Wiki3D_Builder and put inside its content the "nodo" and the main script
- It should work just clicking on this starting cube (try to rez other cubes, to change the type, form etc).

### What it is

A tool that helps a user to build rich 3D wiki architectures made up of NODES connected with particles BEAMS

Each NODE can be customized by changing its NAME, COLOR, SIZE, and FORM

Each NODE can contain:

1. 1 Notecard
1. 1 Landmark
1. 1 Object
1. 1 Script
1. 1 Texture
1. URL that can be given

The network is completely open to the participation of a group of people who can change the network, the position of each node, and freely add or remove portions of the graph.

Being a Wiki there is no limitation on who can do what. If you don't want that the work can be changed further, please set to NOT RUNNING the scripts. To save the mindmap you need to select all the nodes and manually link them together or take into inventory as an aggregate (a coalesced object).




### How it works

Initially you have a NODE (i.e., a cube) which must be touched to start the process

- Touch object to see a menu with these options: color, name, size, content, move, rez
- Select "color" to enter a color on the local chat
- Select "name" to enter a name on the local chat
- Select "size" to enter a size on the local chat
- Select "rez" to rez a new node; when choosing this option, you must touch one of the faces of the cube and a new node will be rezzed 50cm on that direction.
- Select "move" and then touch a face to pull the node towards in direction
- Any user can move objects, textures and so from their inventory to a node (CTRL-Dragging them).
- **Contents:** Only one type of inventory item can be in the node at one time, and that content can be given to whom is asking for content
- Changing the texture will also change the texture of the node



### Internal architecture

This is done in ONLY one script named "Main Script" and an internal object named "nodo" containing a llSetPin script.
The llSetPin is just a way for setting the pin to a number depending on the Owner of the object so it is NOT easy to
hack.
The "Main Script" is implementing a quite interesting mechanism for dealing with "multi-threading", i.e. multiple
avatars touching the object at the same time. This is accomplished using an Array of RECORDs representing
the waiting avatars and what they were waiting for. So listen(), touch(), and other events can query this QUEUE
and understand what is to be made next.
This also allows for an interesting handling of MULTI MENU
A part from this the rest is relatively simple, except for the communication between the various nodes.

- A node communicates with its children for example to propagate the DELETE message
- A node communicates with its parent to emit the particles connector
- A node receives messages from its parent to llDie and with alert when other related objects are changing UUID        the latter happens when objects are re-rezzed from inventory

To accomplish this object listens to a
channelPublic (taken from Owner key) for transmitting and receiving changes of UUIDs,
or to channelPrivate (taken from the object key) for receiving commands from parent

## llSetPin to put in "nodo" object

This is NOT really needed you can instead put a copy of main script in inner object.
I used this technique to avoid changing every time the internal script whenever I update it.



```lsl
// This will convert an id to an integer same id => same key
// used to easily set up a not easy way to deposit scripts with a PIN
integer key2int(key id)
{
    string idstring = (string)id;
    integer ret = 0;
    integer i = 0;
    for(; i < llStringLength(idstring); ++i)
    {
        ret = ret * 10 + (((integer)("0x8"+llGetSubString(idstring, i, i)) - 2) % 17);
    }
    return ret;
}

default
{
    state_entry()
    {
        llSetRemoteScriptAccessPin(key2int(llGetOwner()));
    }
    changed(integer change)
    {
        llSetRemoteScriptAccessPin(key2int(llGetOwner()));
    }
}
```

## The Main Script

```lsl
// This source is "OpenSource"
// It can be freely used under the following CC license
// by: you need to state it was originally written by Salahzar Stenvaag
// nc: you cannot use for commercial products
// sa: you can extend it but you must redistribute it under the same license
// This software is specifically written to be used by GPLv3 licenced software

// Wiki3DBuilder (MindMap)
// This had been built following the ideas (but not the code) of similar
// object "SpatialMap.org (MindMap 3D) v1.0.18" written by Jonny Bee Cioc and Vision Raymaker
// which was under a CC by,nc,sa license itself

// What it is
// ==========
// You can build rich 3D wiki architectures made up of NODES, connected with particles BEANS
// Each NODE can be customized changing its NAME, COLOR, SIZE, FORM and possibly inserting in it
// 1 Notecard, 1 Landmark, 1 Object, 1 Script, 1 Texture, URL that can be given
// The network is completely open to the participation of a group of people who can change the
// newtwork, the position of each node, and freely add or remove portions of the graph

// Being a Wiki there is no limitation on who can do what. If you don't want that the work can be furtherly
// changed please set to NOT RUNNING the scripts. To save the mindmap you need to select all the nodes
// and manually link them together or take in the inventory as aggregate


// How it works
// Initially you have a NODE, i.e. a cube which must be touched to start the process
// Touching it you have a menu specifying color, name, size, content, move, rez, ...
// * clicking on name you can type the name on the local chat and other menu for resizing, recoloring...
// * clicking rez you rez a new node when choosing this option you must touch one of the faces of the cube:
//   new node will be rezzed 50cm on that direction.
// * similarly applies to move clicking on a face will pull the node towards that direction
// * content. Everybody can move objects, textures and so from their inventory to a node (CTRL-Dragging them).
//   at each moment only one type of object can be in the node and it can be given to whom is asking for content
//   changing the texture will also change the texture of the node

// Internal architecture
// This is done in ONLY one script named "Salahzar Map" and an internal object named "nodo" containing a llSetPin script.
// The llSetPin is just a way for setting the pin to a number depending on the Owner of the object so it is NOT easy to
// hack.
// The "Salahzar Map" is implementing a quite interesting mechanism for dealing with "multi-threading", i.e. multiple
// avatars touching the object at the same time. This is accomplished using an Array of RECORDs representing
// the waiting avatars and what they were waiting for. So listen(), touch(), and other events can query this QUEUE
// and understand what is to be made next.
// This also allows for an interesting handling of MULTI MENU
// A part from this the rest is relatively simple, except for the communication between the various nodes.
// A node communicates with its children for example to propagate the DELETE message
// A node communicates with its parent to emit the particles connector
// A node receives messages from its parent to llDie and with alert when other related objects are changing UUID
//        the latter happens when objects are re-rezzed from inventory
// To accomplish this object listens to a
// channelPublic (taken from Owner key) for transmitting and receiving changes of UUIDs,
// or to channelPrivate (taken from the object key) for receiving commands from parent

// TODOLIST:

// implement LINKSET all this can be very tricky
// implement UNLINK (remove particles)

// CUSTOMIZABLE PARAMETERS
integer TIMEOUT=30;       // menu will be obsolesced after this period of time
integer CLEANTIMERSEC=10; // timer will run once every this period of time for cleaning timers
integer DEBUG=0;          // 2 maximum level
// END OF CUSTOMIZABLE PARAMETERS

string url=""; // url associated with this node

// 0) General utility functions

// debug this string only if DEBUG is at least 1
debug(string str)
{
    if(DEBUG>=1)llOwnerSay(str);
}

// trace the string only if DEBUG is 2
trace(string str)
{
    if(DEBUG>=2)llOwnerSay(str);
}
// will put on the hover string
notify(string str)
{
    llSetText(str,<1,1,1>,1);
}

// 1) RECORD STACK
// handling. We keep a "queue" or RECORDS for understanding
// multi-avatar touching and remember prompts and menu and let them expire
//

integer STRIDE=6; // we hold 6 field in the waiting list
list waiting=[]; // this is where we actually keep the queue

// this will be the RECORD with the 6 fields
string theType;     // it is something like MENUxxxx or PROMPTyyyy
key theAv;          // which avatar is waiting
integer theTime;    // when the RECORD has been stacked
integer theMenu;    // the menu handle so we can clean up it
integer theChannel; // which channel
string theRest;     // some further information on this RECORD (prompt string?)

// count how many RECORDS are being stacked waiting to be served
integer howManyRecords()
{
    integer ret= llGetListLength(waiting)/STRIDE;
    trace("howManyRecords returning: "+(string)ret);
    return ret;
}
// load the record in theXXX variables to ease handling of it
integer loadTheRecord(integer index)
{
    if(index>=0)
    {
       theType=llList2String(waiting,index);
       theAv=llList2Key(waiting,index+1);
       theTime=llList2Integer(waiting,index+2);
       theMenu=llList2Integer(waiting,index+3);
       theChannel=llList2Integer(waiting,index+4);
       theRest=llList2String(waiting,index+5);
       debug("Loading the record: \n   type: "+theType+"\n   Av: "+(string)theAv
+"\n   time: "+(string)theTime+"\n   menu: "+(string)theMenu+"\n   channel:"
+(string)theChannel+"\n   rest:"+theRest);
       return index;
    }
    else
    {
        theType="";
        theAv=NULL_KEY;
        theTime=-1;
        theMenu=-1;
        theChannel=-1;
        theRest="";
        trace("No record returned");
        return -1;
    }
}

// look in our stack for this avatar return the index AND loading in theXXX variables

integer findWaitingAvatar(key av)
{
    debug("Looking for avatar: "+(string)av);
   integer pos=llListFindList(waiting,[av]);
   integer index;
   if(~pos) index=pos-1; else index=-1;
   return loadTheRecord(index);
}
// change the time of the event at position index
updateTimer(integer index)
{
    if(index<0 || index>=howManyRecords()) return;
    trace("Updating timer for index: "+(string)index);
    integer posTime=index*STRIDE+2;
    waiting=llListReplaceList(waiting,[ llGetUnixTime() ], posTime, posTime);
}

// remove a record
integer deleteRecord(integer index)
{
    if(index>=0 && index [c]
// useful to understan which elements have been added deleted in the inventory
list diffList(list ls1, list ls2)
{
    //llSay(0,"ls1: "+llList2CSV(ls1)+" ls2:"+llList2CSV(ls2));
    list ret=[];
    integer i=0;
    for(i=0;iAdded "+llList2CSV(added));
    //llSay(0,"==>Removed "+llList2CSV(removed));

    // now check for each added if there was a duplicate in currentInventory
    for(i=0;i,
                        PSYS_PART_END_COLOR, <0.75,0,0>,
                        PSYS_PART_START_SCALE,<0.051,.2,FALSE>,
                        PSYS_PART_END_SCALE,<0.2,.1,FALSE>,
                        PSYS_SRC_PATTERN, pattern,
                        PSYS_SRC_BURST_RATE,.1,
                        //PSYS_SRC_ACCEL, <0,0,0>,
                        PSYS_SRC_BURST_PART_COUNT,8,
                        //PSYS_SRC_BURST_RADIUS,0.0,
                        PSYS_SRC_BURST_SPEED_MIN,0.0,
                        PSYS_SRC_BURST_SPEED_MAX,5.0,
                        PSYS_SRC_TARGET_KEY,target,
                        PSYS_SRC_ANGLE_BEGIN,0.0,
                        PSYS_SRC_ANGLE_END,0.0,
                        PSYS_SRC_OMEGA, <0,0,0>,
                        PSYS_SRC_MAX_AGE, 0.0,
                        //PSYS_SRC_TEXTURE, TEXTURE_BLANK,
                        PSYS_PART_START_ALPHA, 1.0,
                        PSYS_PART_END_ALPHA, 0.5
                            ]);


}
// 4) This will convert an id to an integer same id => same key
// used to easily set up a not easy way to deposit scripts with a PIN
integer key2int(key id)
{
    string idstring = (string)id;
    integer ret = 0;
    integer i = 0;
    for(; i < llStringLength(idstring); ++i)
    {
        ret = ret * 10 + (((integer)("0x8"+llGetSubString(idstring, i, i)) - 2) % 17);
    }
    return ret;
}

integer isroot=TRUE; // are we the MAIN object? Useful to avoid being deleted
list children=[]; // will keep the keys of ALL depending children

// 5) propagate message to all children
propagate(string message)
{
    debug("Received message propagating to children: "+llList2CSV(children));
    // received a message from my parent
    // propagate message to my children
    integer i;
    for(i=0;i TIMEOUT )
            {
                debug("Removing listener for "+llKey2Name(theAv));
                // if we were on  particular menu should also delete the
                llListenRemove(theMenu);
                deleteRecord(i);

                // if timeout something related to the detected avatar need to remove from list
                if(detected_key==theAv) remove_detected();

            }
        }
        //debug("List in timer exit: "+llList2CSV(waiting));
    }


    // main menu listening for waiting avatars
    // we answer only to
    touch_start(integer total_number)
    {
        integer i;
        for(i=0;i=0)
            {
                debug("Has already a menu waiting");
                // we have a menu for this avatar.. Check if we have it in detected_key
                // in such case we allow touching for detecting
                if(av==detected_key)
                {
                    trace("We have a detected_key for this avatar  type:"+detected_type);
                    // handle this event
                    if(detected_type=="DETECTMOVE")
                    {
                        debug("Moving the prim");
                        llSetPos(llGetPos()+llDetectedTouchNormal(i)*0.2);
                    }

                   if(detected_type=="DETECTPOSREZ")
                   {
                        debug("rezzing a new cube");
                        vector posrez=llDetectedTouchNormal(i);
                        llRezAtRoot("nodo",llGetPos()+posrez,ZERO_VECTOR,ZERO_ROTATION,1);
                        // execution is going on at rez_object

                    }
                    //upgrade time for this event extend it so that timer won't remove it for next 60 secs
                    updateTimer(index);

                    // do NOT consume this event will be ended by ctimeout
                    return;
                }

                // touch this when avatar has already a queue, will remove the queue
                deleteRecord(index);

                // informing the avatar the menu has been reset
                llInstantMessage(av,"Removing pending menu/promt");
                return;
            }

            // avatar hasn't any pending menu so start with main menu
            // start the initial menu
            addMenu("MENUMAIN",av,"Main menu:
DELETE: delete this and children,
NAME: you can type the new name,
COLOR: change the color,
SIZE: change the scale,
REZ: rez another node (click next on face for where to rez)
MOVE: pull the object in a direction (click next on face for where to rez),
TYPE: changes the object type,
HELP: go to online help,
UNLINK: remove the connecting beam",
            ["DELETE","NAME","COLOR",
             "SIZE","REZ","MOVE",
             "TYPE","HELP","UNLINK",
             "CONTENT" ]);
             trace("List in touch exit: "+llList2CSV(waiting));
            return;
        }
    }


    // listen must understand if this avatar already has pending menu
    // and correctly sort out of them
    listen(integer channel,string name, key id, string message)
    {
        debug("receiving a message in channel "+(string)channel+" message "+message);

        // PRIVATE CHANNEL
        if(channel==channelPrivate)
        {
            debug("Received a message for me from my parent "+message);
            propagate(message);
            return;
        }

        // PUBLIC CHANNEL
        if(channel==channelPublic)
        {
            // on channel public we ONLY receive OLD UUID in the format
            // UUID:
            if(llGetSubString(message,0,4)=="OUID:")
            {
                key olduuid=(key)llGetSubString(message,5,-1);
                debug("Received from "+(string)id+" UUID change from old "+(string)olduuid);

                // need to understand if it was MY target
                if(target==olduuid){
                  target=id;
                  particles(); // change the beam to this new target
                }
                // check my children
                integer pos=llListFindList(children,[olduuid]);
                if(pos>=0)
                {
                  debug("Replacing in children olduuid: "+(string)olduuid+" with "+(string)id);
                  children=llListReplaceList(children,[id],pos,pos);
                }

            }
            return;
        }

        // if not channel public or private then it shoudl be on stack
        integer index=findWaitingAvatar(id);
        debug("listen index found on waiting list: "+(string)index);
        if(index<0) return;

        // only here if we found on the stack
        integer elapsed=llGetUnixTime()-theTime;

        // remove handle AND the record from waiting list
        llListenRemove(theMenu);
        deleteRecord(index);
        debug("Found listen menu type: "+theType+" mesg "+message);

        // stopping menus
        if(theType=="MENUSTOPMOVE")
        {
             remove_detected();
             llInstantMessage(id,"Stop moving");
             return;
        }
        if(theType=="MENUSTOPREZ")
        {
             remove_detected();
             llInstantMessage(id,"Stop rezzing");
             return;
        }

        // handling menu content allow for setting content
        if(theType=="MENUCONTENT")
        {
          // allows for specifying a URL
          if(message=="SETURL")
          {
              addPrompt("PROMPTURL",id,"Say in chat the url where to go");
              return;
          }
          // just send help on how ctrl-dragging objects
          if(message=="SETCONTENT")
          {
              // send help
              llInstantMessage(id,"Please ctrl-drag something from your inventory on me. You can change the texture dragging a texture");
              return;
          }

          // going to stored URL
          if(message=="GIVE URL")
          {
              if(url!="")
              {
                  llLoadURL(id,"Go to webpage",url);
              }
              return;
          }
          // handle all GETXXX buttons
          string name; string desc;
          if(message=="GIVE NOTE")
          {
              name=getFromListOfType(currentInventory,INVENTORY_NOTECARD);
              desc="notecard";
          }
          if(message=="GIVE LMARK")
          {
              name=getFromListOfType(currentInventory,INVENTORY_LANDMARK);
              desc="landmark";
          }
          if(message=="GIVE OBJECT")
          {
              name=getFromListOfType(currentInventory,INVENTORY_OBJECT);
              desc="object";
          }
          if(message=="GIVE TEXTURE")
          {
              name=getFromListOfType(currentInventory,INVENTORY_TEXTURE);
              desc="texture";
          }

          if(name=="")
          {
                  llInstantMessage(id,"No "+desc+" to give you");
                  return;
          }
          // giving actually the object
          llGiveInventory(id,name);
          llInstantMessage(id,"You have been given a "+desc+" named "+name);
          return;


        }

        // Handling of the options in MAIN MENU
        if(theType=="MENUMAIN")
        {
           if(message=="HELP")
           {
               llLoadURL(id,"Load this page for help","http://opensimita.org/lsl/mindmap/README.html");
                return;
           }
           if(message=="CONTENT")
           {
               integer i;
               string texture=getFromListOfType(currentInventory,INVENTORY_TEXTURE);
               string object=getFromListOfType(currentInventory,INVENTORY_OBJECT);
               string note=getFromListOfType(currentInventory,INVENTORY_NOTECARD);
               string landmark=getFromListOfType(currentInventory,INVENTORY_LANDMARK);
               string prompt = "Choose an action:
SETCONTENT: explains how to insert an object
SETURL: allows for specifying a url";
               list buttons=["SETCONTENT","SETURL" ];
               if(url!="")
               {
                   prompt+="\nGIVE URL: go to the url "+url;
                   buttons+=["GIVE URL"];
               }
               if(note!="")
               {
                   prompt+="\nGIVE NOTE: get the note "+note;
                   buttons+=["GIVE NOTE"];
               }

               if(object!="")
               {
                   prompt+="\nGIVE OBJECT: get the object "+object;
                   buttons+=["GIVE OBJECT"];
               }

               if(landmark!="")
               {
                   prompt+="\nGIVE LMARK: get the landmark "+landmark;
                   buttons+=["GIVE LMARK"];
               }
               if(texture!="")
               {
                   prompt+="\nGETTEXTURE: get the texture "+texture;
                   buttons+=["GIVE TEXTURE"];
               }


               addMenu("MENUCONTENT",id,prompt,buttons);
               return;
           }
           if(message=="NAME")
           {
               addPrompt("PROMPTNAME",id,"Say in chat name of this concept");
               return;
            }
            if(message=="DELETE")
            {
                addPrompt("PROMPTDELETE",id,"Say DELETE in chat to be absolutely sure to delete from here");
                return;
            }
            if(message=="COLOR")
            {
               addMenu("MENUCOLOR",id,"Enter color",["RED","GREEN","BLUE","WHITE","BLACK","VIOLET","TURQUESE","YELLOW"]);
               return;
            }
            if(message=="SIZE")
            {
               addMenu("MENUSIZE",id,"Enter size",["HALF", "DOUBLE", "+0.2","-0.2","DEFAULT"]);
               return;
            }

            if(message=="UNLINK")
            {
                llParticleSystem([]); target=NULL_KEY;
                llInstantMessage(id,"Removed particles");
                return;
            }
            // detected category
            if(message=="REZ")
            {
                addDetected("DETECTPOSREZ",id,"Enter position where rez");
                addMenu("MENUSTOPREZ",id,"Click on a face of the concept to rez a new cube in that direction.\nClick 'stop' after chosing",["STOP"]);
                return;
            }
            if(message=="MOVE")
            {
                addDetected("DETECTMOVE",id,"Click on a face of the concept and the cube will move 20cm in that direction.");
                addMenu("MENUSTOPMOVE",id,"Click to stop moving",["STOP"]);
                return;
            }
            if(message=="TYPE")
            {
                addMenu("MENUTYPE",id,"Select type of this concept",["SPHERE","CUBE","FLAT","CYLINDER","PYRAMID","POINT","STAR","ENDTYPE"]);
                return;
            }
        }

        // change the type of this prim
        if(theType=="MENUTYPE")
        {
            if(message=="ENDTYPE")
            {
                llInstantMessage(id,"Finished with typing");
                return;
            }
            list typ=[];
            if(message=="FLAT")
            {
               vector scale=llGetScale();
              llSetScale(<0.01,scale.y,scale.z>);
              return;
            }

            if(message=="POINT")
            {
              llSetScale(<0.01,0.01,0.01>);
              return;
            }
            if(message=="STAR")
            {
              llInstantMessage(id,"STAR not yet implemented");
              return;
            }


            if(message=="SPHERE") typ=[ PRIM_TYPE, PRIM_TYPE_SPHERE, 0, <0,1,0>, 0.0, <0,0,0>,<0,1,0> ];
            if(message=="CUBE") typ=[ PRIM_TYPE, PRIM_TYPE_BOX,0, <0.0, 1.0, 0.0>, 0.0, <0.0, 0.0, 0.0>, <1.0, 1.0, 0.0>, <0.0, 0.0, 0.0>];
            if(message=="CYLINDER") typ=[ PRIM_TYPE, PRIM_TYPE_CYLINDER, 0, <0.0, 1.0, 0.0>, 0.0, <0.0, 0.0, 0.0>, <1.0, 1.0, 0.0>, <0.0, 0.0, 0.0>];
            if(message=="PYRAMID") typ=[ PRIM_TYPE, PRIM_TYPE_BOX,0, <0.0, 1.0, 0.0>, 0.0, <0.0, 0.0, 0.0>, <0.0, 0.0, 0.0>, <0.0, 0.0, 0.0>];

            llSetPrimitiveParams(typ);

            addMenu("MENUTYPE",id,"Select type of this concept",["SPHERE","CUBE","FLATBOX","CYLINDER","PYRAMID","POINT","STAR","ENDTYPE"]);
            return;

        }


        // change the size of this prim
        if(theType=="MENUSIZE")
        {
            vector current=llGetScale();
            if(message=="HALF") current=current/2;
            if(message=="DOUBLE") current=current*2;
            if(message=="+0.2") current=current+<0.2,0.2,0.2>;
            if(message=="-0.2") current=current-<0.2,0.2,0.2>;
            if(message=="DEFAULT") current=<0.5,0.5,0.5>;
            llSetScale(current);
            llInstantMessage(id,"Size changed to '"+(string)current+"'");
            return;

        }

        // change the color of this prim
        if(theType=="MENUCOLOR")
        {
            if(message=="RED") llSetColor(<1,0,0>,ALL_SIDES);
            if(message=="GREEN") llSetColor(<0,1,0>,ALL_SIDES);
            if(message=="BLUE") llSetColor(<0,0,1>,ALL_SIDES);
            if(message=="WHITE") llSetColor(<1,1,1>,ALL_SIDES);
            if(message=="BLACK") llSetColor(<0,0,0>,ALL_SIDES);
            if(message=="VIOLET") llSetColor(<1,0,1>,ALL_SIDES);
            if(message=="TURQUESE") llSetColor(<0,1,1>,ALL_SIDES);
            if(message=="YELLOW") llSetColor(<1,1,0>,ALL_SIDES);
            llInstantMessage(id,"Color changed to '"+message+"'");
            return;
        }

        // change the name
        if(theType=="PROMPTNAME")
        {
            notify(message);
            llSetObjectName(message);
            llInstantMessage(id,"Name changed to '"+message+"'");
            return;
        }
        if(theType=="PROMPTDELETE")
        {
            if(message=="DELETE")
            {
                // handle delete message
                propagate(message);
                return;
            }
        }

        // change the url
        if(theType=="PROMPTURL")
        {
            url=message;
            llInstantMessage(id,"URL accepted: "+url);
            return;
        }


    }
    // when new node is rezzed then we give this script running and tell it
    // my id so that it can emit particles
    object_rez(key id)
    {

        // understand the remotepin which is publicchannel
        integer remotePin=key2int(llGetOwner());
        integer childchannel=key2int(id);

        llRemoteLoadScriptPin(id, llGetScriptName(), remotePin, TRUE, key2int(llGetKey()));
        debug("Obtaining my key: "+(string)childchannel+(string)llGetKey());

        // memorize this channel so to be able to speak to all my children in case of die
        children+=[id];

        llGiveInventory(id,"nodo");

        debug("Chatting "+(string)llGetKey()+" on channel "+(string)key2int(id)+ "children: "+llList2CSV(children));
        llSay(childchannel,(string)llGetKey());

        //llInstantMessage("Node created");
    }
}
```

## Having a copy from XStreetsl

You can get this object inworld IMming me.
I'm NO MORE distributing anything on XStreetSL after the new policies in 2009 where Lindend made impossible to distribute freebies)