---
name: "Visitor Counter Tracker"
category: "example"
type: "example"
language: "LSL"
description: "User:Luxen_Resident | Teleporter_Anywhere | Ultimate_Radar | Language_Scanner | Visitor_Counter_Tracker"
wiki_url: "https://wiki.secondlife.com/wiki/Visitor_Counter_Tracker"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

User:Luxen_Resident | Teleporter_Anywhere | Ultimate_Radar | Language_Scanner | Visitor_Counter_Tracker

## Summary

Track, save and display the list of all the visitors names each day.

- Daily report
- Land wide (scan all your Land)
- Easy to use, no setup needed
- Fully autonomous.

## Code:

```lsl
//////////////////////////////////////////////////////////////////////////////
//                      Zx Visitor Counter - Tracker v3.1                   //
//                                                                          //
//                        By Luxen - Zonyx Technology                       //
//                                                                          //
//////////////////////////////////////////////////////////////////////////////

key Zowner;
integer NVisits;
string ZDate;
integer DCount = 0;
list NewTab  = [];
list IdTab = [];

string Ztime()
{
    string DayDate = llGetSubString(llGetDate(), 8, 9);
    return DayDate;
}
Zcount()
{
    string Ztext = "[D:" + (string)DCount + " - M:" + (string)NVisits + "]";
    llSetPrimitiveParams([PRIM_TEXT, Ztext, <0.667, 0.667, 0.667>, 1.0]);
}
string Zreport(integer Ztab, integer Tcount)
{
    string Fname = "";
    integer index2;
    for(index2 = 0; index2 < Tcount ; ++index2)
    {
        if (Ztab) Fname += llList2String(NewTab, index2) + ", ";
        else Fname += "secondlife:///app/agent/" + llList2String(IdTab, index2) + "/username" + ", ";
    }
    return llDeleteSubString(Fname, -2, -1);
}
integer Zadd(key Zkey, string Zname)
{
    if (Zname)
    {
        if (llListFindList(NewTab, [Zname]) == -1) NewTab += [Zname];
        else return FALSE;
    }
    else
    {
        if (llListFindList(IdTab, [Zkey]) == -1) IdTab += [Zkey];
        else return FALSE;
    }
    return TRUE;
}

default
{
    state_entry()
    {
        Zowner = llGetOwner();
        NVisits = (integer)llGetObjectDesc();
        ZDate = Ztime();
        Zcount();
        llSetTimerEvent(60.0);
    }

    on_rez(integer start_param)
    {
        llSetObjectDesc("0");
        llResetScript();
    }

    touch_start(integer n)
    {
        if (llDetectedKey(0) == Zowner)
        {
            llSleep(0.3);
            integer TnumOfAvatars = llGetListLength(NewTab);
            string Vname = "--------------------------"
                       + "\n Visitors Today:"
                       + "\n List (" + (string)TnumOfAvatars + "): ";

            if (TnumOfAvatars > 0) Vname += Zreport(TRUE, TnumOfAvatars);
            else Vname += "nobody";
            TnumOfAvatars = llGetListLength(IdTab);
            if (TnumOfAvatars > 0) Vname += "\n Others (" + (string)TnumOfAvatars + "): " + Zreport(FALSE, TnumOfAvatars);
            llOwnerSay(Vname + "\n --------------------------");
        }
    }

    changed(integer change)
    {
        if (change & CHANGED_REGION_START)
        {
            llSleep(60.0);
            llSetTimerEvent(60.0);
        }
    }

    timer()
    {
        integer UpDate = FALSE;
        list AvatarsDetect  = llGetAgentList(AGENT_LIST_PARCEL, []);
        integer numOfAvatars = llGetListLength(AvatarsDetect);
        if (numOfAvatars > 0)
        {
            integer ObjectGroup = FALSE;
            list details = llGetObjectDetails(llGetKey(),[OBJECT_GROUP]);
            if(llList2Key(details, 0)) ObjectGroup = TRUE;

            integer index;
            for (index = 0; index < numOfAvatars; ++index)
            {
                key id = llList2Key(AvatarsDetect, index);
                if (llSameGroup(id) && ObjectGroup)  ;
                else if (id != Zowner)
                {
                    integer Znew = Zadd(id, llGetUsername(id));
                    if (Znew)
                    {
                        UpDate = TRUE;
                        ++DCount;
                        ++NVisits;
                    }
                }
            }
            AvatarsDetect = [];
        }

        if (ZDate != Ztime())
        {
            llSleep(1.0);
            ZDate = Ztime();
            if (ZDate == "01") llSetObjectDesc("0");
            else llSetObjectDesc((string)NVisits);
            llResetScript();
        }
        else if (UpDate) Zcount();
    }
}
```