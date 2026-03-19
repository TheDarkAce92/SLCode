---
name: "Skillingo AntiHack Script"
category: "example"
type: "example"
language: "LSL"
description: "This is a simple script to insert into a Skillingo Machine ( or others with a few simple tweaks) to double check whats being paid. If its not what you set in your config card it disables the machine and informs you the owner that someone attempted to spoof a payment."
wiki_url: "https://wiki.secondlife.com/wiki/Skillingo_AntiHack_Script"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

This is a simple script to insert into a Skillingo Machine ( or others with a few simple tweaks) to double check whats being paid. If its not what you set in your config card it disables the machine and informs you the owner that someone attempted to spoof a payment.

Theres only a few things to change for other machines of skill to be able to protect them if they already arent :) i have commented those blocks below.

Once you have gone to the machine you have to first reset scripts in selection then set all scripts to running in selection ( i would reset once more for good measure after though )
or you can remove the protection script and set running on selection then reset machine :)



Please note that although this script is primairly designed for protecting the popular skillingo machine from individuals that use bad viewers i cannot assume any libality for any damages that may happen this script is like every script use at your own risk and i do not garuentee perfect protection i can only try to protect it as much as LSL will let me.

With that said those that chose to use this one or any other protection script i hope you enjoy being able to safley place skillingos back out for use as they are rather fun :)

```lsl
//////////////////////////////////////////////////////////////////////////////
//                      Skillingo Anti Hack Script                          //
//                                                                          //
//    Copyright (C) 2009 Tmzasz Luminos                                     //
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

list deadpay = [PAY_HIDE,PAY_HIDE,PAY_HIDE,PAY_HIDE]; // The Disabler List for llSetPayPrice()
integer price;
key kQuery;
integer iLine;
list settings;

string wwGetSLUrl() // Function pulled somewhere off the wiki if it was yours please edit this and give credit ( i couldent find it again :( )
{
    string globe = "http://slurl.com/secondlife";
    string region = llGetRegionName();
    vector pos = llGetPos();
    string posx = (string)llRound(pos.x);
    string posy = (string)llRound(pos.y);
    string posz = (string)llRound(pos.z);
    return (globe + "/" + region +"/" + posx + "/" + posy + "/" + posz);
}

default
{
    state_entry()
    {
        iLine = 0;
        llSetTimerEvent(0.0); // set timer to not run for pay disable
        kQuery = llGetNotecardLine("config", iLine); // change "config" to the name of your machines config
    }
    on_rez(integer start_param)
    {
        llResetScript();
    }
    money(key id, integer amount)
    {
        if(amount != price) // CHeck to make sure that the price is indeed what the config says it should be
        {
            llSetScriptState("configuration",FALSE); // Disables the config Card Reader // change or remove for your machine
            llSetScriptState("game.3",FALSE); // Disables the Core machine script // change to your machines Core script
            llInstantMessage(llGetOwner(),(string)llKey2Name(id) + " Has atempted to hack the machine located at " + wwGetSLUrl());
            llSetTimerEvent(0.1); // start the pay hide timer
            llSay(0,"HACK ATTEMPT SHUTTING DOWN MACHINE!");
            llSetText("Machine Down For Repair",<1,0,0>,1); // remove hovertext
        }
    }
    timer()
    {
        llSetPayPrice(PAY_HIDE,deadpay); // DISABLE pay options so no further atempts can be made
    }
    dataserver(key query_id, string data)
    {
        if (query_id == kQuery)
        {
            list a = llParseString2List(data, ["="], [""]); // Change only the "=" part for configs that dont use a = as a seperator
            data = llList2String(a, 1);
            if (iLine==16) // Change to reflect TOTAL number of lines in your config file
            {
                price = llList2Integer(settings, 0);
                llOwnerSay("Machine Protection ACTIVATED");
            }
            else
            {
                settings+=data;
                iLine++;
                kQuery = llGetNotecardLine("config", iLine); // change "config" to the name of your machines config
            }
        }
    }
}
```