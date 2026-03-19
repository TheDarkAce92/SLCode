---
name: "Ultimate Radar"
category: "example"
type: "example"
language: "LSL"
description: "User:Luxen_Resident | Teleporter_Anywhere | Ultimate_Radar | Language_Scanner | Visitor_Counter_Tracker"
wiki_url: "https://wiki.secondlife.com/wiki/Ultimate_Radar"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

User:Luxen_Resident | Teleporter_Anywhere | Ultimate_Radar | Language_Scanner | Visitor_Counter_Tracker

## Summary

An advanced radar to detect avatars and their language on an entire region.

## Code:

```lsl
//////////////////////////////////////////////////////////////////////////////
//                      Zx Ultimate Radar Hud   v5                          //
//                                                                          //
//                     By Luxen - Zonyx Technology                          //
//////////////////////////////////////////////////////////////////////////////

integer counter = 0;
key owner = NULL_KEY;
integer RStat = TRUE;

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
            llSetMemoryLimit(40000);
            owner = llGetOwner();
            set_time(10.0, "[- Starting -]", 0);
        }
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
                set_time(0.0, "[- Off -]", 0);
                RStat = FALSE;
            }
            else if (!RStat)
            {
                set_time(10.0, "[- Starting -]", 0);
                RStat = TRUE;
            }
        }
    }

    timer()
    {
        list AvatarsDetect = llGetAgentList(AGENT_LIST_REGION, []);
        integer numOfAvatars = llGetListLength(AvatarsDetect);
        if (!llGetAttached())
        {
            if (llGetObjectPrimCount(llGetKey()))
            {
                set_time(0.0, "[- Off -]", 0);
                RStat = FALSE;
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
                string mode = "[- Sim: " + (string)(numOfAvatars -1) + " -]";
                numOfAvatars *= 2;
                for(index = 0; index < numOfAvatars; index += 2)
                {
                    key id = llList2Key(NewTab, index + 1);
                    if (Zfix)
                    {
                        if (id == owner)
                        {
                            Zfix = FALSE;
                            jump Ignore;
                        }
                    }
                    string DName = llGetUsername(id);
                    string DLang = "?";
                    if (DName)
                    {
                        DLang = llGetAgentLanguage(id);
                        integer Dlenght = llStringLength(DLang);
                        if (Dlenght == 2)  ;
                        else if (Dlenght == 5)
                        {
                            if (DLang == "en-us") DLang = "en";
                            else DLang = "xx";
                        }
                        else DLang = "xx";
                    }
                    else DName = "???";
                    DName += " (" + DLang + "-" + (string)llList2Integer(NewTab, index) + "m)";
                    if (index > 18)
                    {
                        DName = mode + "\n" + DName;
                        if (llStringLength(DName) > 254) jump affich;
                        else mode = DName;
                    }
                    else mode += "\n" + DName;
                    @Ignore;

                }
                @affich;
                NewTab = [];
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