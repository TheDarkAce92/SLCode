---
name: "One Script, many doors"
category: "example"
type: "example"
language: "LSL"
description: "This script is my attempt at solving the massive amount of simple door scripts one can have in a sim (I removed about 110 door scripts in my sim using this system)"
wiki_url: "https://wiki.secondlife.com/wiki/One_Script,_many_doors"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

This script is my attempt at solving the massive amount of simple door scripts one can have in a sim (I removed about 110 door scripts in my sim using this system)

It handles clockwise and counter clockwise door direction, a name-based access control list, play sounds, and the root prim reports memory free (useful for REALLY big door sets).

HOW TO USE IT

All your doors have to be one prim, typical cube with a path cut of 0.125 0.625 .

- All your doors must be linked to a root prim which won't be a door.
- All the doors must be uniquely named.
- All the doors must have "left" or "right" in their description depending on the direction you want them to swing to.

- In the root prim you will need 3 rezzable objects (simple cubes will do) named "open" , "close" and "lock" with, in them, the corresponding scripts (see at the bottom of the page) in order to play sounds at the right place.

- You need a configuration notecard called "config"

main door script: must be in the root prim of the door link set.

```lsl
/*******************************************
Single script, linked, lockable, door system
by Kyrah Abattoir

allow you to control many doors from a single
core script, complete with sound projectors
and name based access control!
*******************************************/

float autoclose_time = 30.0;//define how long the script will wait before closing a door.
float activation_distance = 2.0;//define how long the script will wait before closing a door.

//This functions is from Nomad Padar, pretty awesome!
//encode from vector to integer
integer vec2int(vector v)
{
    integer x = (integer)(v.x);
    integer y = (integer)(v.y);
    integer z = (integer)(v.z);
    integer out;

    //Rounds to 0, .5, or 1.0
    float delta = v.x-x;

    if((delta>.25) && (delta<.75))
        out += 0x10000000;
    else if(delta>.75)
        out += 0x1;

    delta = v.y-y;

    if((delta>.25) && (delta<.75))
        out += 0x20000000;
    else if(delta>.75)
        out += 0x100;

    delta = v.z-z;

    if((delta>.25) && (delta<.75))
        out += 0x40000000;
    else if(delta>.75)
        out += 0x10000;

    out += x+(y<<8)+(z<<16);
    return out;
}

list door_names         = [];//door list
list door_num           = [];//corresponding link numbers
list door_closed_rot    = [];//corresponding closed state rotation
list door_direction     = [];//which direction the door spin open
list door_open          = [];//is the door open?
list door_open_time     = [];//when was it open?
list door_acl           = [];//who can open the door (by user id)
list door_pos           = [];//the position of the door

list user_indexes       = [];//list of users (user ids)

integer is_active = FALSE;//if this is false the script ignore touches

recount_doors()
{
    //this function recount the doors and record all the different door characteristics
    //only ran after script reset/when an object is linked/unlinked
    is_active = FALSE;
    llSetText("recounting doors...",<1.0,1.0,1.0>,1.0);
    integer prims = llGetNumberOfPrims();

    integer i;
    for(i=2;i<=prims;i++)
    {
        key prim = llGetLinkKey(i);
        list tmp = llGetObjectDetails(prim,[OBJECT_NAME,OBJECT_DESC,OBJECT_ROT,OBJECT_POS]);
        string prim_name = llList2String(tmp,0);
        string prim_descr = llList2String(tmp,1);
        rotation prim_rot = (rotation)llList2String(tmp,2);
        vector prim_pos = (vector)llList2String(tmp,3);

        door_num += [i];
        door_names += [prim_name];
        door_closed_rot += [prim_rot];
        door_open += [FALSE];
        door_open_time += [0];
        if(prim_descr == "right")
            door_direction += [TRUE];
        else
            door_direction += [FALSE];
        door_acl += [""];
        door_pos += [prim_pos];
    }
    llSetText("...done!",<1,1,1>,1.0);
    reload_acl();
}

string config = "config";//name of the configuration file
integer nLine = 0;//current line we are reading

//this function re read the config notecard and populate the
//user list and acl table
reload_acl()
{

    llSetText("reloading access controls...",<1,1,1>,1.0);
    is_active = FALSE;
    nLine = 0;
    //remove all acl
    integer i;
    for(i=0;i *DEG_TO_RAD));
    else
        open = llEuler2Rot(llRot2Euler(closed)+ (<0,0,-90> *DEG_TO_RAD));
    llSetLinkPrimitiveParams(linknum,[PRIM_ROTATION,open]);

    door_open_time = llListReplaceList(door_open_time,[llGetUnixTime()],index,index);
    door_open = llListReplaceList(door_open,[TRUE],index,index);

    llSetTimerEvent(1.0);
}

//those 3 functions rez a sound emitter with it's destination position encoded in integer
play_open(vector pos)
{
    llRezObject("open",llGetPos(),ZERO_VECTOR,ZERO_ROTATION,vec2int(pos));
}
play_close(vector pos)
{
    llRezObject("close",llGetPos(),ZERO_VECTOR,ZERO_ROTATION,vec2int(pos));
}
play_lock(vector pos)
{
    llRezObject("lock",llGetPos(),ZERO_VECTOR,ZERO_ROTATION,vec2int(pos));
}

default
{
    touch_start(integer total_number)
    {
        integer userid;

        if(!is_active)
            return;

        //considering we MAY receive more than one touch at the same time since
        //we can manage many doors.
        for(userid=0;userid activation_distance )
                llInstantMessage(llDetectedKey(userid),"You can't use this from this distance.");
            else
            {
                if(is_open)
                {   //if the door is open, simply play sound and close it.
                    play_close(door_vec);
                    close(door_index);
                }
                else
                {
                    string acl_string = llList2String(door_acl,door_index);

                    //if the acl string is empty for this door we simply open it
                    if(acl_string == "") //no specific locking
                    {
                        play_open(door_vec);
                        open(door_index);
                    }
                    else
                    {
                        //otherwise we lookup if the userid that correspond to the person who touched
                        //the door match any of the ones in the ACL string
                        integer user_index = llListFindList(user_indexes,[clicker_name]);

                        if(user_index == -1)  //we don't even know this user? sure as hell there is no acl about him
                            play_lock(door_vec);
                        else
                        {
                            list acl_list =  llParseString2List(acl_string,[","],[]);

                            if(llListFindList(acl_list,[(string)user_index]) != -1)
                            {
                                play_open(door_vec);
                                open(door_index);
                            }
                            else
                                play_lock(door_vec);
                        }
                    }
                }
            }
        }
    }
    dataserver(key id,string data)
    {
        //notecard reading stuff
        if(data != EOF)
        {
            if(data != "" && data != " " && llGetSubString(data,0,1) != "//")
            {
                list command_and_data = llParseString2List(data,["="],[]);
                string door_name = llList2String(command_and_data,0);
                string user_names_string = llList2String(command_and_data,1);

                integer index = llListFindList(door_names,[door_name]);
                if(index != -1)
                {
                    list user_names_list = llParseString2List(user_names_string,[","],[]);
                    integer j;

                    list pre_acl_list;
                    for(j=0;j,.5);
        }
    }
    state_entry()
    {
        recount_doors();
    }
    changed(integer change)
    {
        //if we detect an inventory change we reread the notecard
        //if we detect a linkchange we reset the script and recount doors first
        if( (change & CHANGED_INVENTORY) == CHANGED_INVENTORY)
            reload_acl();
        if( (change & CHANGED_LINK) == CHANGED_LINK)
            llResetScript();
    }
    timer()
    {
        //timer will run once a second as long as at least one door is open.
        if(llListFindList(door_open,[TRUE]) == -1)
        {
            llSetTimerEvent(0.0);
            return;
        }
        integer i;

        //each run of the timer we loop through the timestamps to check if one of them is too old
        //(which means we can force close the associated door
        for(i=0;i

You need this script in the 3 rezzable objects "open" "close" and "lock" in order to play your door sounds at the right place (At the time i wrote this , lsl doesn't allow yet to play sounds from an unscripted prim in a link set)

```lsl
string sound_to_play = "my door sound";// put your sound name/key here

//This functions is from Nomad Padar, pretty awesome!
//decode from integer to vector
vector int2vec(integer n)
{
    //0zyx ZZZZ ZZZZ ZZZZ YYYY YYYY XXXX XXXX
    return >8)&0xFF, ((n>>16)&0xFFF)> + <((n&0x10000000)!=0)*.5,((n&0x20000000)!=0)*.5,((n&0x40000000)!=0)*.5>;
}

default
{
    state_entry()
    {
        llSetStatus(STATUS_PHANTOM, TRUE);
        llSetPrimitiveParams([PRIM_TEMP_ON_REZ, TRUE]);
        llSetTexture(TEXTURE_TRANSPARENT,ALL_SIDES);
    }
    on_rez(integer a)
    {
        if(a == 0)
            return;

        vector destination = int2vec(a);

        integer i;
        for(i=0 ; i<50 && (llGetPos() != destination) ; i++)
            llSetLinkPrimitiveParamsFast(0, [PRIM_POSITION, destination]);

        if(llGetPos() == destination)
            llTriggerSound(sound_to_play,1.0);
        llDie();
    }
}
```

Example "config" notecard:

```lsl
//lines starting with "//" are ignored
//Syntax: one line per door in the format door_name=user name,user name
```

```lsl
My fancy front door=Kyrah Abattoir
My secret playroom door=Kyrah Abattoir,Timeless Prototype
```

```lsl
//of course if you want to lock a door from anybody you can set it to something like this:
```

```lsl
Mine entrance=condemned until further notice
```

--Kyrah Abattoir 18:46, 7 March 2010 (UTC)