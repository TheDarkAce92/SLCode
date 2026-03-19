---
name: "Target Crosshair HUD"
category: "example"
type: "example"
language: "LSL"
description: "A 2 prim HUD targets nearby players names, profiles and user key. Drop this into the root prim of 2 linked prims. Modify it to suit your particular use in another Hud, weapon, or whatever you want. <3 --Ackley Bing"
wiki_url: "https://wiki.secondlife.com/wiki/Target_Crosshair_HUD"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

A 2 prim HUD targets nearby players names, profiles and user key. Drop this into the root prim of 2 linked prims. Modify it to suit your particular use in another Hud, weapon, or whatever you want. <3 --Ackley Bing

```lsl
// Target Crosshair HUD
// by Ackley Bing
// Save this script into the root prim of 2 linked prims (2 ordinary wooden cube prims - linked)
//
// This is based on my Basic Target Scanner HUD
// (http://wiki.secondlife.com/wiki/Basic_Target_Scanner_HUD)
// Now you get a crosshair that follows your target
// thanks to Cerise Sorbet's HUD Dots Radar
// (http://wiki.secondlife.com/wiki/HUD_Dots_Radar)
//
// Changes in 0.5.1.2
// 1. UpdateCrosshair():
//    Bugs fixed where crosshair and hud info didn't match up.
//    Info still buggy sometimes.  Don't click too fast! :)
// 2. Identify():
//    Avatar list sort ascending.
//
// If you cant see the hud, Wear or Add again should fix the problem.

integer AgentListindex;
key HUDtarget;
string showName;
string legName;
string dispName;
key photoReq;
string missingtexture="1a6e02aa-23a8-7a5f-0525-44d724144f89";
float gFOV = 1.7320508075688774;
vector gOffScreen = <-1000., -1000., -1000.>;
integer HUDattachpoint=ATTACH_HUD_CENTER_1;
integer AgentCount()
{
    list AgentCountList;
    integer ownerindex;
    integer num_agents;
    AgentCountList=llGetAgentList(AGENT_LIST_REGION,[]);
    ownerindex=llListFindList( AgentCountList, (list)llGetOwner() );
    AgentCountList=llDeleteSubList( AgentCountList, ownerindex, ownerindex );
    num_agents = llGetListLength(AgentCountList);
    return num_agents;
}
key Identify(integer selected)
{
    list IdentifiedAgentList;
    integer ownerindex;
    key IdentifiedAgent;
    list nameParts;
    IdentifiedAgentList=llGetAgentList(AGENT_LIST_REGION,[]);
    ownerindex=llListFindList( IdentifiedAgentList, (list)llGetOwner() );
    IdentifiedAgentList=llDeleteSubList( IdentifiedAgentList, ownerindex, ownerindex );
    if ( llGetListLength(IdentifiedAgentList)==0 )
    {
        AgentListindex = 0;
        llSetText(" ", <1,1,1>, 1.0);
        llSetTexture(missingtexture, 0);
        return NULL_KEY;
    }
    else
    {
        IdentifiedAgentList=llListSort(IdentifiedAgentList, 1, TRUE);
        if ( selected>llGetListLength(IdentifiedAgentList) )
        {
            AgentListindex = 0;
            IdentifiedAgent = llList2Key(IdentifiedAgentList, 0);
        }
        else IdentifiedAgent = llList2Key(IdentifiedAgentList, selected);
        legName = llKey2Name(IdentifiedAgent);
        nameParts = llParseString2List(legName,[" "],[]);
        if (llList2String(nameParts, 1) == "Resident") legName = llList2String(nameParts, 0);
        showName = legName;
        dispName = llGetDisplayName(IdentifiedAgent);
        if (dispName) if (llToLower(dispName) != llToLower(legName)) llSetText(showName+"\n(" + dispName + ")\n"+(string)IdentifiedAgent, <1,1,1>, 1.0);
        else llSetText(showName+"\n"+(string)IdentifiedAgent, <1,1,1>, 1.0);
        llOwnerSay("("+(string)(AgentListindex+1)+"/"+(string)(AgentCount()) +") Current Target: secondlife:///app/agent/" + (string)IdentifiedAgent + "/inspect " + (string)IdentifiedAgent);
        photoReq=llHTTPRequest("http://world.secondlife.com/resident/"+(string)IdentifiedAgent,[],"");
        return IdentifiedAgent;
    }
}
UpdateCrosshair(key lockedtarget)
{
    if (lockedtarget!=NULL_KEY)
    {
        list SuspectList=llGetAgentList(AGENT_LIST_REGION,[]);
        integer lockedtargetindex=llListFindList( SuspectList, (list)lockedtarget );
        if (lockedtargetindex>-1)
        {
            vector cPos = llGetCameraPos();
            rotation cRot = llGetCameraRot();
            vector targetPos = llList2Vector(llGetObjectDetails(lockedtarget,[OBJECT_POS]),0);
            vector childPos = Region2HUD(targetPos + <0,0,0.5>, cPos, cRot);
            if (childPos!=gOffScreen)
            {
                vector myPos = llGetPos();
                float dist = llRound(llVecDist(myPos, targetPos));
                vector localhudpos = llGetLocalPos();
                string crosshairtext;
                localhudpos = ;
                if (dispName) if (llToLower(dispName) != llToLower(legName)) crosshairtext = showName+"\n( " + dispName + " )\n"+(string)((integer)dist)+"m";
                else crosshairtext = showName+"\n"+(string)((integer)dist)+"m";
                llSetLinkPrimitiveParamsFast(2,[PRIM_POSITION,childPos-localhudpos,PRIM_COLOR,ALL_SIDES,llVecNorm(),1,PRIM_TEXT,crosshairtext,llVecNorm(),1]);
            }
            else llSetLinkPrimitiveParamsFast(2,[PRIM_POSITION,<.02,0,0>,PRIM_COLOR,ALL_SIDES,llVecNorm(<0,0,0>),0,PRIM_TEXT,"",llVecNorm(<0,0,0>),0]);
        }
        else
        {
            llSetTimerEvent(0.0);
            AgentListindex = 0;
            llSetLinkPrimitiveParamsFast(2,[PRIM_POSITION,<.02,0,0>,PRIM_COLOR,ALL_SIDES,llVecNorm(<0,0,0>),0,PRIM_TEXT,"",llVecNorm(<0,0,0>),0]);
            llSetText(" ", <1,1,1>, 1.0);
            llSetTexture(missingtexture, 0);
        }
    }
    else
    {
        llSetLinkPrimitiveParamsFast(2,[PRIM_POSITION,<.02,0,0>,PRIM_COLOR,ALL_SIDES,llVecNorm(<0,0,0>),0,PRIM_TEXT,"",llVecNorm(<0,0,0>),0]);
        llSetTimerEvent(0.0);
    }
}
vector Region2HUD(vector objPos, vector camPos, rotation camRot)
{
    objPos = (objPos - camPos) * (ZERO_ROTATION / camRot);
    objPos = <-objPos.y, objPos.z, objPos.x>;
    float Xcrosshair = (objPos.x * gFOV) / objPos.z;
    if (Xcrosshair > -3. && Xcrosshair < 3.)
    {
        float Ycrosshair = (objPos.y * gFOV) / objPos.z;
        if (Ycrosshair > -1. && Ycrosshair < 1.)
        {
            float Zcrosshair = (objPos.z - 2) / objPos.z;
            if (Zcrosshair > -1. && Zcrosshair < 1.) return ;
        }
    }
    return gOffScreen;
}
default
{
    state_entry()
    {
        AgentListindex=0;
        HUDtarget=NULL_KEY;
        llSetScale(<0.1, 0.15, 0.1>);
        llSetPrimitiveParams([PRIM_TYPE, PRIM_TYPE_BOX, PRIM_HOLE_DEFAULT, <0.0, 1.0, 0.0>, 0.0, <0.0, 0.0, 0.0>, <2.0, 0.5, 1.0>, <0.0, 0.0, 0.0>, PRIM_ROT_LOCAL, <0.000000, -0.707107, 0.000000, 0.707107>, PRIM_COLOR, 0, <1.0,1.0,1.0>, 1.0, PRIM_COLOR, 1, <0.0,1.0,0.0>, 1.0, PRIM_COLOR, 3, <0.0,1.0,0.0>, 1.0, PRIM_COLOR, 2, <1.0,1.0,1.0>, 0.0, PRIM_COLOR, 4, <1.0,1.0,1.0>, 0.0]);
        llSetTexture(missingtexture, 0);
        llRotateTexture(270.0*DEG_TO_RAD,0);
        llSetText("", <0.0, 1.0, 0.0>, 1.0);
        llSetLinkPrimitiveParamsFast(2,[PRIM_POSITION,<.02,0,0>,PRIM_COLOR,ALL_SIDES,llVecNorm(<1,1,1>),0,PRIM_SIZE,<0.075,0.075,0.075>,PRIM_TEXT,"",llVecNorm(<0,0,0>),0,PRIM_TEXTURE, ALL_SIDES, "3e86b422-b3a9-c42d-bb87-044279cd4fd5", <1,1,1>, <0,0,0>, 0.0]);
        llSetTimerEvent(0.0);
        llRequestPermissions(llGetOwner(),PERMISSION_ATTACH|PERMISSION_TAKE_CONTROLS|PERMISSION_TRACK_CAMERA);
    }
    touch_start(integer n)
    {
        if ( llGetAttached() )
        {
            integer AgentTotal;
            AgentTotal = AgentCount();
            AgentListindex=AgentListindex+(llDetectedTouchFace(0)==1)-(llDetectedTouchFace(0)==3);
            AgentListindex = ((AgentListindex<0)*(AgentTotal-1))+((AgentListindex>=0)*(AgentListindex*(AgentListindex!=AgentTotal)));
            HUDtarget=Identify(AgentListindex);
            llSetTimerEvent(0.1);
        }
    }
    timer()
    {
        UpdateCrosshair(HUDtarget);
    }
    http_response(key request_id, integer status, list metadata, string body)
    {
        if( request_id == photoReq )
        {
            string photoID;
            integer StartIndex=llSubStringIndex(body,"");
            integer EndIndex=llSubStringIndex(body,"");
            if( StartIndex!=-1)
            {
                integer tempIndex=llSubStringIndex(body,"imageid")+18;
                if(tempIndex>17)photoID=llGetSubString(body,tempIndex,tempIndex+35);
            }
            if ( photoID==NULL_KEY || photoID=="" ) photoID=missingtexture;
            llSetTexture(photoID, 0);
        }
    }
    attach(key id)
    {
        if (id)
        {
            llSetScale(<0.1, 0.15, 0.1>);
            llSetPrimitiveParams([PRIM_TYPE, PRIM_TYPE_BOX, PRIM_HOLE_DEFAULT, <0.0, 1.0, 0.0>, 0.0, <0.0, 0.0, 0.0>, <2.0, 0.5, 1.0>, <0.0, 0.0, 0.0>, PRIM_ROT_LOCAL, <0.000000, -0.707107, 0.000000, 0.707107>, PRIM_COLOR, 0, <1.0,1.0,1.0>, 1.0, PRIM_COLOR, 1, <0.0,1.0,0.0>, 1.0, PRIM_COLOR, 3, <0.0,1.0,0.0>, 1.0, PRIM_COLOR, 2, <1.0,1.0,1.0>, 0.0, PRIM_COLOR, 4, <1.0,1.0,1.0>, 0.0]);
            llRotateTexture(270.0*DEG_TO_RAD,0);
            HUDattachpoint=llGetAttached();
            llRequestPermissions(llGetOwner(), PERMISSION_TAKE_CONTROLS|PERMISSION_TRACK_CAMERA);
        }
    }
    on_rez(integer param)
    {
        if ( !llGetAttached() )
        {
            AgentListindex=0;
            HUDtarget=NULL_KEY;
            UpdateCrosshair(HUDtarget);
            llRequestPermissions(llGetOwner(),PERMISSION_ATTACH);
        }
    }
    run_time_permissions(integer perms)
    {
        if ( perms & PERMISSION_ATTACH ) llAttachToAvatar(HUDattachpoint);
        if ( perms & PERMISSION_TAKE_CONTROLS ) llTakeControls(CONTROL_BACK, FALSE, TRUE);
    }
}
```