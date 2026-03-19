---
name: "Under Age Boot"
category: "example"
type: "example"
language: "LSL"
description: "Security device example to teleport home accounts below a minimum age limit; can be useful in combating free griefer accounts."
wiki_url: "https://wiki.secondlife.com/wiki/Under_Age_Boot"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

Security device example to teleport home accounts below a minimum age limit; can be useful in combating free griefer accounts.

Place this script into a single prim and decorate to taste.

Requirements:

1. Deed to match the land group
1. Place the prim reasonably close to the parcel landing point
1. Set the prim description field to be the minimum age accounts; must be in days

Operation:

1. No special instructions. It operates stand alone once installed.

```lsl
//////////////////////////////////////////////////////////////////////////////////////
//
//    Version 1.0 Release
//    Copyright (C) 2007, Chance Unknown
//
//    This library is free software; you can redistribute it and/or
//    modify it under the terms of the GNU Lesser General Public License
//    as published by the Free Software Foundation; either
//    version 2.1 of the License, or (at your option) any later version.
//
//    This library is distributed in the hope that it will be useful,
//    but WITHOUT ANY WARRANTY; without even the implied warranty of
//    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//    GNU Lesser General Public License for more details.
//
//    You should have received a copy of the GNU Lesser General Public License
//    along with this library; if not, write to the Free Software
//    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
//
//////////////////////////////////////////////////////////////////////////////////////

// Set the age in the description field of the prim to reflect the SL account age
// of individuals to boot.

integer AGE_LIMIT;
list agent_list;

integer date2days(string data)
{
    integer result;
    list parse_date = llParseString2List(data, ["-"], []);
    integer year = llList2Integer(parse_date, 0);

    result = (year - 2000) * 365; // Bias Number to year 2000 (SL Avatars Born After Date)
    list days = [ 0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334 ];

    result += llList2Integer(days, (llList2Integer(parse_date, 1) - 1));

    //Fixed the leap year calculation below  ~Casper Warden, 28/10/2015.
    //if (year/4 == llRound(year/4)) result += 1;
    result += llFloor((year-2000) / 4);

    result += llList2Integer(parse_date, 2);

    return result;
}

default
{
    on_rez(integer param)
    {
        llResetScript();
    }

    state_entry()
    {
        AGE_LIMIT = (integer)llGetObjectDesc();

        if (AGE_LIMIT < 2)
        {
            AGE_LIMIT = 2;
        }

        llSetObjectName("Unknown Underage Boot - " + llGetRegionName());
        llVolumeDetect(TRUE);
        if (llOverMyLand(llGetKey()) == FALSE)
        {
            llSay(0, "Requires proper group deeds to work on this land.");
        }
        llSensorRepeat("", "", AGENT, 100.0, PI, 1.0);
        llOwnerSay("Set Avatar age in the description, currently it is set for " +
            (string)AGE_LIMIT + " days.");
    }

    sensor(integer num_detected)
    {
        if (llOverMyLand(llGetKey()) == FALSE)
        {
            return;
        }

        integer i;

        for (i = 0; i < num_detected; i++)
        {
            key agent = llDetectedKey(i);
            if (llSameGroup(agent) == FALSE)
            {
                if (llListFindList(agent_list, [ agent ]) < 0)
                {
                    if (llGetListLength(agent_list) == 0)
                    {
                        agent_list += agent;
                        llRequestAgentData(llList2Key(agent_list, 0), DATA_BORN);
                    }
                    else
                    {
                        agent_list += agent;
                    }
                }
            }
        }
    }

    dataserver(key queryid, string data)
    {
        AGE_LIMIT = (integer)llGetObjectDesc();

        integer today = date2days(llGetDate());
        integer age = date2days(data);
        key agent = llList2Key(agent_list, 0);
        string name = llKey2Name(agent);

        if (AGE_LIMIT < 2)
        {
            AGE_LIMIT = 2;
            llSetObjectDesc((string)AGE_LIMIT + " : SET AGE LIMIT HERE");
        }

        if (name != "")
        {
            if ((today - age) < AGE_LIMIT)
            {
                if (llOverMyLand(agent))
                {
                    llSay(0, name + ", you are too young to be here.");
                    llTeleportAgentHome(agent);
                }
            }
            else
            {
            }
        }
        else
        {
            llTeleportAgentHome(agent);
        }

        agent_list = llDeleteSubList(agent_list, 0, 0);
        if (llGetListLength(agent_list) != 0)
        {
            llRequestAgentData(llList2Key(agent_list, 0), DATA_BORN);
        }
    }
}
```