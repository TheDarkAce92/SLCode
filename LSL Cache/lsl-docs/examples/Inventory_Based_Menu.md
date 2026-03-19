---
name: "Inventory Based Menu"
category: "example"
type: "example"
language: "LSL"
description: "Ok you want to create a dialog based menu system, you want to support more than 12 buttons so im going to give you quick overview of basic menu using llRezAtRoot, llGetInventoryName & llGetInventoryNumber"
wiki_url: "https://wiki.secondlife.com/wiki/Inventory_Based_Menu"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

### Introduction

Ok you want to create a dialog based menu system, you want to support more than 12 buttons
so im going to give you quick overview of basic menu using llRezAtRoot, llGetInventoryName & llGetInventoryNumber

USAGE:just drop objects into the prim and rez them from the dialog by touching the prim.

### LSL Script

```lsl
list MENU1 = [];
list MENU2 = [];
integer listener;
integer MENU_CHANNEL = 1000;

Dialog(key id, list menu)
{
    llListenRemove(listener);
    listener = llListen(MENU_CHANNEL, "", NULL_KEY, "");
    llDialog(id, "Select one object below: ", menu, MENU_CHANNEL);
}

default
{
    on_rez(integer num)
    {
        llResetScript();
    }

    touch_start(integer total_number)
    {
        integer i = 0;
        MENU1 = [];
        MENU2 = [];
        integer c = llGetInventoryNumber(INVENTORY_OBJECT);
        if (c <= 12)
        {
            for (; i < c; ++i)
                MENU1 += llGetInventoryName(INVENTORY_OBJECT, i);
        }
        else
        {
            for (; i < 11; ++i)
                MENU1 += llGetInventoryName(INVENTORY_OBJECT, i);
            if(c > 22)
                c = 22;
            for (; i < c; ++i)
                MENU2 += llGetInventoryName(INVENTORY_OBJECT, i);
            MENU1 += ">>";
            MENU2 += "<<";
        }
        Dialog(llDetectedKey(0), MENU1);
    }

    listen(integer channel, string name, key id, string message)
    {
        if (channel == MENU_CHANNEL)
        {
            llListenRemove(listener);
            if (message == ">>")
            {
                Dialog(id, MENU2);
            }
            else if (message == "<<")
            {
                Dialog(id, MENU1);
            }
            else
            {
                // todo add offsets so box sites perfect on rezzer
                llRezAtRoot(message, llGetPos(), ZERO_VECTOR, llGetRot(), 0);
            }
        }
    }
}
```

### Support

For technical support, requests, etc., use the Search under the Groups Tab and search for Dazzle Software

If you have any problems getting this script to work either contact me in-world [Revolution Perenti](https://wiki.secondlife.com/wiki/User:Revolution_Perenti)
Or visit our free scripts at our LSL scripts [www.dazzlesoftware.org](http://www.dazzlesoftware.org) Secondlife Open Source Section on Tutorials.
Latest version always available on [[1]](https://marketplace.secondlife.com/p/Dazzle-Software-Inventory-Menu-Rezzer-API/374439) or [Dazzle Software via Wyrd](http://maps.secondlife.com/secondlife/Wyrd/230/83/97)