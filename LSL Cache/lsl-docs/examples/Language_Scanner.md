---
name: "Language Scanner"
category: "example"
type: "example"
language: "LSL"
description: "User:Luxen_Resident | Teleporter_Anywhere | Ultimate_Radar | Language_Scanner | Visitor_Counter_Tracker"
wiki_url: "https://wiki.secondlife.com/wiki/Language_Scanner"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

User:Luxen_Resident | Teleporter_Anywhere | Ultimate_Radar | Language_Scanner | Visitor_Counter_Tracker

## Summary

Advanced language scanner to detect users language, distance and names on a Sim.

You can easily filter by language with the menu. Useful to find who speak your language.

## History

This version is optimized for the Language search.

- When a radar displays the nearest avatars, a language scanner need often to scan all the users so the script need to be a bit different than a radar...

## Code:

```lsl
//////////////////////////////////////////////////////////////////////////////
//                      Zx Language Scanner v5                              //
//                                                                          //
//                   By Luxen - Zonyx Technology                            //
//////////////////////////////////////////////////////////////////////////////

integer counter = 0;
key owner = NULL_KEY;
list LangAffich = ["Default", "English", "Danish", "German", "Spanish", "French", "Italian", "Hungarian", "Dutch", "Polish", "Portuguese", "Russian"];
integer ZxMenu = 0;
integer Zchan = -4552155;
integer listenHandle;
string Av_Lang = "Default";
string SLang = "en";

set_time(float Stime, string Stext, integer Scounter)
{
        llSetText(Stext, <0.667, 0.667, 0.667>, 1.0);
        if (Stime != 5.0) llSetTimerEvent(Stime);
        counter = Scounter;
}

default
{
    state_entry()
    {
        if(owner)  ;
        else
        {
            owner = llGetOwner();
            set_time(10.0, "[- Starting -]", 0);
            Zchan = 0x80000000 | (integer)("0x"+(string)llGetKey());
        }
        ZxMenu = 0;
    }

    on_rez(integer start_param)
    {
        llResetScript();
    }

    changed(integer change)
    {
        if(change & (CHANGED_REGION)) state teleport;
    }

    touch_start(integer total_number)
    {
        if (llGetAttached())
        {
            if (counter)
            {
                if (!ZxMenu)
                {
                    key Touch = llDetectedKey(0);
                    if (Touch == owner)
                    {
                        llListenRemove(listenHandle);
                        ZxMenu = 1;
                        counter = 0;
                        listenHandle = llListen(Zchan, "", owner, "");
                        llDialog(owner, "by Luxen, Zonyx technology - Used Memory: " + llGetSubString((string)llGetUsedMemory(), 0, 1) + "k"
                             + "\n "
                             + "\n - Language: " + Av_Lang
                             + "\n (to reopen the menu: to wait some seconds)", LangAffich, Zchan);
                    }
                }
            }
        }
    }

    listen(integer channel, string name, key id, string msg)
    {
        if (ZxMenu)
        {
            if (llGetAttached())
            {
                if (channel == Zchan && id == owner)
                {
                    integer CheckTab = llListFindList(LangAffich, [msg]);
                    if (~CheckTab)
                    {
                        llListenRemove(listenHandle);
                        ZxMenu = 0;
                        Av_Lang = llList2String(LangAffich, CheckTab);
                        SLang = llList2String(["en", "en", "da", "de", "es", "fr", "it", "hu", "nl", "pl", "pt", "ru"], CheckTab);
                    }
                }
            }
        }
    }

    timer()
    {
        if (ZxMenu)
        {
            if (ZxMenu > 3)
            {
                llListenRemove(listenHandle);
                ZxMenu = 0;
                llOwnerSay("Resetting listen...\nMenu Off");
            }
            else ++ZxMenu;
        }

        list AvatarsDetect = llGetAgentList(AGENT_LIST_REGION, []);
        integer numOfAvatars = llGetListLength(AvatarsDetect);
        if (!llGetAttached())
        {
            if (llGetObjectPrimCount(llGetKey()))
            {
                set_time(0.0, "[- Off -]", 0);
            }
        }
        else if (numOfAvatars < 2)
        {
            if (counter != 2) set_time(5.0, "[- Nobody -]", 2);
        }
        else if (numOfAvatars > 100) return;
        else
        {
            integer index;
            list NewTab = [];
            vector currentPos = llGetPos();
            integer Zfix = numOfAvatars;
            for (index = 0; index < Zfix; ++index)
            {
                key AvKey = llList2Key(AvatarsDetect, index);
                list AvPos = llGetObjectDetails(AvKey, [OBJECT_POS]);
                if (AvPos) NewTab += [llVecDist(currentPos, llList2Vector(AvPos, 0)), AvKey];
                else --numOfAvatars;
            }

            if (numOfAvatars > 1)
            {
                AvatarsDetect = [];
                NewTab = llListSort(NewTab, 2, TRUE);
                string mode = "[- " + Av_Lang + " -]";
                numOfAvatars *= 2;
                if (llGetAgentLanguage(owner) != SLang) Zfix = FALSE;
                integer Av_Count = 0;
                for(index = 0; index < numOfAvatars; index += 2)
                {
                    key id = llList2Key(NewTab, index + 1);
                    string DLang = (string)llGetAgentLanguage(id);
                    if (DLang == "en-us") DLang = "en";
                    if (DLang == SLang)
                    {
                        if (Zfix)
                        {
                            if (id == owner)
                            {
                                Zfix = FALSE;
                                jump Ignore;
                            }
                        }
                        string DName = llGetUsername(id);
                        if (DName) DName += " (" + DLang + "-" + (string)llList2Integer(NewTab, index) + "m)";
                        else DName = "???";
                        if (Av_Count > 9)
                        {
                            DName = mode + "\n" + DName;
                            if (llStringLength(DName) > 254) jump affich;
                            else mode = DName;
                        }
                        else mode += "\n" + DName;
                        ++Av_Count;
                    }
                    @Ignore;

                }
                @affich;
                NewTab = [];
                if (!Av_Count) mode = "[- " + Av_Lang + ": 0 -]";
                set_time(5.0, mode, 1);
            }
        }
    }
}

state teleport
{
    state_entry()
    {
        if (counter) set_time(10.0, "[- Searching -]", 0);
        state default;
    }

    on_rez(integer start_param)
    {
        llResetScript();
    }

    timer()
    {
        return;
    }
}
```