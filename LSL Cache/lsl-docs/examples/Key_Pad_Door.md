---
name: "Key Pad Door"
category: "example"
type: "example"
language: "LSL"
description: "This keypad Door is composed of 3 scripts, one for the door, one for the keypad, and one for each keypad button. Below is the script for the button: Put this script in each button. Make 11 buttons and name them the following: \"Reset\",\"Enter\",and the numbers 1-9."
wiki_url: "https://wiki.secondlife.com/wiki/Key_Pad_Door"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

This keypad Door is composed of 3 scripts, one for the door, one for the keypad, and one for each keypad button.
Below is the script for the button:


Put this script in each button. Make 11 buttons and name them the following: "Reset","Enter",and the numbers 1-9.

```lsl
//Button Script
default
{
    touch_start(integer total_number)
    {
        llMessageLinked(LINK_ROOT,1,llGetObjectName(),NULL_KEY);
    }
}
```



Then mount the buttons on a root prim and call the root prim "Key Pad" (without quotes) and put the following script in it. On rez it will ask you what you want the code to be, say it in the form x,y,z with as many digits as desired. After 15 seconds of not anwsering, it we default to 1,2,3,4.

```lsl
integer channel = 3800; //If you change this remeber to change it in the door script as well
list temp;
list code = [1,2,3,4];
integer handle;

default
{
    on_rez(integer param)
    {
        handle = llListen(0,"",llGetOwner(),"");
        llOwnerSay("What do you wish the code to be?");
        llSetTimerEvent(15);
    }
    link_message(integer send_num, integer num, string msg, key id)
    {
        if(msg == "Reset")
        {
            temp = [];
        }
        if(msg == "Enter")
        {
            if(temp != code)
            {
                llWhisper(0,"Incorrect Code!!");
                temp = [];
            }
            if(llList2CSV(temp) == llList2CSV(code))
            {
                llWhisper(channel,"open");
                llWhisper(0,"You may enter.");
                temp = [];
            }
        }
        if(msg != "Reset" && msg != "Enter")
        {
            temp += [(integer)msg];
            if(llGetListLength(temp) > llGetListLength(code))
            {
                temp = [];
            }
        }
    }
    timer()
    {
        llOwnerSay("You have run out of time. Setting default " + llList2CSV(code));
        llListenRemove(handle);
        llSetTimerEvent(0);
    }
    listen(integer chan, string name, key id, string msg)
    {
        llListenRemove(handle);
        code = llCSV2List(msg);
        llOwnerSay("Code set to " + llList2CSV(code) + ".");
        llSetTimerEvent(0);
    }
}
```



Now the door script. The door can be called anything. Script is as follows:

```lsl
integer channel = 3800; //Must be the same as in the key pad script
float open_time = 3; //Change to how long you want it to stay open

default
{
    state_entry()
    {
        llListen(3800,"Key Pad",NULL_KEY,"open");
    }
    listen(integer chan, string name, key id, string msg)
    {
        llSetStatus(STATUS_PHANTOM,TRUE);
        llSetAlpha(0.1,ALL_SIDES);
        llSleep(open_time);
        llSetAlpha(1.0,ALL_SIDES);
        llSetStatus(STATUS_PHANTOM,FALSE);
    }
}
```



If you want the completed object with key pad and door, you can buy it at [http://www.tslemporium.com](http://www.tslemporium.com) for 30 L$. I will not give support to people who use the scripts on this page for thier own door, only paying customers.




Here is a more updated version of the Key Pad Door.. This requires only 1 prim for the entire keypad instead of the previous 12..
No changes to the door.

Script is as follows:

```lsl
integer channel = 3800; //If you change this remeber to change it in the door script as well
list temp;
string button;
list code = [1,2,3,4];
integer handle;
integer horizontal = 3;
integer vertical = 4;
list buttons = [ "1", "2", "3", "4",
"5", "6", "7", "8",
"9", "*", "0", "#" ];
key keypad = "7cec8c66-bf10-1f18-4914-1308b6c1e07c";
key blank = "5748decc-f629-461c-9a36-a35a221fe21f";

default
{
    state_entry()
    {
        handle = llListen(0,"",llGetOwner(),"");
        llOwnerSay("What do you wish the code to be?");
        llSetTimerEvent(15);
    }

    on_rez(integer param)
    {
        llSetTexture(blank, ALL_SIDES);
        llSetTexture(keypad, 2);
        llSetTexture(keypad, 4);
        llResetScript();
    }

    touch_end(integer num_detected)
    {
        integer i;
        for (i = 0; i < num_detected; i++)
        {
            integer touchedFace = llDetectedTouchFace(i);

            if (touchedFace == -1)
            {
                llWhisper(0, "Sorry, your viewer doesn't support touched faces.");
            }
            else if (touchedFace != 2 & touchedFace != 4)
            {
            }
            else
            {
                vector v = llDetectedTouchUV(0);

                if( v == TOUCH_INVALID_TEXCOORD )
                {
                    llSay(0, "I don't know what you just did.");
                    return;
                }

                float x = v.x;
                float y = 1.0-v.y;

                integer idx;
                integer rowno;
                integer colno;

                rowno = (integer)(y / (1.0/(float)vertical));
                colno = (integer)(x / (1.0/(float)horizontal));

                idx = rowno*horizontal + colno;
                button = llList2String(buttons,idx);
                if(button == "*")
                {
                    temp = [];
                }
                if(button == "#")
                {
                    if(temp != code)
                    {
                        llWhisper(0,"Incorrect Code!!");
                        temp = [];
                    }
                    if(llList2CSV(temp) == llList2CSV(code))
                    {
                        llWhisper(channel,"open");
                        llWhisper(0,"You may enter.");
                        temp = [];
                    }
                }
                if(button != "*" && button != "#")
                {
                    temp += [(integer)button];
                }
            }
        }
    }

    timer()
    {
        llOwnerSay("You have run out of time. Setting default " + llList2CSV(code));
        llListenRemove(handle);
        llSetTimerEvent(0);
    }

    listen(integer chan, string name, key id, string msg)
    {
        llListenRemove(handle);
        code = llCSV2List(msg);
        llOwnerSay("Code set to " + llList2CSV(code) + ".");
        llSetTimerEvent(0);
    }
}
```