---
name: "Window Control"
category: "example"
type: "example"
language: "LSL"
description: "Window Control is basically just to change the opacity of windows and such, helpful for buildings."
wiki_url: "https://wiki.secondlife.com/wiki/Window_Control"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

- 1 What it does
- 2 Window
- 3 Window Switch
- 4 How to work with it

## What it does

Window Control is basically just to change the opacity of windows and such, helpful for buildings.

## Window

Put this in the windows;

```lsl
// script that changes opacity of object based on external messages

integer gChannel = 5; // communication channel on which we listen for opacity change commands
integer gLastListen; // id of last listen command

default
 {
     state_entry()
     {
         gLastListen = llListen(gChannel, "", "", "0");
     }

     listen(integer channel, string name, key id, string msg)
     {
         llListenRemove(gLastListen);

         integer nextOpacityLvl = (integer)msg;
         nextOpacityLvl += 1;
         if (nextOpacityLvl > 3) nextOpacityLvl = 0;
         gLastListen = llListen(gChannel, "", "", (string)nextOpacityLvl);

         float opacityLvl = (float)msg;
         opacityLvl = 1.1 - ((opacityLvl / 3) * 0.9);
         llSetAlpha(opacityLvl, ALL_SIDES);
     }
 }
```

## Window Switch

Put this in a switch;

```lsl
 // script for a switch that controls window opacity
 integer gOpacityLevel = 0; // current opacity level of windows
 integer gChannel = 5; // channel that controls which windows respond to this switch

default
 {
     state_entry()
     {

     }

     touch_start(integer num_touchers)
     {
         gOpacityLevel += 1;
         if (gOpacityLevel > 3)
         {
             gOpacityLevel = 0;
         }
         string opacityCmd = "";
         opacityCmd = opacityCmd + (string)gOpacityLevel;
         llSay(gChannel, opacityCmd);
     }
 }
```

## How to work with it

When you've put all the window opacity scripts in and done the switch, just click the switch to cycle through transparent and opaque.