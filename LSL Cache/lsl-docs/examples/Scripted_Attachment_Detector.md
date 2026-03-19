---
name: "Scripted Attachment Detector"
category: "example"
type: "example"
language: "LSL"
description: "Scripted Attachment Dectector.lsl - Linden Scripting Language (LSL) Version 1.0.2"
wiki_url: "https://wiki.secondlife.com/wiki/Scripted_Attachment_Detector.lsl"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

- 1 Description
- 2 Creator
- 3 Contributors
- 4 License
- 5 Disclaimer
- 6 Purpose
- 7 Documentation
- 8 Scripted Attachment Detector.lsl

Scripted Attachment Dectector.lsl - Linden Scripting Language (LSL)
Version 1.0.2

Description

This script will show up to 16 scripted avatars within the sensor's reach and display their name in hovertext. You may also touch the prim to get a list of the scripted avatars. It can also show their distances. It will reset when rezzed, worn, or transferred to a new owner. It is LSL & Mono compatible.

Please note: It does not show its owner, whether or not they are scripted.

It was written in LSLEditor.

Creator

- Bobbyb30 Swashbuckler -- Devolper

Contributors

If you modify/improve upon the script, please add your name here.

License

This work is hereby released in Public Domain.

Disclaimer

This program is distributed in the hope that it will be useful, but **WITHOUT ANY WARRANTY**; without even the implied warranty of **MERCHANTABILITY** or **FITNESS FOR A PARTICULAR PURPOSE**.

Purpose

- To display a hovertext of which avatars are scripted.

Documentation

Create a prim. Drop this script in. Modify the global user variables. Compile in mono. Attach of leave as rezzed prim. Enjoy.=D

Scripted Attachment Detector.lsl

```lsl
//***********************************************************************************************************
//                                                                                                          *
//                                     --Scripted Attachment Detector--                                     *
//                                                                                                          *
//***********************************************************************************************************
// www.lsleditor.org  by Alphons van der Heijden (SL: Alphons Jano)
//Creator: Bobbyb30 Swashbuckler
//Attribution: None required, but it is appreciated.
//Created: December 13, 2009
//Last Modified: December 13, 2009
//Released: Tuesday, December 15, 2009
//License: Public Domain

//Status: Fully Working/Production Ready
//Version: 1.0.2

//Name: Scripted Attachment Detector.lsl
//Purpose: To show scripted avatars within the sensor's radius
//Technical Overview: Uses a sensor and exclusion list.
//Description: This script will shows scripted avatars within the sensor's reach and display their name in hovertext.
//             You may also touch the prim to get a list of the avatars. It can also show their distances. It will
//             reset when rezzed, or first worn.
//Directions: Create a prim. Place this script in the prim. Modify the parameters as needed. Save the script. Enjoy.
//Compatible: Mono & LSL compatible
//Other items required:
//Notes: Uses a sensorrepeat. This will cover up to 16 avatars that are in range.
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

/////////////////////////
//global user variables, you may change these

//hovertext
vector hovercolor = <1.0,1.0,1.0>;//color of hovertext
float hoveralpha = 1.0;//alpha of hovertext, 1 for solid, or 0 to not show hovertext

//sensor
float range = 96.0;//how far to scan out in meters up to 96...(this is the radius)
float interval = 30.0;//how often to scan for in seconds

//distance
integer showdistance = TRUE;//TRUE/FALSE whether to show the distance of the avatar next to their name
//example: Billy Joe (4m)

//exclude list
// CaSe does *NOT* matter, but spelling counts!
list exclude = ["John Doe","Santa Clause","Barrack Obama","Homeland Security", "Saddam Hussain","Big Oil"];//'people' to exclude

///////////////////////////////////
//global variables...don't change below
list scriptedavatars;//names of avatars who are scripted
list correctedexclusion;//the exclusion list in lowercase+owner

///////////////////
//user functions, dont change
hovertext(string input)//sets the hovertext
{
    llSetText(input,hovercolor,hoveralpha);
}

default
{
    on_rez(integer start_param)
    {
        if(!llGetAttached())//its not attatched, but was rezzed on the ground
            llResetScript();
    }
    attach(key attached)
    {
        if(attached != NULL_KEY)//they just put it on
            llResetScript();
    }
    state_entry()
    {
        llSensorRepeat("","",AGENT,range,TWO_PI,interval);//scan every so many seconds

        //add owner to exclude list
        exclude += llKey2Name(llGetOwner());

        //correct case on exclude list to lowercase and copy to correctexclusion list
        integer counter;
        integer excludelength = llGetListLength(exclude);
        do
        {
            correctedexclusion += llToLower(llList2String(exclude,counter));//add lowercase version to corrected exclusion
        }while(++counter < excludelength);

        //empty the exclude list to save memory
        exclude = [];//clears exclude list
        llOwnerSay("Scripted Attatchment.lsl (Public Domain 2009) by Bobbyb30 Swashbuckler running.");
        llOwnerSay("I will scan " + (string)llRound(range) + "m every " + (string)llRound(interval) + " seconds.");

    }
    touch_start(integer total_number)
    {
        if(llDetectedKey(0) == llGetOwner())//make sure owner touched
            llOwnerSay("The following avatar(s) have scripted attatchments: \n" +
            llDumpList2String(scriptedavatars,", "));//if you want one per line, do "\n"
    }
    sensor(integer total_number)//avatars were found
    {
        //llOwnerSay((string)llGetListLength(exclude));

        //set scriptedavatars to nothing, and then rebuild list based on new finds
        scriptedavatars = [];//clean up old list

        //build scriptedavatars list
        integer counter;
        vector mypos = llGetPos();//for use in determining distance, faster to call once, though less accurate I guess
        do
        {
            string detectedavatarname = llDetectedName(counter);//avatar name
            if(llListFindList(correctedexclusion,[llToLower(detectedavatarname)]) == -1)//check if they are excluded
            {
                if(llGetAgentInfo(llDetectedKey(counter)) & AGENT_SCRIPTED)//if the agent is scripted, add to list
                {
                    if(showdistance)//if showdistance == TRUE, append detectedavatarname with avatar distance
                        detectedavatarname += "(" + (string)llRound(llVecDist(llDetectedPos(counter),mypos)) + ")";//add avatar distance
                    scriptedavatars += detectedavatarname;//not excluded and scripted so add to list
                }
            }
        }while(++counter < total_number);
        //end of build

        //display scripted avatars in hovertext if any

        //get the length of scriptedavatars list to see if anyone was scripted
        integer scriptedavatarslength = llGetListLength(scriptedavatars);//

        if(scriptedavatarslength)//the list isn't empty so someone must have been scripted
            hovertext("* " + (string)llGetListLength(scriptedavatars) + " scripted avatars found *\n" +
            llDumpList2String(scriptedavatars,"\n"));//set the hovertext to display the scripted avatars, will truncate at x chrs
        else//no scripted avatars found
            hovertext("* No scripted avatars found *");
    }
    no_sensor()//this shouldn't trigger as its meant to be an attatchment, but if no avatars, this will trigger
    {
        hovertext("* No avatars detected *");//display no avatars for hovertext
    }
    changed(integer change)
    {
        if(change & CHANGED_OWNER)//new owner, reset script
            llResetScript();
    }
}
```