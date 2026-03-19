---
name: "Tail Messages (NewAge)"
category: "example"
type: "example"
language: "LSL"
description: "Copy and Paste this into your tail and edit some things you may want to change like the announce_type and menu timeout."
wiki_url: "https://wiki.secondlife.com/wiki/Tail_Messages_(NewAge)"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

New Age Tail Click Script

Copy and Paste this into your tail and edit some things you may want to change like the `announce_type` and menu timeout.

To add more options, go to the list buttons, after "Kiss" you need to add a , then new space so it's like this:

```lsl
"Kiss",
"New button here"
];
```

As you add new buttons, you need to add to the messages as well in the same order as the buttons otherwise it will mess up.

```lsl
/////////////////////////////////
// New Age Tail Click Script
// By Asia Snowfall
// Version 1.0
/////////////////////////////////

string announce_type = "say";
// Replace say with either:
// "shout" = to shout out messages
// "whisper" = to whisper the messages

float seconds_till_menu_timeout = 30;

list buttons = [
"Hug",
"Stroke",
"Kiss"
];

list messages = [
" picks up 's tail and hugs it gently",
" gently strokes their fingers through 's tail",
" picks up 's tail and kisses it"
];

string menu_text = "'s Tail Menu\nWhat do you want to do with my tail ?";

// Message Tags;
//  = Person clicking the button's first name will appear there
//  = Person clicking the button's last name will appear there
//  = Tail owners first name will appear there
//  = Tail owners last name will appear there

integer chan;
integer hand;

asMenuSetup(key id)
{
    llListenRemove(hand);
    chan = llRound(llFrand(99999)+10);
    hand = llListen(chan, "", id, "");
    if(llGetListLength(buttons) > 12)
    {
        llOwnerSay("Error: There is more than 12 options, please reduce the ammount");
    }
    else
    {
        llDialog(id, asTagScan(menu_text, id), buttons, chan);
    }
}

asCheckSelected(string message, key id)
{
    llListenRemove(hand);
    integer index = llListFindList(buttons, [message]);
    if(index != -1)
    {
        if(llToLower(announce_type) == "say")
        {
            llSay(0, asTagScan(llList2String(messages, index), id));
        }
        else if(llToLower(announce_type) == "shout")
        {
            llShout(0, asTagScan(llList2String(messages, index), id));
        }
        else
        {
            llWhisper(0, asTagScan(llList2String(messages, index), id));
        }
    }
}


string asTagScan(string message, key user)
{
    integer ufn = llStringLength("")-1;
    integer uln = llStringLength("")-1;
    integer ofn = llStringLength("")-1;
    integer oln = llStringLength("")-1;
    list parse = llParseString2List(llKey2Name(user), [" "], []);
    string user_first_name = llList2String(parse, 0);
    string user_last_name = llList2String(parse, 1);
    parse = llParseString2List(llKey2Name(llGetOwnerKey(llGetKey())), [" "], []);
    string owner_first_name = llList2String(parse, 0);string owner_last_name = llList2String(parse, 1);integer ind;integer ind2;integer own;integer own2;integer done = FALSE;
    do
    {
        @recheck;
        ind = llSubStringIndex(message, "");
        ind2 = llSubStringIndex(message, "");
        own = llSubStringIndex(message, "");
        own2 = llSubStringIndex(message, "");
        if(ind != -1)
        {
            message = llDeleteSubString(message, ind, (ind+ufn));
            message = llInsertString(message, ind, user_first_name);
            jump recheck;
        }
        else if(ind2 != -1)
        {
            message = llDeleteSubString(message, ind2, (ind2+uln));
            message = llInsertString(message, ind2, user_last_name);
            jump recheck;
        }
        else if(own != -1)
        {
            message = llDeleteSubString(message, own, (own+ofn));
            message = llInsertString(message, own, owner_first_name);
            jump recheck;
        }
        else if(own2 != -1)
        {
            message = llDeleteSubString(message, own2, (own2+oln));
            message = llInsertString(message, own2, owner_last_name);
            jump recheck;
        }
        else if(ind == -1 && ind2 == -1 && own == -1 && own2 == -1)
        {
            done = TRUE;
        }
    }while(done < FALSE);
    return message;
}

default
{
    touch_start(integer x)
    {
        asMenuSetup(llDetectedKey(0));
        llSetTimerEvent(seconds_till_menu_timeout);
    }
    listen(integer channel, string name, key id, string str)
    {
        asCheckSelected(str, id);
    }
    timer()
    {
        llListenRemove(hand);
        llSetTimerEvent(0);
    }
}
```