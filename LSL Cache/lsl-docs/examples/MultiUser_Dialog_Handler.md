---
name: "MultiUser Dialog Handler"
category: "example"
type: "example"
language: "LSL"
description: "I found that i was constantly rewriting a pile of dialog handling functions in my scrips so i decided to write a single dialog handler script. It needed to have the following features;"
wiki_url: "https://wiki.secondlife.com/wiki/MultiUser_Dialog_Handler"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

- 1 Introduction
- 2 Using The Script

  - 2.1 Calling a Simple Menu
  - 2.2 Calling a Simple Menu with Auto-Navigation Buttons
  - 2.3 Calling a Complex Menu
  - 2.4 Parsing the returning Menu information
- 3 The Script
- 4 See also

## Introduction

I found that i was constantly rewriting a pile of dialog handling functions in my scrips so i decided to write a single dialog handler script. It needed to have the following features;

- Support multiple simultaneous menus from different users, scripts and prims.
- Support fixed top buttons that will persist on lists.
- Support fixed bottom buttons with include Back and Exit buttons.
- Handle item lists > 12 and automatically insert << and  >> buttons to scroll through the lists.
- Handle timeouts and communicate timeout back to calling script.
- Handles truncation of the buttons and text to stop errors in llDialog

## Using The Script

### Calling a Simple Menu

In the script that is calling the menu I use a function something like this.

```lsl
// Link Commands
integer     LINK_MENU_DISPLAY = 300;
integer     LINK_MENU_RETURN = 320;
integer     LINK_MENU_TIMEOUT = 330;

DisplayMenu(key id)
{   // Menu Functions
    string  menuDescripter = "mymenu";  //An identifier to show what menu called the script. I often include the script name plus menu name.
    string  menuNavigate = "FALSE";      //Navigation buttons not displayed
    string  menuText = "This is the menu text that will be displayed.";  // The text will be trimmed to 510 characters
    string  menuButtons =  "TopLeft~Top~TopRight~Left~Center~Right~BottomLeft~Bottom~BottomRight";   // The buttons, each button separated by a '~'.

    llMessageLinked(LINK_THIS, LINK_MENU_DISPLAY, menuDescripter+"|"+menuNavigate+"|"+menuText+"|"+ menuButtons, id);
}
```

This will display a menu that looks something like

```lsl
This is the menu text that will be displayed.
```

TopLeft
Top
TopRight

Left
Center
Right

BottomLeft
Bottom
BottomRight

### Calling a Simple Menu with Auto-Navigation Buttons

In this case we now add navigation buttons to the bottom of the script.  Back and Exit buttons are added to the bottom and if necessary >> and << buttons.  In the script that is calling the menu I use a function something like this.

```lsl
// Link Commands
integer     LINK_MENU_DISPLAY = 300;
integer     LINK_MENU_RETURN = 320;
integer     LINK_MENU_TIMEOUT = 330;

DisplayMenu(key id)
{   // Menu Functions
    string  menuDescripter = "mymenu";  //An identifier to show what menu called the script. I often include the script name plus menu name.
    string  menuNavigate = "TRUE";      //The display of the bottom navigation buttons is set to TRUE
    string  menuText = "This is the menu text that will be displayed.";  // The text will be trimmed to 510 characters
    string  menuButtons =  "Owner~Group~All";                            // The buttons, each button separated by a '~'.  Buttons will be trimmed to 24 characters

    llMessageLinked(LINK_THIS, LINK_MENU_DISPLAY, menuDescripter+"|"+menuNavigate+"|"+menuText+"|"+ menuButtons, id);
}
```



This will display a menu that looks something like this.

```lsl
This is the menu text that will be displayed.
```

Owner
Group
All

Back
Exit

### Calling a Complex Menu

In the following case we will have 10 buttons that are going to be displayed.  Because we will also display the bottom 3 buttons this will be spanned across 2 menus.  We will also include 2 fixed buttons that always display at the top of the menu, PLUS each button has a unique descriptor that is displayed.  Here is the menu call.

```lsl
// Link Commands
integer     LINK_MENU_DISPLAY = 300;
integer     LINK_MENU_RETURN = 320;
integer     LINK_MENU_TIMEOUT = 330;

DisplayMenu(key id)
{   // Menu Functions
    string  menuDescripter = "mymenu"
    string  menuNavigate = "TRUE";
    string  menuText = "Main text displayed.~text1~text2~text3~text4~text5~text6~text7~text8~text9~text10";
    string  menuButtons =  "B1~B2~B3~B4~B5~B6~B7~B8~B9~B10";
    string  menuFixedButtons = "FIXED1~FIXED2"

    llMessageLinked(LINK_THIS, LINK_MENU_DISPLAY, menuDescripter+"|"+menuNavigate+"|"+menuText+"|"+ menuButtons+"|"+menuFixedButtons, id);
}
```

This will display the following 2 menus

Menu1

```lsl
Main text displayed.
item1
item2
item3
item4
item5
item6
item7
```

FIXED1
FIXED2
B1

B2
B3
B4

B5
B6
B7

Back
>>

Menu2 (on clicking the >> button)

```lsl
Main text displayed.
item8
item9
item10
```

FIXED1
FIXED2
B8

B9
B10

<<
Back
Exit

### Parsing the returning Menu information

Note that if the user clicks on the << or >> buttons the calling script WILL NOT see any response.  The correct menu is displayed.  The calling script only receives a response when one of the buttons or Back/Exit are clicked.  Clicking on a space button will cause the menu to redisplay.

The script that expects the response back from the menu has the following

```lsl
// Link Commands
integer     LINK_MENU_DISPLAY = 300;
integer     LINK_MENU_RETURN = 320;
integer     LINK_MENU_TIMEOUT = 330;

default
{
    link_message(integer intSenderNum, integer num, string message, key id)
    {
        if (num == LINK_MENU_RETURN)
        {
            list    returnMenu = llParseString2List(message, ["|"], []);
            string  menuDescriptor = llList2String(returnMenu,0);        // The idenfifying descriptor.  I sometimes use the name of the script plus menu and parent menu name

            if (menuDescriptor == "mymenu")
            {    // Is this a response to "mymenu" from the dialog script?
                 string  item = llList2String(returnMenu,1);             // The actual button pushed

                 // id == the key of the menu user.
                 // The button pressed in the menu is 'item', so now do something with it
            }
         }
         else if (num == LINK_MENU_TIMEOUT)
         {
             if (message == "mymenu")
             {
                // We received a timeout (don't worry the listens are all dealt with) so you might want to IM the menu user.
             }
         }
    }
}
```

## The Script

```lsl
// ********************************************************************
//
// Menu Display Script
//
// Menu command format
// string = menuidentifier | display navigate? TRUE/FALSE | menuMaintitle~subtitle1~subtitle2~subtitle3 | button1~button2~button3 {| fixedbutton1~fixedbutton2~fixedbutton3  optional}
// key = menuuser key
//
// Return is in the format
// "menuidentifier | item"
//
// menusDescription [menuchannel, key, menu & parent, return link, nav?,  titles, buttons, fixed buttons]
// menusActive      [menuchannel, menuhandle, time, page]
//
// by SimonT Quinnell
//
// CHANGES
// 2010/10/14 - Timeout message now gets sent to the prim that called the menu, not LINK_THIS.  Also includes menuidentifier
// 2010/11/29 - Fixed Bug in RemoveUser function.  Thanks for Virtouse Lilienthal for pointing it out.
// 2010/11/29 - Tidied up a little and removed functions NewMenu and RemoveUser that are only called once
// 2014/04/28 - Clarified licence
//
// NOTE: This script is licenced using the Creative Commons Attribution-Share Alike 3.0 license
//
// ********************************************************************

// ********************************************************************
// CONSTANTS
// ********************************************************************

// Link Commands
integer     LINK_MENU_DISPLAY = 300;
integer     LINK_MENU_CLOSE = 310;
integer     LINK_MENU_RETURN = 320;
integer     LINK_MENU_TIMEOUT = 330;

// Main Menu Details
string      BACK = "<<";
string      FOWARD = ">>";
list        MENU_NAVIGATE_BUTTONS = [ " ", "Back", "Exit"];
float       MENU_TIMEOUT_CHECK = 10.0;
integer     MENU_TIMEOUT = 120;
integer     MAX_TEXT = 510;

integer     STRIDE_DESCRIPTION = 8;
integer     STRIDE_ACTIVE = 4;
integer     DEBUG = FALSE;

// ********************************************************************
// Variables
// ********************************************************************

list    menusDescription;
list    menusActive;

// ********************************************************************
// Functions - General
// ********************************************************************

debug(string debug)
{
    if (DEBUG) llSay(DEBUG_CHANNEL,"DEBUG:"+llGetScriptName()+":"+debug+" : Free("+(string)llGetFreeMemory()+")");
}


integer string2Bool (string test)
{
    if (test == "TRUE") return TRUE;
    else return FALSE;
}

// ********************************************************************
// Functions - Menu Helpers
// ********************************************************************

integer NewChannel()
{    // generates unique channel number
    integer channel;

    do channel = -(llRound(llFrand(999999)) + 99999);
    while (~llListFindList(menusDescription, [channel]));

    return channel;
}

string  CheckTitleLength(string title)
{
    if (llStringLength(title) > MAX_TEXT) title = llGetSubString(title, 0, MAX_TEXT-1);

    return title;
}

list FillMenu(list buttons)
{   //adds empty buttons until the list length is multiple of 3, to max of 12
    integer i;
    list    listButtons;

    for(i=0;i 24) name = llGetSubString(name, 0, 23);
        listButtons = listButtons + [name];
    }

    while (llGetListLength(listButtons) != 3 && llGetListLength(listButtons) != 6 && llGetListLength(listButtons) != 9 && llGetListLength(listButtons) < 12)
    {
        listButtons = listButtons + [" "];
    }

    buttons = llList2List(listButtons, 9, 11);
    buttons = buttons + llList2List(listButtons, 6, 8);
    buttons = buttons + llList2List(listButtons, 3, 5);
    buttons = buttons + llList2List(listButtons, 0, 2);

    return buttons;
}

RemoveMenu(integer channel, integer echo)
{
    integer index = llListFindList(menusDescription, [channel]);

    if (index != -1)
    {
        key     menuId = llList2Key(menusDescription, index+1);
        string  menuDetails = llList2String(menusDescription, index+2);
        integer menuLink = llList2Integer(menusDescription, index+3);
        menusDescription = llDeleteSubList(menusDescription, index, index + STRIDE_DESCRIPTION - 1);
        RemoveListen(channel);

        if (echo) llMessageLinked(menuLink, LINK_MENU_TIMEOUT, menuDetails, menuId);
    }
}

RemoveListen(integer channel)
{
    integer index = llListFindList(menusActive, [channel]);
    if (index != -1)
    {
        llListenRemove(llList2Integer(menusActive, index + 1));
        menusActive = llDeleteSubList(menusActive, index, index + STRIDE_ACTIVE - 1);
    }
}

// ********************************************************************
// Functions - Menu Main
// ********************************************************************

DisplayMenu(key id, integer channel, integer page)
{
    string  menuTitle;
    list    menuSubTitles;
    list    menuButtonsAll;
    list    menuButtons;
    list    menuNavigateButtons;
    list    menuFixedButtons;

    integer max = 12;

    // Populate values
    integer index = llListFindList(menusDescription, [channel]);
    menuButtonsAll = llParseString2List(llList2String(menusDescription, index+6), ["~"], []);
    if (llList2String(menusDescription, index+7) != "") menuFixedButtons = llParseString2List(llList2String(menusDescription, index+7), ["~"], []);

    // Set up the menu buttons
    if (llList2Integer(menusDescription, index+4)) menuNavigateButtons= MENU_NAVIGATE_BUTTONS;
    else if (llGetListLength(menuButtonsAll) > (max-llGetListLength(menuFixedButtons))) menuNavigateButtons = [" ", " ", " "];

    // FIXME: add sanity check for menu page

    max = max - llGetListLength(menuFixedButtons) - llGetListLength(menuNavigateButtons);
    integer     start = page*max;
    integer     stop = (page+1)*max - 1;
    menuButtons = FillMenu(menuFixedButtons + llList2List(menuButtonsAll, start, stop));

    // Generate the title
    list tempTitle = llParseString2List(llList2String(menusDescription, index+5), ["~"], []);
    menuTitle = llList2String(tempTitle,0);
    if (llGetListLength(tempTitle) > 1) menuSubTitles = llList2List(tempTitle, 1, -1);
    if (llGetListLength(menuSubTitles) > 0)
    {
        integer i;
        for(i=start;i<(stop+1);++i)
        {
            if (llList2String(menuSubTitles, i) != "") menuTitle += "\n"+llList2String(menuSubTitles, i);
        }
    }
    menuTitle = CheckTitleLength(menuTitle);

    // Add navigate buttons if necessary
    if (page > 0) menuNavigateButtons = llListReplaceList(menuNavigateButtons, [BACK], 0, 0);
    if (llGetListLength(menuButtonsAll) > (page+1)*max) menuNavigateButtons = llListReplaceList(menuNavigateButtons, [FOWARD], 2, 2);

    // Set up listen and add the row details
    integer menuHandle = llListen(channel, "", id, "");
    menusActive = [channel, menuHandle, llGetUnixTime(), page] + menusActive;

    llSetTimerEvent(MENU_TIMEOUT_CHECK);

    // Display menu
    llDialog(id, menuTitle, menuNavigateButtons + menuButtons, channel);
}


// ********************************************************************
// Event Handlers
// ********************************************************************

default
{
    listen(integer channel, string name, key id, string message)
    {
        if (message == BACK)
        {
            integer index = llListFindList(menusActive, [channel]);
            integer page = llList2Integer(menusActive, index+3)-1;
            RemoveListen(channel);
            DisplayMenu(id, channel, page);
        }
        else if (message == FOWARD)
        {
            integer index = llListFindList(menusActive, [channel]);
            integer page = llList2Integer(menusActive, index+3)+1;
            RemoveListen(channel);
            DisplayMenu(id, channel, page);
        }
        else if (message == " ")
        {
            integer index = llListFindList(menusActive, [channel]);
            integer page = llList2Integer(menusActive, index+3);
            RemoveListen(channel);
            DisplayMenu(id, channel, page);
        }
        else
        {
            integer index = llListFindList(menusDescription, [channel]);
            llMessageLinked(llList2Integer(menusDescription, index+3), LINK_MENU_RETURN, llList2String(menusDescription, index+2)+"|"+message, id);
            RemoveMenu(channel, FALSE);
        }
    }

    link_message(integer senderNum, integer num, string message, key id)
    {
        if (num == LINK_MENU_DISPLAY)
        {   // Setup New Menu
            list    temp = llParseString2List(message, ["|"], []);
            integer channel = NewChannel();

            if (llGetListLength(temp) > 2)
            {
                menusDescription = [channel, id, llList2String(temp, 0), senderNum,  string2Bool(llList2String(temp, 1)), llList2String(temp, 2), llList2String(temp, 3), llList2String(temp, 4)] + menusDescription;

                DisplayMenu(id, channel, 0);
            }
            else llSay (DEBUG_CHANNEL, "ERROR in "+llGetScriptName()+": Dialog Script. Incorrect menu format");
        }
        else if (num == LINK_MENU_CLOSE)
        {    // Will remove all menus that have the user id.
             integer index_id = llListFindList(menusDescription, [id]);

             while (~index_id)
             {
                 integer channel = llList2Integer(menusDescription, index_id-1);
                 RemoveMenu(channel, FALSE);

                 // Check for another menu by same user
                 index_id = llListFindList(menusDescription, [id]);
             }
        }
    }

    timer()
    {   // Check through timers and close if necessary
        integer i;
        list toRemove;
        integer currentTime = llGetUnixTime();
        integer length = llGetListLength(menusActive);

        for(i=0;i MENU_TIMEOUT) toRemove = [llList2Integer(menusActive, i)] + toRemove;
        }

        length = llGetListLength(toRemove);
        if (length > 0)
        {
            for(i=0;i