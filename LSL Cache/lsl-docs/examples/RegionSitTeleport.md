---
name: "RegionSitTeleport"
category: "example"
type: "example"
language: "LSL"
description: "It's a very simple and clean script to make quick sit/unsit teleport to given position based on reading current prim's description."
wiki_url: "https://wiki.secondlife.com/wiki/RegionSitTeleport"
author: "User:Vincent_Nacon"
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

- Created by User:Vincent_Nacon

## RegionSitTeleport

It's a very simple and clean script to make quick sit/unsit teleport to given position based on reading current prim's description.

```lsl
////////////////////////////////////////////////////////
//             Written by Vincent Nacon
//          Released into the Public Domain
//   I'm sick and tired of WarpPos and <0,0,0> bug.
//                    Feb 26th 2012
////////////////////////////////////////////////////////

//What to do?
//Just place position (in vector form) where you want to drop avatar at in the prim's description.

default
{
    changed(integer change)
    {
        vector targetPosition = (vector)llGetObjectDesc();

        key sittingAvatar = llAvatarOnSitTarget();

        if(sittingAvatar)
        {
            vector positionToReturnTo = llGetPos();

            llSetRegionPos(targetPosition);
            llUnSit(sittingAvatar);
            llSetRegionPos(positionToReturnTo);
        }
    }

    state_entry()
    {
        llSitTarget(<0.0, 0.0, 0.1>, ZERO_ROTATION);
    }
}
```