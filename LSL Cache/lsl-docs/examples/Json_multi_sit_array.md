---
name: "Json multi sit array"
category: "example"
type: "example"
language: "LSL"
description: "With the new Json support, we can now have forms of arrays instead of single line lists. For this example I have written a Json Object based array for storing keys and positions of sitting avatars on a child prim. This object allows you to sit multiple avatars on a child prim however, it won't work on an object like a vehicle that requires a root key to drive the object. For that I'd recommend using llLinkSitTarget from the root and assigning an offset to the passenger seats."
wiki_url: "https://wiki.secondlife.com/wiki/Json_multi_sit_array"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

Introduction

With the new Json support, we can now have forms of arrays instead of single line lists. For this example I have written a Json Object based array for storing keys and positions of sitting avatars on a child prim. This object allows you to sit multiple avatars on a child prim however, it won't work on an object like a vehicle that requires a root key to drive the object. For that I'd recommend using llLinkSitTarget from the root and assigning an offset to the passenger seats.

Usage

To use this script just create a new script in the child prim that will be used as the primary seat for people and drop the code from below into it. This script will keep track of what avatar is sitting where and will assign an avatar to the next empty seat accordingly.

The Code

This script utilizes the new Json array object to store multiple keys to arrays with its position offset and twist on the z axis. It is for demonstration purposes and can be used in whatever product you want :) please share this page for learning and enjoy.

```lsl
//multi sit prim using Json Arrays (expects 6 seats)
//written by To-mos Codewarrior(tomos.halsey)
string SEATS_data;
list getFreeSeat()
{
    string avi;integer i=llGetNumberOfPrims();
    list avatarCheck;list sittingAvis;
    integer listIndex;string newAvi;
    integer newAviFlag=FALSE;
    //get current avatars on seat
    for (;i--;)
    {
        if(llGetAgentSize(llGetLinkKey(i+1)) != ZERO_VECTOR)
        {avatarCheck += [llGetLinkKey(i+1)];}
    }
    //llOwnerSay("Current Avatars: "+llList2CSV(avatarCheck));
    //run garbage cleaning loop to dump dead keys
    //and store the existing ones for checking
    for(i=6;i--;)
    {
        avi=llJsonGetValue(SEATS_data,["seat"+(string)i,"key"]);
        if(avi!="empty")
        {//if avi isn't on the list set it to empty
            listIndex=llListFindList(avatarCheck,[(key)avi]);
            if(!~listIndex)
                SEATS_data=llJsonSetValue(SEATS_data,["seat"+(string)i,"key"],"empty");
            else
                sittingAvis+=avi;
        }
    }
    //identify the new key
    i=llGetListLength(avatarCheck);
    for(;i--;)
    {
        listIndex=llListFindList(sittingAvis,[llList2String(avatarCheck,i)]);
        if((!~listIndex)&&!newAviFlag)
        {
            newAviFlag=TRUE;
            newAvi=llList2String(avatarCheck,i);
            //llOwnerSay("The new avatar is: "+newAvi);
        }
    }
    //check their numbers
    if(llGetListLength(avatarCheck)>6)
    {
        if(newAvi!="")
            llSay(0,"Too many avatars are on me, please get off "+llKey2Name(newAvi));
        else
            llSay(0,"More avatars need to get off me.");
        return ["full"];
    }
    //no need to go further after cleaning
    //up the array and have empty newAvi
    if(newAvi=="")return ["none"];
    //llOwnerSay("New avatar is: "+(string)newAvi);
    //now find first instance of empty to dump the new key
    //reset the new avi flag for the next loop
    newAviFlag=FALSE;
    for(i=6;i--;)
    {
        avi=llJsonGetValue(SEATS_data,["seat"+(string)i,"key"]);
        if(avi=="empty"&&!newAviFlag)
        {
            SEATS_data=llJsonSetValue(SEATS_data,["seat"+(string)i,"key"],(string)newAvi);
            //just use avatarCheck list as a temp variable for the output
            avatarCheck=[llJsonGetValue(SEATS_data,["seat"+(string)i,"pos"]),llJsonGetValue(SEATS_data,["seat"+(string)i,"twist"])];
            newAviFlag=TRUE;
        }
    }
    return avatarCheck;
}
default
{
    state_entry()
    {
        SEATS_data=llList2Json(JSON_OBJECT,
        [
            "seat0",llList2Json(JSON_OBJECT,["key","empty","pos",<0.734989, -1.202856, -0.018962>,"twist",-1.5706]),    //frontR
            "seat1",llList2Json(JSON_OBJECT,["key","empty","pos",<0.045105, -1.354009, -0.018962>,"twist",-1.5706]),    //middleR
            "seat2",llList2Json(JSON_OBJECT,["key","empty","pos",<-0.658836, -1.420682, -0.018962>,"twist",-1.5706]),//backR
            "seat3",llList2Json(JSON_OBJECT,["key","empty","pos",<0.734989, 1.202856, -0.018962>,"twist",1.5706]),  //frontL
            "seat4",llList2Json(JSON_OBJECT,["key","empty","pos",<0.045105, 1.354009, -0.018962>,"twist",1.5706]),  //middleL
            "seat5",llList2Json(JSON_OBJECT,["key","empty","pos",<-0.658836, 1.420682, -0.018962>,"twist",1.5706])     //backL
        ]);
        llSetClickAction(CLICK_ACTION_SIT);
        llSitTarget(<0.0,0.0,0.1>,ZERO_ROTATION);
    }
    changed(integer change)
    {
        if(change & CHANGED_LINK)
        {
            list output=getFreeSeat();
            if(output!=["full"]&&output!=["none"])
                llSetLinkPrimitiveParamsFast(llGetNumberOfPrims(),[PRIM_POS_LOCAL,(vector)llList2String(output,0),PRIM_ROT_LOCAL,llEuler2Rot(<0.0,0.0,llList2Float(output,1)>)]);

            //Debug draw array
            //llOwnerSay(SEATS_data);
        }
    }
}
```