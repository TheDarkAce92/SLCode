---
name: "Open Zyngo Skin Installer"
category: "example"
type: "example"
language: "LSL"
description: "I am uploading this script here for everyone to use its a simple skin script to set skins on the popular zyngo machines all you have to do is change the keys and other varriables and drop it into your machine it does the rest."
wiki_url: "https://wiki.secondlife.com/wiki/Open_Zyngo_Skin_Installer"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

I am uploading this script here for everyone to use its a simple skin script to set skins on the popular zyngo machines all you have to do is change the keys and other varriables and drop it into your machine it does the rest.

```lsl
//////////////////////////////////////////////////////////////////////////////
//                      Good Skin Instaler Script                           //
//                                                                          //
//      I got the basics of this script from Cold Spitteler over at Jaded   //
//      so its not entirely mine but i am giving credit where it is due     //
//                                                                          //
//    Copyright (C) 2009 Tmzasz Luminos with help from Cold Spitteler       //
//    This program is free software: you can redistribute it and/or modify  //
//    it under the terms of the GNU General Public License version 3, as    //
//    published by the Free Software Foundation.                            //
//                                                                          //
//    This program is distributed in the hope that it will be useful,       //
//    but WITHOUT ANY WARRANTY; without even the implied warranty of        //
//    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         //
//    GNU General Public License for more details.                          //
//                                                                          //
//   You should have received a copy of the GNU General Public License      //
//    along with this program.  If not, see   //
//////////////////////////////////////////////////////////////////////////////

key texture = "00000000-0000-0000-0000-000000000000"; // replace 0 with your skins UUID
vector topColor = <1.0,1.0,1.0>; //Top of the machines color
vector potcolor = <1,1,1>; //Color of the Pot numbers
vector score2beatcolor = <1,1,1>; //Color of the Score2Beat numbers
vector scorecolor = <1,1,1>; //Color of the Score and Round numbers
vector pricecolor = <1,1,1>; //Color of the Price and %to Pot numbers

LoadTexture(key texture, vector topColor) //  set the skin itself
{
    llSetTexture(texture,1);
    llSetTexture(texture,2);
    llSetTexture(texture,3);
    llSetTexture(texture,4);
    llSetColor(topColor,0);
}

default
{
    state_entry()
    {
        LoadTexture(texture,topColor); // Calls the function to set skin

        llSetLinkColor(11, potcolor, ALL_SIDES); // sets pot color
        llSetLinkColor(10, score2beatcolor, ALL_SIDES); // sets score2beat color
        llSetLinkColor(9, scorecolor, ALL_SIDES); // sets score color
        llSetLinkColor(7, pricecolor, ALL_SIDES); // sets price color
        llSleep(2.5);
        llOwnerSay("Skin Installed removing this Script");    // tells you when its all done
        llRemoveInventory(llGetScriptName());    // gets the script name of this script! and removes THIS SCRIPT

    }
}
```