---
name: "Teleporter Anywhere"
category: "example"
type: "example"
language: "LSL"
description: "User:Luxen_Resident | Teleporter_Anywhere | Ultimate_Radar | Language_Scanner | Visitor_Counter_Tracker"
wiki_url: "https://wiki.secondlife.com/wiki/Teleporter_Anywhere"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

User:Luxen_Resident | Teleporter_Anywhere | Ultimate_Radar | Language_Scanner | Visitor_Counter_Tracker

## Summary

This teleporter can teleport anybody anywhere in your land, to an other Parcel or to an other Sim.

- Easy to use, Touch and menu system.

## Notes:

Setup:1. Rez the Teleporter on your land *(where you want your first location)* and up it to 1 meter above the floor. 1. Click on it to open the menu. 1. The *"Save Dest 1"* Button save the first destination coordinate. 1. The *"Dest name 1"* Button set the first destination name. 1. Take the teleporter in your inventory, and go to the second destination, rez it and up it to 1 meter above the floor. 1. Click on it to open the menu. 1. The *"Save Dest 2"* Button save the second destination coordinate. 1. The *"Dest name 2"* Button set the second destination name. 1. Take it in your inventory and Rez the Teleporter *(where you want on your land)*. 1. Click on it to open the Menu and choose the "Ready" Button. To use the teleporter: 1. click on the teleporter 1. click on one of the 2 links *(in the popup)* to teleport at the first or at the second destination. "Ready" Button: This button lock temporarily the setup menu: the setup menu will be unavailable until the next rez. Note: To allow avatars to teleport anywhere in your land: you need to allow the teleport feature in your Land Settings *(Options tab and Teleport routing)*: Anywhere *(teleports may arrive at any location on the parcel)*.

If your land is "Group owned", you can allow the teleport feature for this group only: to disallow the teleport feature in the Land Settings and to allow it for the Group: *Group Profile -> "Roles" section -> "Abilities" tab*...

## Code:

```lsl
//////////////////////////////////////////////////////////////////////////////
//                      Zx Teleporter Anywhere v5.1                         //
//                                                                          //
//                      By Luxen - Zonyx Technology                         //
//                                                                          //
//////////////////////////////////////////////////////////////////////////////

key owner = NULL_KEY;
integer New_Key = TRUE;
integer Ready = TRUE;
integer Zchan = -58846;
integer CTimer = FALSE;
integer ZxMenu = FALSE;
integer ZxText1 = FALSE;
integer ZxText2 = FALSE;
integer TOwner = FALSE;
integer TMember = FALSE;
string TDest1 = "Banyan/70/79/96";
string MDest1 = "Gadgets:";
string TDest2 = "Banyan/70/79/96";
string MDest2 = "Freebies:";
integer listenHandle;

FCTimer()
{
    if (CTimer)
    {
        llSetTimerEvent(0.0);
        CTimer = FALSE;
    }
}
ChangeColor(vector Tcolor)
{
    vector SColor = llGetColor(2);
    if (SColor != Tcolor) llSetColor(Tcolor, 2);
}
string SetDest(vector VDest)
{
    return llEscapeURL(llGetRegionName()) + "/" + (string)llRound(VDest.x) + "/" + (string)llRound(VDest.y) + "/" + (string)llRound(VDest.z);
}

default
{

    state_entry()
    {
        if (owner)  ;
        else
        {
            owner = llGetOwner();
            ChangeColor(<0.239, 0.600, 0.439>);
        }
        if (New_Key)
        {
            New_Key = FALSE;
            Ready = TRUE;
            Zchan = 0x80000000 | (integer)("0x"+(string)llGetKey());
        }
        FCTimer();
        ZxMenu = FALSE;
        ZxText1 = FALSE;
        ZxText2 = FALSE;
    }

    on_rez(integer start_param)
    {
        if (owner != llGetOwner()) llResetScript();
        else
        {
            New_Key = TRUE;
            state restart_scr;
        }
    }

    changed(integer change)
    {
        if (change & CHANGED_REGION_START)
        {
            llSleep(5.0);
            state restart_scr;
        }
    }

    touch_start(integer num_detected)
    {
        key ZTouch = llDetectedKey(0);
        integer Zpass = FALSE;
        if (TOwner)
        {
            if (ZTouch == owner) Zpass = TRUE;
        }
        else if (TMember)
        {
            integer ObjectGroup = FALSE;
            list details = llGetObjectDetails(llGetKey(),[OBJECT_GROUP]);
            if (llList2Key(details, 0)) ObjectGroup = TRUE;
            if (llSameGroup(ZTouch) && ObjectGroup) Zpass = TRUE;
            else if (ZTouch == owner) Zpass = TRUE;
        }
        else Zpass = TRUE;

        if (Zpass)
        {
            string Dest = "\n " + "\n " + MDest1
                      + "\n " + "secondlife:///app/teleport/" + TDest1
                      + "\n " + "\n " + MDest2
                      + "\n " + "secondlife:///app/teleport/" + TDest2;
            if (Ready)
            {
                if (ZTouch == owner)
                {
                    Dest = "- Click on the links below -"
                    + "\n (Buttons are only visible to the Owner)" + Dest;
                    llListenRemove(listenHandle);
                    llSetTimerEvent(120.0);
                    CTimer = TRUE;
                    list Teleport_Tab = ["Public", "Member Only", "Owner Only", "Dest Name 1", "Save Dest 2", "Dest Name 2", "Reset", "Ready", "Save Dest 1", "Close"];
                    llDialog(ZTouch, Dest, Teleport_Tab , Zchan);
                    listenHandle = llListen(Zchan, "", owner, "");
                    ZxMenu = TRUE;
                    return;
                }
            }
            Dest = "- Click on the links below -" + Dest;
            llDialog(ZTouch, Dest, ["Close"], -5958);
        }
    }

    listen(integer channel, string name, key id, string msg)
    {
        if (ZxMenu)
        {
            if(channel == Zchan && id == owner)
            {
                integer Tmsg = llStringLength(msg);
                if (Tmsg < 50)
                {
                    if (msg == "Public")
                    {
                        TOwner = FALSE;
                        TMember = FALSE;
                        ChangeColor(<0.239, 0.600, 0.439>);
                    }
                    else if (msg == "Member Only")
                    {
                        TOwner = FALSE;
                        TMember = TRUE;
                        ChangeColor(<0.000, 0.455, 0.851>);
                    }
                    else if (msg == "Owner Only")
                    {
                        TOwner = TRUE;
                        TMember = FALSE;
                        ChangeColor(<1.000, 0.255, 0.212>);
                    }
                    else if (msg == "Reset")
                    {
                        llSleep(0.5);
                        llResetScript();
                    }
                    else if (msg == "Ready") Ready = FALSE;
                    else if (msg == "Close")  ;
                    else if (msg == "Save Dest 2")
                    {
                        vector VDest2 = llGetPos();
                        TDest2 = SetDest(VDest2);
                    }
                    else if (msg == "Dest Name 2")
                    {
                        llTextBox(owner, "Type the name of the destination 2... (Max: 50)", Zchan);
                        ZxText2 = TRUE;
                        ZxText1 = FALSE;
                        return;
                    }
                    else if (msg == "Save Dest 1")
                    {
                        vector VDest1 = llGetPos();
                        TDest1 = SetDest(VDest1);
                    }
                    else if (msg == "Dest Name 1")
                    {
                        llTextBox(owner, "Type the name of the destination 1... (Max: 50)", Zchan);
                        ZxText1 = TRUE;
                        ZxText2 = FALSE;
                        return;
                    }
                    else if (ZxText1)
                    {
                        msg = llStringTrim(msg, STRING_TRIM);
                        if (msg) MDest1 = msg;
                    }
                    else if (ZxText2)
                    {
                        msg = llStringTrim(msg, STRING_TRIM);
                        if (msg) MDest2 = msg;
                    }
                    else return;
                    llListenRemove(listenHandle);
                    state restart_scr;
                }
            }
        }
    }

    timer()
    {
        llWhisper(0,"Resetting listen...\nMenu Off");
        state restart_scr;
    }
}

state restart_scr
{
    state_entry()
    {
        state default;
    }

    on_rez(integer start_param)
    {
        if (owner != llGetOwner()) llResetScript();
        else
        {
            New_Key = TRUE;
            state default;
        }
    }
}
```