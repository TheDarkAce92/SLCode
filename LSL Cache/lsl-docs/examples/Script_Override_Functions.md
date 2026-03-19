---
name: "Script Override Functions"
category: "example"
type: "example"
language: "LSL"
description: "Well, you like to override strings, integer etc. in chat channel. For example you like to enable debug or change the channel. I find this the best solution and it can be pretty useful API framework for many listens."
wiki_url: "https://wiki.secondlife.com/wiki/Script_Override_Functions"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

/LSL

## Script Override

Well, you like to override strings, integer etc. in chat channel. For example you like to enable debug or change the channel. I find this the best solution and it can be pretty useful API framework for many listens.

#### USAGE: /CHANNEL Object_Name,message,value eg: /1000 Object,channel,1001

```lsl
list csv_commands;

integer P_channel = 1000; // channel
integer key_listen;  // listen key
default
{
    state_entry()
    {
        key_listen = llListen(P_channel, "", NULL_KEY, "");
    }

    listen(integer channel, string name, key id, string message)
    {
        csv_commands = llCSV2List( llToLower( message ));
//        string said_name = llList2String( csv_commands, 0);
        string command = llList2String( csv_commands, 1);
        if ( command == "channel")
        {
            P_channel = (integer)llList2String( csv_commands, 2);
            llListenRemove( key_listen );
            key_listen = llListen(P_channel, "","","");
            llOwnerSay( "Listen Channel set to " + (string)P_channel);
        }
        else if(command == "avatar" || message == "AVATAR")
        {
            llSay(0, "Hello, Avatar!");
        }
    }
}
```

#### Support

For technical support, requests, etc., use the Search under the Groups Tab and search for Dazzle Software

If you have any problems getting this script to work either contact me in-world [Revolution Perenti](https://wiki.secondlife.com/wiki/User:Revolution_Perenti)
Or visit our free scripts at our LSL scripts [www.dazzlesoftware.org](http://www.dazzlesoftware.org) Secondlife Open Source Section on Tutorials.
Latest version always available on [Dazzle Software via Wyrd](http://maps.secondlife.com/secondlife/Wyrd/230/83/97)