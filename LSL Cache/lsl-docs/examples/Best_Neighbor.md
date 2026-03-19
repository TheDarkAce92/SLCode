---
name: "Best Neighbor"
category: "example"
type: "example"
language: "LSL"
description: "Best Neighbor Ad Hiding Script"
wiki_url: "https://wiki.secondlife.com/wiki/Best_Neighbor_Ad_Hiding_Script"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

Best Neighbor Ad Hiding Script

## Introduction

Even after changes regulating the form of advertising billboards in Second Life, many users are still dissatisfied with the look of some ads.  As part of a "Best Neighbor" policy, some advertisers have agreed to hide their advertisements when nearby land owners are logged in.  Doran Zemlja was kind enough to release a script to do this under the open source GPL license.

```lsl
//  best neighbor.lsl: Best Neighbor Ad Hider
//  Copyright (C) 2009 Adam Wozniak and Doran Zemlja
//
//  This program is free software: you can redistribute it and/or modify
//  it under the terms of the GNU General Public License as published by
//  the Free Software Foundation, either version 3 of the License, or
//  (at your option) any later version.
//
//  This program is distributed in the hope that it will be useful,
//  but WITHOUT ANY WARRANTY; without even the implied warranty of
//  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//  GNU General Public License for more details.
//
//  You should have received a copy of the GNU General Public License
//  along with this program.  If not, see .
//
//  Adam Wozniak and Doran Zemlja
//  1352 Fourteenth St, Los Osos, CA 93402
//  adam-opengate@cuddlepuddle.org

//  Scan for owners on their own land within 96m
//  If any are found, go invisible by setting all alphas to 0.0
//  Otherwise go visible by setting all alphas to 1.0

//  This is a compromise solution to the "ad problem".  The hope is that
//  if the ad is invisible to nearby land owners, then they are less
//  likely to complain about the ad.

//  Adapted from an idea proposed by Temporal Mitra
//  in Arbor Project group chat.

//  And no, copying an idea is NOT theft.  Pepsi isn't stealing from Coke,
//  and I'm not stealing from toaster manufacturers when I design and build
//  my own kind of toaster, even if toast is a pretty neat idea.

//  force alpha value for all prims in linkset
setAlpha(float alpha)
{
    llSetLinkAlpha(LINK_SET, alpha, ALL_SIDES);
}

//  change visibility
changeVisibilityTo(integer inputInteger)
{
    if (inputInteger)
        setAlpha(1.0);

    else
        setAlpha(0.0);
}

default
{
    on_rez(integer start_param)
    {
        llResetScript();
    }

    state_entry()
    {
        changeVisibilityTo(TRUE);
        llSensorRepeat("", NULL_KEY, AGENT, 96.0, PI, 10);
    }

    sensor(integer num)
    {
        integer found = FALSE;

        integer i;
        do
        {
            key id = llDetectedKey(i);
            key landOwnerAtDetectedPos = llGetLandOwnerAt(llDetectedPos(i));

            if (id == landOwnerAtDetectedPos)
                found = TRUE;
        }
        while (++i < num);

        if (found)
            changeVisibilityTo(FALSE);
        else
            changeVisibilityTo(TRUE);
    }

    no_sensor()
    {
        changeVisibilityTo(TRUE);
    }
}
```

## See also

- Advertising in Second Life
- Script Library