---
name: "Group Privacy"
category: "example"
type: "example"
language: "LSL"
description: "Many landlords do not allow residents to have security devices that are continuously operating. This device is activated manually, and only operates so long as avatars are present. When avatars leave the vicinity, the device turns off. To turn on again, the device needs to be touched by an authorised person."
wiki_url: "https://wiki.secondlife.com/wiki/Group_Privacy"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

Many landlords do not allow residents to have security devices that are continuously operating. This device is activated manually, and only operates so long as avatars are present. When avatars leave the vicinity, the device turns off. To turn on again, the device needs to be touched by an authorised person.

Place this script into a single prim, and decorate to taste.

Requirements:

1. Edit script range and timer frequency to suit
1. Deed to match the land group

Operation:

1. Insure that group members have the group tag active
1. Touch to activate; touch to deactivate

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

float duration = 60.0;          // Duration of Land Ban Following the Eject (1Hr)
float RANGE = 40.0;             // Scan Range (40m)
float RATE = 10.0;              // Scan Rate (10 Sec)

integer status;

off()
{
    status = FALSE;
    llSensorRemove();
    llSetColor(<1,1,1>, ALL_SIDES);
    llSay(0, "Deactivated.");
    llSetText("Group Privacy\nOff\n\nTouch to Turn On", <1,1,1>, 1);
}

on()
{
    status = TRUE;
    llSensorRepeat("", NULL_KEY, AGENT, RANGE, PI, RATE);
    llSetColor(<1,0,0>, ALL_SIDES);
    llSay(0, "Activated while group memebers are present.");
    llSetText("Group Privacy\nOn\n\nTouch to Turn Off", <1,1,1>, 0.5);
}

boot(key id)
{
    if (llOverMyLand(id) == TRUE)
    {
        llUnSit(id);
        llEjectFromLand(id);
        llAddToLandBanList(id, duration); // Hour of Ban
    }
}

default
{
    state_entry()
    {
        off();
    }

    touch_start(integer num_detected)
    {
        if (llGetLandOwnerAt(llGetPos()) != llGetOwner())
            llSay(0, "Deed device to match land group.");
        else
        {
            if (llSameGroup(llDetectedKey(0)))
            {
                if (status)
                    off();
                else
                    on();
            }
            else
                llSay(0, "Authorized to group members only.");
        }
    }

    sensor(integer num_detected)
    {
        integer group_members;
        key id;

        integer i;
        for ( ; i < num_detected; ++i)
        {
            id = llDetectedKey(i);

            if (llSameGroup(id))
            {
                llRemoveFromLandBanList(id);
                ++group_members;
            }
            else
                boot(id);
        }

        if (!group_members)
            off();
    }

    no_sensor()
    {
        off();
    }
}
```