---
name: "All button.lsl"
category: "example"
type: "example"
language: "LSL"
description: "integer toAllChannel = -255; // general channel - linked message"
wiki_url: "https://wiki.secondlife.com/wiki/All_button.lsl"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

```lsl
// Global Variables

integer toAllChannel = -255;                    // general channel - linked message

default
{
    state_entry()
    {
        llSetColor( <0,0,0>, ALL_SIDES);
    }

    touch_start(integer total_number)
    {
        llMessageLinked(LINK_ALL_OTHERS, toAllChannel, "SetTestSelected::ALL", NULL_KEY);
        llSetColor( <0,0,0>, ALL_SIDES);
    }

///////////////////////////////////////////////////////
//  Link Message of default state                    //
///////////////////////////////////////////////////////
    link_message(integer sender_number, integer number, string message, key id)
    {
        //if link message is on the correct channel
        if(number == toAllChannel)
        {
            if(llSubStringIndex( message, "TestSelectedButton") != -1)
            {
                llSetColor( <255,255,255>, ALL_SIDES);
            }
            if(message == "reset")
            {
                llResetScript();
            }

        }

    } //end of link message

}
```