---
name: "Dialog Control"
category: "example"
type: "example"
language: "LSL"
description: "If anyone uses this module, please IM Nargus Asturias, I'd love to hear what you think."
wiki_url: "https://wiki.secondlife.com/wiki/Dialog_Control"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

- 1 Functions List

  - 1.1 Basic Dialog Functionalities
  - 1.2 Menus Control
- 2 Sample Scripts
- 3 Scripts

  - 3.1 Basic Usage Examples

  - 3.1.1 Dialog Usage
  - 3.1.2 Menus Usage

## Functions List

### Basic Dialog Functionalities

1. Standard dialog with buttons. If there are more than 12 buttons, BACK/NEXT button will be added *automatically*! In that case, the last button on the list will be used as Close/Cancel button.

  - **dialog**(key id, string message, list buttons, list returns);
1. Standard dialog with an input box

  - **dialogTextbox**(key id, string message);
1. To recall last dialog (only work if a dialog has been called before):

  - **dialogReshow**();
1. To cancel current dialog; Currently displayed dialog will give no response when clicked.

  - **dialogCancel**();

### Menus Control

1. Initialize menus control using:

  - llMessageLinked(LINK_THIS, lnkMenuClear, "", NULL_KEY);
1. Using "packDialogMessage" function to generate new menu, and add it to menus list:

  - llMessageLinked(LINK_THIS, lnkMenuAdd, **packDialogMessage**(....), "MenuName");
  - While "MenuName" is the name of this menu, ie: MainMenu
1. To make a dialog button show a sub-menu, use following as return value of the button:

  - MENU_
  - Replace "" with the actual name of the added menu (without parenthesis).
1. Repeat (2) and (3) for all menus you want
1. To show a menu, use:

  - llMessageLinked(LINK_THIS, lnkMenuShow, "MenuName", llGetOwner());
  - Where "MenuName" is the name of menu to show. To show last-used menu, leave this field empty.
1. Dialog will return value the same way as usual call to Nargus Dialog Module script.

## Sample Scripts

1. **OnTouchSelectTexture** (Tiyuk Quellmalz)



If anyone uses this module, please IM *Nargus Asturias*, I'd love to hear what you think.

## Scripts

- **Dialog Control v1.8** (with built-in Dialog Menus Control)
- **Dialog Control (legacy)** (*Legacy version*; do not have built-in menus control)
- **Dialog Menus Control** (*Legacy version*; Need Dialog Control (legacy) for the script to work)

### Basic Usage Examples

#### Dialog Usage

```lsl
// READ ME:
// To see this sample in action;
// Put "Nargus Dialog Control" along with this script in a prim and touch.

// ********** DIALOG FUNCTIONS **********
// Dialog constants
integer lnkDialog = 14001;
integer lnkDialogTextbox = 14007;
integer lnkDialogResponse = 14002;
integer lnkDialogTimeOut = 14003;

integer lnkDialogReshow = 14011;
integer lnkDialogCancel = 14012;

string seperator = "||";
integer dialogTimeOut = 0;

string packDialogMessage(string message, list buttons, list returns){
    string packed_message = message + seperator + (string)dialogTimeOut;

    integer i;
    integer count = llGetListLength(buttons);
    for(i=0; i 24) button = llGetSubString(button, 0, 23);
        packed_message += seperator + button + seperator + llList2String(returns, i);
    }

    return packed_message;
}

dialogReshow(){llMessageLinked(LINK_THIS, lnkDialogReshow, "", NULL_KEY);}
dialogCancel(){
    llMessageLinked(LINK_THIS, lnkDialogCancel, "", NULL_KEY);
    llSleep(1);
}

dialog(key id, string message, list buttons, list returns){
    llMessageLinked(LINK_THIS, lnkDialog, packDialogMessage(message, buttons, returns), id);
}

dialogTextbox(key id, string message){
    llMessageLinked(LINK_THIS, lnkDialogTextbox, message + seperator + (string)dialogTimeOut, id);
}
// ********** END DIALOG FUNCTIONS **********

default{
    state_entry(){
        llSetText("Touch me to show dialog", <1,1,1>, 1);
    }

    link_message(integer sender_num, integer num, string str, key id){
        if(num == lnkDialogTimeOut){
            llOwnerSay("Menu time-out. Please try again.");
            state default;
        }else if(num == lnkDialogResponse){
            llWhisper(0, str);
        }
    }

    touch_start(integer num_detected){
        dialog(llDetectedKey(0),

            // Dialog message here
            "Messages go here",

            // List of dialog buttons
            [ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, "Close" ],

            // List of return value from the buttons, in same order
            // Note that this value do not need to be the same as button texts
            [ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, "X" ]
        );
    }
}
```

#### Menus Usage

```lsl
// READ ME:
// To see this sample in action;
// Put "Nargus Dialog Control v1.80" along with this script
// in a prim and touch.

// Dialog constants
integer lnkDialog = 14001;
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
            llOwnerSay("Menu time-out. Please try again.");
        }else if(num == lnkDialogResponse){
            llWhisper(0, str);
        }
    }

    touch_start(integer num_detected){
        llMessageLinked(LINK_THIS, lnkMenuShow, "", llDetectedOwner(0));
    }
}
```