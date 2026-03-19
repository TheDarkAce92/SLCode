---
name: "Wiki3DBuilder1.0"
category: "example"
type: "example"
language: "LSL"
description: "Here an advance version of Wiki3DBuilder.. See it for a simpler and less powerful version. Here I put the differences. You can get this object inworld IMming me. I'm NO MORE distributing anything on XStreetSL after the new policies in 2009 where Lindend made impossible to distribute freebies) if you have problems in setting it up (it's not easy since it is using \"Matrioshka like\" embedded objects."
wiki_url: "https://wiki.secondlife.com/wiki/Wiki3DBuilder1.0"
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
- 4 The dropbox script
- 5 Having a copy from SL Marketplace

## Introduction

Here an advance version of Wiki3DBuilder.. See it for a simpler and less powerful version. Here I put the differences.
You can get this object inworld IMming me.
I'm NO MORE distributing anything on XStreetSL after the new policies in 2009 where Lindend made impossible to distribute freebies) if you have problems in setting it up (it's not easy since it is using "Matrioshka like" embedded objects.

There are 3 levels of embedding:

- the root cube
- the inner NODE carrying a copy of the main program and a dropbox object
- the dropbox object

The main differences from the v0.1 version are the following:

- Every cube rezzed is LINKED to all the structure (easier to move around and to put and rez from inventory)
- Removed llSay for internal communication replaced with linked messages (faster and more professional)
- Removed forced putting of script via llRemoteLoadPIN
- Added the "bin" metaphor to be able to put objects precisely in nodes (I was obliged to do this since when ctrl-dragging into linked objects they are going to root :( )
- It allows to "lock" the object putting "LOCKED" in the description of the root prim
- It allows restricting access to group or owner putting "GROUP" "OWNER" in the description of the root prim
- and some other minor modifications



### Disclaimer

This is still a POC (Proof of Concept) and it is meant as a beta stage prototype I developed during last weeks.
It should be now relatively mature to be used as it solved many unprofessional aspects in version 0.1.

Still are remaining the following things to do probably to have it better:

- Split the script in two or more scripts (right now it is a huge script and might need splitting
- control better the way things are put and retrieved from the bin into the node inventory
- Have it dialog with a website (like moodle) to render hierarchical structures automatically from the website
- When communicating with website it can however "serve" apart from URL and text from the website, also UUID of notecars, texture, and possibly distributing remote objects

### QuickStart

- Build a bin name it dropbox and put inside the dropbox script
- Build a cube, name it "NODE1" and put inside the llSetPin script, the dropbox object, and a copy of the main script. Be sure to RESET it to show "node" over it
- Build another cube, name it Wiki3D_Builder1.0 and put inside its content the "NODE1" and the main script
- Reset the script be sure to give the LINK permissions. In case you have problems you can also access the reset script from the menu.
- Resetting the script should be done also when changing owner



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

There is now protection against unauthorized access to the object so you can be sure hackers cannot destroy your work.
Just put "LOCKED" or "OWNER" or "GROUP" inside the description of the root prim




### How it works

Initially you have a NODE (i.e., a cube) which must be touched to start the process

- Touch object to see a menu with these options: color, name, size, content, move, rez
- Select "color" to enter a color on the local chat
- Select "textcolor" to enter a color for the node name
- Select "name" to enter a name on the local chat
- Select "size" to enter a size on the local chat
- Select "new cube" to rez a new node; when choosing this option, you must touch one of the faces of the cube and a new node will be rezzed 50cm on that direction.
- Select "move" and then touch a face to pull the node towards in direction
- Select "content" and "setcontent" to rez a bin where to move inventory items.
- Authorized users can move objects, textures and so from their inventory to a node (CTRL-Dragging them on the bin).
- **Contents:** Only one type of inventory item can be in the node at one time, and that content can be given to whom is asking for content
- Changing the texture will also change the texture of the node



### Internal architecture

This is done in ONLY one script named "Main Script" and an internal object named "NODE1".
The "Main Script" is implementing a quite interesting mechanism for dealing with "multi-threading", i.e. multiple
avatars touching the object at the same time. This is accomplished using an Array of RECORDs representing
the waiting avatars and what they were waiting for. So listen(), touch(), and other events can query this QUEUE
and understand what is to be made next.
This also allows for an interesting handling of MULTI MENU
A part from this the rest is relatively simple, except for the communication between the various nodes made with LinkedMessages

Here some of the internal protocol messages

- ROOT:PRUNEALL to ask the root to prune all nodes
- PARENT:ADD parent is informed of a new ID for child (so it can have an array of children)
- CHILD:BEAM parent is asking the child to "beam" to the parent with particles (used at first rez and when rezzing from inventory and when RESET LOCAL)
- PARENT:UUID child is asking the UUID of its parent for beaming onto it
- ROOT:LINK root is asked to keep track of a new node linking it and be sure that new node and its parent know each other
- CHILD:CHANGEDESC root is informing that description has changed (LOCKED OWNER GROUP) so that children can behave consequently
- When a node is unlinked and is alone it simply llDie's so this is a way for simply prune your mindmap if you are the owner.

## llSetPin to put in "nodo" object

This is NOT  needed but currently we are detecting we are not in the root checking for this. So you can simply put an empty script.



```lsl
default
{
    state_entry()
    {
    }
}
```

## The Main Script

```lsl
// CUSTOMIZABLE PARAMETERS
integer TIMEOUT=30;       // menu will be obsolesced after this period of time
integer CLEANTIMERSEC=10; // timer will run once every this period of time for cleaning timers
integer DEBUG=2;          // 2 maximum level (10: debug, 9: traces)
integer USESAY=1;         // use SAY or instantmessages
string nodename="NODE1";
// END OF CUSTOMIZABLE PARAMETERS

// Wiki3DBuilder version 1.0
// Add Functionalities
// - make glow the object current under editing
// - allow FREEZE the mindmap
// - allow for private or group usage using LINKSET!!!!!
// - using only linked messages instead of listen/say
// - implement LINKed sets and a framework of conversation among nodes
//
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
//
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

integer incchannel=1000; // incrementing channel for assigning identities to created prims
integer mychannel=-1; // must be esplicitly set to begin answering linked messages
integer waitingrez=FALSE;
integer waitingdrop=FALSE;

string url=""; // url associated with this node

// will send to that channel a command.. key will hold the sending channel for answers
send(integer channel, string command) {
    debug("Sending on channel "+(string)channel+" command "+command+" key: "+(string)mychannel);
    llMessageLinked(LINK_SET,channel,command,(key)((string)mychannel));
}

// 0) General utility functions

// debug this string only if DEBUG is at least 1
debug(string str) {
    if(DEBUG>=1)llSay(10,"DEBUG "+(string)llGetKey()+"."+str);
}

// trace the string only if DEBUG is 2
trace(string str){
    if(DEBUG>=2)llSay(9,"TRACE "+(string)llGetKey()+"."+str);
}
vector text=<0,1,0>; // default is red
// will put on the hover string
notify(string str){
    llSetText(str,text,1);
}
// this might be shown on a board
inform(key id,string str) {
    if(USESAY==1)
        llSay(0,str+" ["+llKey2Name(id)+"]");
    else
        llInstantMessage(id,str);
}
// **********************************************************
// 1) RECORD STACK
// handling. We keep a "queue" or RECORDS for understanding
// multi-avatar touching and remember prompts and menu and let them expire
// **********************************************************

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
        trace("Loading the record: \n   type: "+theType+"\n   Av: "+(string)theAv+"\n   time: "+(string)theTime+"\n   menu: "+(string)theMenu+"\n   channel:"+(string)theChannel+"\n   rest:"+theRest);
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
    trace("Looking for avatar: "+(string)av);
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
        PSYS_PART_END_SCALE,<0.4,.1,FALSE>,
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
list children=[]; // will keep the keys of ALL depending children
//
// Handling menu main
//
menumain(key id, string message)
{
    if(message=="HELP")
    {
        llLoadURL(id,"Load this page for help","http://opensimita.org/lsl/mindmap/README.html");
        return;
    }
    if(message=="CONTENT")
    {
        showMenuContent(id);
        return;
    }
    if(message=="NAME")
    {
        addPrompt("PROMPTNAME",id,"Say in chat name of this concept");
        return;
    }
    if(message=="PRUNE")
    {
        addMenu("MENUPRUNE",id,"What:\nPRUNE: me and my children\nPRUNEALL: all except root",["PRUNE","PRUNEALL"]);
        return;
    }
    if(message=="COLOR")
    {
        addMenu("MENUCOLOR",id,"Enter node color",["RED","GREEN","BLUE","WHITE","BLACK","VIOLET","TURQUESE","YELLOW"]);
        return;
    }
    if(message=="TEXTCOLOR")
    {
        addMenu("MENUTEXTCOLOR",id,"Enter text color",["RED","GREEN","BLUE","WHITE","BLACK","VIOLET","TURQUESE","YELLOW"]);
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
        inform(id,"Removed particles");
        return;
    }
    // detected category
    if(message=="NEWCUBE")
    {
        addDetected("DETECTPOSREZ",id,"Click face where you want to extrude a new cube");
        addMenu("MENUSTOPREZ",id,"Click on a face of the concept to rez a new cube in that direction.\nClick 'stop' after chosing",["STOP"]);
        return;
    }
    if(message=="MOVE")
    {
        addDetected("DETECTMOVE",id,"Click on a face of the node and the cube will move 20cm in that direction.");
        addMenu("MENUSTOPMOVE",id,"Click on a face of the node and the cube will move 20cm in that direction. \nSTOP: finish moving",["STOP"]);
        return;
    }
    if(message=="TYPE")
    {
        addMenu("MENUTYPE",id,"Select type of this concept",["SPHERE","CUBE","FLAT","CYLINDER","PYRAMID","POINT","STAR","ENDTYPE"]);
        return;
    }
    if(message=="RESET")
    {
        addMenu("MENURESET",id,"Type of reset\nLOCAL: owner/beam\nSCRIPT: the local script (warn this might put the node in an unusable state)",["LOCAL","SCRIPT" ]);
        return;
    }
}
localReset()
{
        currentOwner=llGetOwner();
        trace("Object rezzed with new taskUUID, need to update all the beams");
        if(parentchannel!=-1)
        {
            // need to reinstate the beam versus my parent, ask the new UUID
            send(parentchannel,"PARENT:UUID");
        }
}

menuReset(key id, string message)
{
   if(message=="SCRIPT") llResetScript();
   if(message=="LOCAL") localReset();

}
//
// Menu Size
//
menusize(key id, string message)
{
    vector current=llGetScale();
    if(message=="HALF") current=current/2;
    if(message=="DOUBLE") current=current*2;
    if(message=="+0.2") current=current+<0.2,0.2,0.2>;
    if(message=="-0.2") current=current-<0.2,0.2,0.2>;
    if(message=="DEFAULT") current=<0.5,0.5,0.5>;
    llSetScale(current);
    inform(id,"Size changed to '"+(string)current+"'");
    return;
}
//
// Menu color
//
menucolor(key id,string message)
{
    if(message=="RED") llSetColor(<1,0,0>,ALL_SIDES);
    if(message=="GREEN") llSetColor(<0,1,0>,ALL_SIDES);
    if(message=="BLUE") llSetColor(<0,0,1>,ALL_SIDES);
    if(message=="WHITE") llSetColor(<1,1,1>,ALL_SIDES);
    if(message=="BLACK") llSetColor(<0,0,0>,ALL_SIDES);
    if(message=="VIOLET") llSetColor(<1,0,1>,ALL_SIDES);
    if(message=="TURQUESE") llSetColor(<0,1,1>,ALL_SIDES);
    if(message=="YELLOW") llSetColor(<1,1,0>,ALL_SIDES);
    inform(id,"Color changed to '"+message+"'");
    return;
}

menuTextColor(key id,string message)
{
    if(message=="RED") text=<1,0,0>;
    if(message=="GREEN") text=<0,1,0>;
    if(message=="BLUE") text=<0,0,1>;
    if(message=="WHITE") text=<1,1,1>;
    if(message=="BLACK") text=<0,0,0>;
    if(message=="VIOLET") text=<1,0,1>;
    if(message=="TURQUESE") text=<0,1,1>;
    if(message=="YELLOW") text=<1,1,0>;
    notify(llGetObjectName());
    inform(id,"Text Color changed to '"+message+"'");
    return;
}

//
// Menu TYPE
//
menutype(key id,string message)
{
    if(message=="ENDTYPE")
    {
        inform(id,"Finished with typing");
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
        llSetPrimitiveParams([ PRIM_TYPE, 7, "92ed71aa-d27f-31bc-57b8-7d699fc7cde5", 1, PRIM_ROTATION, <-0.627212, -0.326506, -0.326506, 0.627211>, PRIM_SIZE, <0.500000, 0.500000, 0.108749> ]);
        //inform(id,"STAR not yet implemented I have sculpted however :)");
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

//
// Handling menu content
//
menucontent(key id,string message)
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
        // use a special trick since SL doesn't allow us doing that
        waitingdrop=key2int(llGetKey());
        llRezAtRoot("dropbox",llGetPos()+<0.2,0.2,0.2>,ZERO_VECTOR,ZERO_ROTATION,waitingdrop);
        inform(id,"Please ctrl-drag something from your inventory on the dropbox. You can change the texture dragging a texture");
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
    if(message=="GIVE SCRIPT")
    {
        name=getFromListOfType(currentInventory,INVENTORY_SCRIPT);
        desc="script";
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
        inform(id,"No "+desc+" to give you");
        return;
    }
    // giving actually the object
    llGiveInventory(id,name);
    inform(id,"You have been given a "+desc+" named "+name);
    return;
}
showMenu(key av)
{
    if(isBlocked(av)==FALSE)
    {
        string menudesc="Main menu:"; list menubuttons=[];
        menudesc+="\nRESET: reset"; menubuttons+=["RESET"];
        if(av==currentOwner) menudesc+="\nPRUNE: cleanup"; menubuttons+=["PRUNE"];
        menudesc+="\nTYPE:object type"; menubuttons+=["TYPE"];
        menudesc+="\nHELP: get web help"; menubuttons+=["HELP"];


        menudesc+="\nNAME: change name"; menubuttons+=["NAME"];
        menudesc+="\nCOLOR: choose color"; menubuttons+=["COLOR"];
        menudesc+="\nTEXTCOLOR: text color"; menubuttons+=["TEXTCOLOR"];
        menudesc+="\nSIZE: choose size"; menubuttons+=["SIZE"];
        menudesc+="\nNEWCUBE: create new concept"; menubuttons+=["NEWCUBE"];
        menudesc+="\nMOVE: pull the node"; menubuttons+=["MOVE"];

        menudesc+="\nCONTENT: go to content"; menubuttons+=["CONTENT"];

        addMenu("MENUMAIN",av,menudesc,menubuttons);
    } else showMenuContent(av);
}
showMenuContent(key id)
{
    string texture=getFromListOfType(currentInventory,INVENTORY_TEXTURE);
    string object=getFromListOfType(currentInventory,INVENTORY_OBJECT);
    string note=getFromListOfType(currentInventory,INVENTORY_NOTECARD);
    string landmark=getFromListOfType(currentInventory,INVENTORY_LANDMARK);
    string script=getFromListOfType(currentInventory,INVENTORY_SCRIPT);
    string prompt = "Content:"; list buttons=[];
    if(isBlocked(id)==FALSE)
    {
        prompt+="\nSETCONTENT: explains how to insert an object"; buttons+=["SETCONTENT"];
        prompt+="\nSETURL: allows for specifying a url"; buttons+=["SETURL"];
    }


    if(url!="")
    {
        prompt+="\nGIVE URL: go to the url "+url; buttons+=["GIVE URL"];
    }
    if(note!="")
    {
        prompt+="\nGIVE NOTE: get the note "+note;
        buttons+=["GIVE NOTE"];
    }
    if(script!="")
    {
        prompt+="\nGIVE SCRIPT: get the script "+script; buttons+=["GIVE SCRIPT"];
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
    if(prompt=="Content:") prompt="Node is empty";
    addMenu("MENUCONTENT",id,prompt,buttons);
}
// ============================== MAIN =========================
// will NO MORE USE voice channels for internal communication
// when entering here IT IS NOT LINKED so must wait to be linked
integer privChannel;

key parent=NULL_KEY;
integer parentchannel=-1;
default
{
    on_rez(integer flag)
    {
        inventoryUpdate();
        if(flag==0)
        {
            mychannel=0; // i'm the root
            state ready;
        }
        debug("Waiting to be linked and assigned a channel");
    }
    state_entry()
    {
        notify("node");
        // when reset for debug should go directly on read
        if(llGetInventoryName(INVENTORY_SCRIPT,0)!="llSetPin")
        {
            inventoryUpdate();
            mychannel=0;
            state ready;
        }
    }

    // ON v0.2 we got rid from any listeners only LINKMESSAGES
    // will wait until on channel#1 will appear my key id, string is CHILD:CHANNEL|channel|parentchannel
    link_message(integer sender, integer channel, string str, key id)
    {
        //debug("Received channel "+(string)str+" key: "+(string)id+" myUUID: "+(string)llGetKey());
        if(channel!=1) return;
        debug("Received channel "+(string)str+" key: "+(string)id+" myUUID: "+(string)llGetKey());
        if(id!=llGetKey()) return;

        list pieces=llParseStringKeepNulls(str,["|"],[]);
        string command=llList2String(pieces,0);
        mychannel=(integer)llList2String(pieces,1);
        parentchannel=(integer)llList2String(pieces,2);

        // ask UUID to parent to emit proper beam
        send(parentchannel,"PARENT:UUID");

        state ready;

    }
}

// =========================== READY =========================
state ready
{
    state_entry()
    {
        currentOwner=llGetOwner();
        if(mychannel==0) llRequestPermissions(llGetOwner(), PERMISSION_CHANGE_LINKS);
        // reset waiting list
        waiting=[]; children=[];
        llSetTimerEvent(CLEANTIMERSEC); // garbage collector

        // allow inventory dropping (for content dropping)
        llAllowInventoryDrop(TRUE);
    }
    run_time_permissions(integer permissions)
    {
        if(!(permissions & PERMISSION_CHANGE_LINKS))
        {
            notify("Cannot work without change link permissions");
            state default;
        }
        notify("Wiki3D v1.0\n By Salahzar Stenvaag, nc, sa 2009\nFree Memory:"+(string)llGetFreeMemory());
    }

    //
    // Rezzed here from inventory
    //
    on_rez(integer rez)
    {
        localReset();
    }
    // If we changed owner or inventory
    changed(integer change)
    {
        //llSay(0,"change: "+(string)change);
        if(change & CHANGED_OWNER)
        {

            currentOwner=llGetOwner();
            debug("Changed owner, resetting owner to "+(string)currentOwner);
            // state default;
        }
        // handle changing of the inventory or somebody dropped
        if(change & CHANGED_INVENTORY || change & CHANGED_ALLOWED_DROP)
        {
            inventoryUpdate();
        }
        if(change & CHANGED_LINK && mychannel!=0 && llGetObjectPrimCount(llGetKey())==1)
        {
            // if unlinked and left alone and NOT root die
            inform(llGetOwner(),"dying since unlinked and alone");
            llDie();
            return;
        }
    }

    // timer is trying to get all the menu listener clean
    // if they are exhausted then proceed to cancel them
    timer()
    {
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
        // remove glow
        if(i==0)
        {
            glowOff();
        }
        //debug("List in timer exit: "+llList2CSV(waiting));
        if(currentDesc!=llGetObjectDesc() && mychannel==0)
        {

            // description has been changed
            inform(llGetOwner(),"Changed security to "+llGetObjectDesc());
            send(2,llGetObjectDesc());
        }
    }
    // main menu listening for waiting avatars
    // we answer only to
    touch_start(integer total_number)
    {
        integer i;
        for(i=0;i=0)
            {
                trace("Has already a menu waiting");
                // we have a menu for this avatar.. Check if we have it in detected_key
                // in such case we allow touching for detecting
                if(av==detected_key)
                {
                    trace("We have a detected_key for this avatar  type:"+detected_type);
                    // handle this event
                    if(detected_type=="DETECTMOVE")
                    {

                        vector realnormal=llDetectedTouchNormal(i); //*llEuler2Rot(<0,0,PI/2>);
                        debug("Moving the prim normal: "+(string)llDetectedTouchNormal(i)+ " realnormal: "+(string)realnormal);
                        llSetPos(llGetLocalPos()+realnormal*0.2);
                    }
                    if(detected_type=="DETECTPOSREZ")
                    {
                        debug("rezzing a new cube");
                        vector posrez=llDetectedTouchNormal(i);

                        // will rez it the channel number will be given by the root
                        waitingrez=TRUE;
                        llRezAtRoot(nodename,llGetPos()+posrez,ZERO_VECTOR,ZERO_ROTATION,1);
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
                inform(av,"Removing pending menu/prompt");
                return;
            }

            // avatar hasn't any pending menu so start with main menu
            // start the initial menu
            showMenu(av);
            trace("List in touch exit: "+llList2CSV(waiting));
            return;
        }
    }

    // listen must understand if this avatar already has pending menu
    // and correctly sort out of them
    listen(integer channel,string name, key id, string message)
    {
        trace("receiving a message in channel "+(string)channel+" message "+message);

        // we just listen to MENU STACK
        integer index=findWaitingAvatar(id);
        debug("listen index found on waiting list: "+(string)index);
        if(index<0) return;

        // only here if we found on the stack
        integer elapsed=llGetUnixTime()-theTime;

        // remove handle AND the record from waiting list
        llListenRemove(theMenu);
        deleteRecord(index);
        trace("Found listen menu type: "+theType+" mesg "+message);

        // stopping menus
        if(theType=="MENUSTOPMOVE")
        {
            remove_detected();
            inform(id,"Stop moving");
            return;
        }
        // stopping menus
        if(theType=="MENUSTOPREZ")
        {
            remove_detected();
            inform(id,"Stop rezzing");
            return;
        }
        if(theType=="MENUTEXTCOLOR")
        {
            menuTextColor(id,message);
            return;
        }
        if(theType=="MENURESET")
        {
            menuReset(id,message);
            return;
        }

        if(theType=="MENUPRUNE")
        {
            if(message=="PRUNE")
            {
                // should collect all my children and tell root this list
                inform(id,"Not yet implemented");
                return;
            }
            if(message=="PRUNEALL")
            {
                // tell the root to do this
                send(0,"ROOT:PRUNEALL");
                return;
            }
        }
        // handling menu content allow for setting content
        if(theType=="MENUCONTENT")
        {
            menucontent(id,message);
            return;

        }

        // Handling of the options in MAIN MENU
        if(theType=="MENUMAIN")
        {
            menumain(id,message);
            return;
        }

        // change the type of this prim
        if(theType=="MENUTYPE")
        {
            menutype(id,message);
            return;

        }

        // change the size of this prim
        if(theType=="MENUSIZE")
        {
            menusize(id,message);
            return;
        }

        // change the color of this prim
        if(theType=="MENUCOLOR")
        {
            menucolor(id,message);
            return;
        }

        // change the name
        if(theType=="PROMPTNAME")
        {
            notify(message);
            llSetObjectName(message);
            inform(id,"Name changed to '"+message+"'");
            return;
        }
        // change the url
        if(theType=="PROMPTURL")
        {
            url=message;
            inform(id,"URL accepted: "+url);
            return;
        }
    }
    // when new node is rezzed then we give this script running and tell it
    // my id so that it can emit particles
    object_rez(key id)
    {
        if(waitingdrop!=FALSE)
        {
            llSleep(0.2);
            llSay(waitingdrop,""); // tell our waiting drop our UUID
            waitingdrop=FALSE;
            return;
        }
        if(waitingrez==FALSE) return; // don't fire too much
        waitingrez=FALSE;
        // understand the remotepin which is owner dependent
        //integer remotePin=key2int(llGetOwner());

        //llRemoteLoadScriptPin(id, llGetScriptName(), remotePin, TRUE, key2int(llGetKey()));
        llGiveInventory(id,nodename);
        // tell ROOT to link this newly created object
        send(0,"ROOT:LINK|"+(string)id);
        // it will wait until we will receive an acknowledgement from this son
    }
    //
    // Message handling when rezzing a new cube (only in ready state)
    //
    // Somebody can send me a message: PARENT:ADD and ROOT:LINK
    link_message(integer sender, integer channel, string str, key id)
    {
        // we can control FREEZING/PRIVACY sending this on channel 2 (public channel)
        trace("XXXX Receiving "+str+" from channel "+(string)channel+" id: "+(string)id);
        if(channel==2)

        {
            debug("Receiving on channel#2 CHILD:CHANGEDESC "+str);
            llSetObjectDesc(str);
            currentDesc=str;
            return;

        }

        // message NOT for me (root prim will answer to 0)
        if(channel!=mychannel) return;
        integer senderchannel=(integer)( (string)id);
        trace("Received from sender: "+(string)sender+" to channel "+(string)channel+" msg: "+str+" senderchannel: "+(string)senderchannel);

        // get command from str
        list pieces=llParseStringKeepNulls(str,["|"],[]);
        string cmd=llList2String(pieces,0);
        string parm=llList2String(pieces,1);

        // root is informed a new node has been generated by parent
        if(cmd=="ROOT:LINK")
        {
            key linkthis=(key)parm;
            debug("Creating a link with new object "+(string)parm);
            llCreateLink(linkthis,TRUE);
            debug("Informing it about its parent which is "+(string)senderchannel);

            // inform new linked object who is his parent (send id to be sure only newborn will get this
            // this will be received in the initial default state
            string s="CHILD:CHANNEL|"+(string)incchannel+"|"+(string)senderchannel;
            debug("Sending "+s+" on channel 1.. Id is "+(string)linkthis);
            llMessageLinked(LINK_SET,1,s,linkthis);

            // inform parent which new channel to be used to communicate with this child
            send(senderchannel,"PARENT:ADD|"+(string)incchannel);

            // increment channel number so that we have fresh number and no collisions
            incchannel++;
            return;
        }
        // somebody requesting our UUID for starting up a new beam
        if(cmd=="PARENT:UUID")
        {
            debug("Being asked my new UUID");
            send(senderchannel,"CHILD:BEAM");
            return;
        }
        // parent told me its UUID so we will project a new BEAM
        if(cmd=="CHILD:BEAM")
        {
            debug("Changing target to new UUID after rezzing");
            target=llGetLinkKey(sender);
            particles();
            return;
        }
        // parent will receive this from the root when adding new child
        if(cmd=="PARENT:ADD")
        {
            integer childchannel=(integer)parm;
            // memorize this channel so to be able to speak to all my children in case of die
            debug("Adding childchannel "+(string)childchannel+" to my children");

            children+=[childchannel];

            return;

        }
        if(cmd=="ROOT:PRUNEALL")
        {
            integer n=llGetObjectPrimCount(llGetKey());
            integer i;
            for(i=n;i>=2;i--)
            {
                debug("Breaking link #"+(string)i);
                // this will also delete the box
                llBreakLink(i);
            }
        }
    }
}
```

## The dropbox script

```lsl
key parentuuid;
default
{

    state_entry()
    {
        llSetText("Waiting to be enabled",<1,1,1>,1);
        llSetRot(llEuler2Rot());
    }
    on_rez(integer channel)
    {
        llSetRot(llEuler2Rot());
        if(channel!=0)
            llListen(channel,"",NULL_KEY,"");
    }
    touch_start(integer count)
    {
        llDie();
    }
    listen(integer channel, string name, key id, string str)
    {
        parentuuid=id;
        state ready;
    }
}
state ready
{
    state_entry()
    {
        llSetText("Drop on me something within 90 seconds",<1,1,1>,1);
        llSetTimerEvent(90);
        llAllowInventoryDrop(TRUE);
    }
    touch_start(integer count)
    {
        llDie();
    }
    on_rez(integer channel)
    {
        llSetRot(llEuler2Rot());
        if(channel!=0)
            llListen(channel,"",NULL_KEY,"");
    }
    timer()
    {
        llDie();
    }
    listen(integer channel, string name, key id, string str)
    {
        parentuuid=id;
        state ready;
    }
    changed(integer change)
    {
        string name=llGetInventoryName(INVENTORY_ALL,0);
        if(name==llGetScriptName()) name=llGetInventoryName(INVENTORY_ALL,1);
        llSetText("Sending object to node...",<1,1,1>,1);
        llGiveInventory(parentuuid,name);
        llDie();

    }
}
```

## Having a copy from SL Marketplace

If you have any difficulties in having these scripts running, please get a copy from SL Marketplace for 0 L$: [https://marketplace.secondlife.com/p/Wiki-3D-v104-OFFICIAL/1970024](https://marketplace.secondlife.com/p/Wiki-3D-v104-OFFICIAL/1970024)