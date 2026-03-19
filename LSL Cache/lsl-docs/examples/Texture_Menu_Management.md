---
name: "Texture Menu Management"
category: "example"
type: "example"
language: "LSL"
description: "(based on our previus script and released here for you as we did a custom edit for second-life community and i thought you may like to use this script as well.)"
wiki_url: "https://wiki.secondlife.com/wiki/Texture_Menu_Management"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

- 1 Texture Menu Management

  - 1.1 Introduction
  - 1.2 Usage
  - 1.3 Main Script

  - 1.3.1 Support

Texture Menu Management

(based on our previus script and released here for you as we did a custom edit for second-life community and i thought you may like to use this script as well.)

### Introduction

Allows you to have dialog based navigation of textures.
and browse the image you like to display on your prim from a dialog with simple and ease of navigation

## Usage

Create a script and copy and paste the script below into your prim.
and copy textures or photos from your inventory into the content tab of your prim
click your prim containing the script and textures and select a texture or photo from the menu dialog

## Main Script

```lsl
list MENU1 = [];
list MENU2 = [];
integer listener;
integer MENU_CHANNEL = 1000;

// opens menu channel and displays dialog
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
        // reset scripts on rez
        llResetScript();
    }

    touch_start(integer total_number)
    {
        integer i = 0;
        MENU1 = [];
        MENU2 = [];
        // count the textures in the prim to see if we need pages
        integer c = llGetInventoryNumber(INVENTORY_TEXTURE);
        if (c <= 12)
        {
            for (; i < c; ++i)
                MENU1 += llGetInventoryName(INVENTORY_TEXTURE, i);
        }
        else
        {
            for (; i < 11; ++i)
                MENU1 += llGetInventoryName(INVENTORY_TEXTURE, i);
            if(c > 22)
                c = 22;
            for (; i < c; ++i)
                MENU2 += llGetInventoryName(INVENTORY_TEXTURE, i);
            MENU1 += ">>";
            MENU2 += "<<";
        }
        // display the dialog
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
                // display the texture from menu selection
                llSetTexture(message, ALL_SIDES);

            }
        }
    }
}
```

#### Support

For technical support, requests, etc., use the Search under the Groups Tab and search for Dazzle Software

If you have any problems getting this script to work either contact me in-world [Revolution Perenti](https://wiki.secondlife.com/wiki/User:Revolution_Perenti)
Or visit our free scripts at our LSL scripts [www.dazzlesoftware.org](http://www.dazzlesoftware.org) Secondlife Open Source Section on Tutorials.
Latest version always available on [Marketplace](https://marketplace.secondlife.com/p/Dazzle-Software-Dialog-Menu-Based-Texture-API/374435) or [Dazzle Software via Wyrd](http://maps.secondlife.com/secondlife/Wyrd/230/83/97)