---
name: "Dialog Menus Control"
category: "example"
type: "example"
language: "LSL"
description: "This is example of usage and function library needed in each scripts to use this dialog menus module."
wiki_url: "https://wiki.secondlife.com/wiki/Dialog_Menus_Control"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

**Important:** This script is considered obsoleted. Latest version of Dialog Control has this functionality built-in! An obsoleted version of Nargus Dialog Control script is required to work with this script. This is example of usage and function library needed in each scripts to use this dialog menus module. **IMPORTANT NOTE:** This menus control REQUIRED Nargus Dialog Control script. You MUST have both Nargus Dialog Control and Nargus Dialog Menus in the same prim for it to work. ## Menus Usage 1. Initialize menus control using: - llMessageLinked(LINK_THIS, lnkMenuClear, "", NULL_KEY); 1. Using "packDialogMessage" function to generate new menu, and add it to menus list: - llMessageLinked(LINK_THIS, lnkMenuAdd, packDialogMessage(....), "MenuName"); - While "MenuName" is the same of this menu, ie: MainMenu 1. To make a dialog button show a sub-menu, use following as return value of the button: - MENU_ - Replace "" with the actual name of the added menu (without parenthesis). 1. Repeat (2) and (3) for all menus you want 1. To show a menu, use: - llMessageLinked(LINK_THIS, lnkMenuShow, "MenuName", llGetOwner()); - Where "MenuName" is the name of menu to show. To show last-used menu, leave this field empty. 1. Dialog will return value the same way as usual call to Nargus Dialog Module script. ## Sample Scripts - **OnTouchSelectTexture** (Tiyuk Quellmalz) If anyone uses this module, please IM Nargus Asturias, I'd love to hear what you think.

## Scripts & Example

```lsl
// READ ME:
// To see this sample in action;
// Put "Nargus Dialog Control" and "Nargus Dialog Menus" along with this script
// in a prim and touch.

// Dialog constants
integer lnkDialog = 14001;
integer lnkDialogNotify = 14004;
integer lnkDialogResponse = 14002;
integer lnkDialogTimeOut = 14003;

integer lnkDialogReshow = 14011;
integer lnkDialogCancel = 14012;

integer lnkMenuClear = 15001;
integer lnkMenuAdd = 15002;
integer lnkMenuShow = 15003;

string seperator = "||";
integer dialogTimeOut = 0;

// ********** DIALOG FUNCTIONS **********
string packDialogMessage(string message, list buttons, list returns){
    string packed_message = message + seperator + (string)dialogTimeOut;

    integer i;
    integer count = llGetListLength(buttons);
    for(i=0; i, 1);
    }

    link_message(integer sender_num, integer num, string str, key id){
        if(num == lnkDialogTimeOut){
            dialogNotify(llGetOwner(), "Menu time-out. Please try again.");
            state default;
        }else if(num == lnkDialogResponse){
            llWhisper(0, str);
        }
    }

    touch_start(integer num_detected){
        llMessageLinked(LINK_THIS, lnkMenuShow, "", llDetectedOwner(0));
    }
}
```

Nargus Dialog Menus v1.01 (by Nargus Asturias)

```lsl
// ********** DIALOG MENUS MODULE ********** //
// By Nargus Asturias
// Version 1.01
//
// Multi-layer menus management module for Nargus Dialog Control.
// Use same packing method as Nargus Dialog Control
//
// HOW TO USE:
// 1) Initialize menu by sending "lnkMenuClear" signal:
//          llMessageLinked(LINK_THIS, lnkMenuClear, "", NULL_KEY);
//
// 2) Add menu dialog using provided function (or manually, please referr to Nargus Dialog Control
//    manual). Make sure signal is sent with "lnkMenuAdd" and key field is menu's name;
//          llMessageLinked(LINK_THIS, lnkMenuAdd, ......, "MainMenu");
//
//    To make a button show submenu, use following as return value of the button:
//          MENU_
//    Replace "" with the actual name of the added menu (without parenthesis).
//
// 3) Repeat (2) for as much menus as needed
//
// 4) To show a menu, use:
//          llMessageLinked(LINK_THIS, lnkMenuShow, name, llGetOwner());
//    When "name" is name of the menu to show. To show last-used menu, leave this field empty.
//
// 5) Dialog will return value the same way as usual call to Nargus Dialog Module script.
// ******************************************* //

// Dialog constants
integer lnkDialog = 14001;
integer lnkDialogNotify = 14004;
integer lnkDialogResponse = 14002;
integer lnkDialogTimeOut = 14003;

integer lnkDialogReshow = 14011;
integer lnkDialogCancel = 14012;

string seperator = "||";
integer dialogTimeOut = 0;

// ********** DIALOG FUNCTIONS **********
dialogReshow(){llMessageLinked(LINK_THIS, lnkDialogReshow, "", NULL_KEY);}
dialogCancel(){
    llSleep(1);
    llMessageLinked(LINK_THIS, lnkDialogCancel, "", NULL_KEY);
}
// ********** END DIALOG FUNCTIONS **********

// Constants
integer lnkMenuClear = 15001;
integer lnkMenuAdd = 15002;
integer lnkMenuShow = 15003;

// Menus variables
list menuNames;             // List of names of all menus
list menus;                 // List of packed menus command, in order of menuNames

// Variables
integer lastMenuIndex;      // Latest called menu's index

// ********** Menu Functions **********
clearMenusList(){
    menuNames = [];
    menus = [];

    lastMenuIndex = 0;
}

addMenu(string name, string message, list buttons, list returns){
    // Reduced menu request time by packing request commands
    string packed_message = message + seperator + (string)dialogTimeOut;

    integer i;
    integer count = llGetListLength(buttons);
    for(i=0; i