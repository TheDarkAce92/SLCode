---
name: "Multi-displays Texture Cycler"
category: "example"
type: "example"
language: "LSL"
description: "1. Display all textures in sequence, distributed to all screens in the set. 1. Internal delay between each screen, to give viewer some time to load 1. Single script!"
wiki_url: "https://wiki.secondlife.com/wiki/Multi-displays_Texture_Cycler"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

## Features

1. Display all textures in sequence, distributed to all screens in the set.
1. Internal delay between each screen, to give viewer some time to load
1. Single script!

## Usage

1. Link all screens into a linkset, with another root prim separate from the screens.
1. Name all the screens as **DISPLAY#n**, where *n* is a number, starting from 1, 2, 3, ...
1. Put all textures into the root prim
1. Put the script in last
1. Texture will be displayed on Side#1 of the prim. Make sure it is faced right.

## Scripts

```lsl
float cycleTimer = 30;
list displays;
integer totalDisplays;

integer currentTexture = 0;

displayOff(integer link){
    llSetLinkPrimitiveParamsFast(link, [
        PRIM_COLOR, 1, <0,0,0>, 1,
        PRIM_TEXTURE, 1, TEXTURE_BLANK, <1,1,0>, <0,0,0>, 0
    ]);
}

displayOn(integer link, string name, key texture){
    llSetLinkPrimitiveParamsFast(link, [
        PRIM_COLOR, 1, <1,1,1>, 1,
        PRIM_TEXTURE, 1, texture, <1,1,0>, <0,0,0>, 0,
        PRIM_TEXT, name, <1,1,1>, 1
    ]);
}

showTextures(){
    integer count = llGetInventoryNumber(INVENTORY_TEXTURE);
    if(count < 1) return;

    integer i;
    for(i=0; i0; --i){
            if(llGetSubString((name = llGetLinkName(i)), 0, 7) == "DISPLAY#"){
                num = (integer)llGetSubString(name, 8, -1);

                // Force the ID into link list
                while(llGetListLength(displays) < num) displays += [0];
                displays = llListReplaceList(displays, [i], num - 1, num - 1);

                // Prepare display screen
                displayOff(i);
            }
        }

        totalDisplays = llGetListLength(displays);
        if(totalDisplays < 1)
            llOwnerSay("ERROR: No target display found! Please name target prims as \"DISPLAY#1\", \"DISPLAY#2\", ..., \"DISPLAY#n\"");
        else llSetTimerEvent(cycleTimer);
    }

    timer(){
        showTextures();
    }
}
```