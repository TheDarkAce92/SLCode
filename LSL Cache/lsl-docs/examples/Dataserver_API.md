---
name: "Dataserver API"
category: "example"
type: "example"
language: "LSL"
description: "A common problem in SL is reading and parsing notecards by script. One application for this is so a script can be distributed as no-mod but still be configurable."
wiki_url: "https://wiki.secondlife.com/wiki/Dataserver_API"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

- 1 Dataserver Framework

  - 1.1 Introduction
  - 1.2 Testimonial
  - 1.3 Main Script
  - 1.4 Notecard
  - 1.5 How It Works

Dataserver Framework

### Introduction

A common problem in SL is reading and parsing notecards by script. One application for this is so a script can be distributed as no-mod but still be configurable.

The below framework demonstrates how to setup such an interface with very little work to retool.

The default state reads the notecard and when it is done it activates the configuration state.

### Testimonial

The most common problem I find is people asking about dataservers, reading from notecards to bypass variables within a notecard so you can release your script as nomod.
So I setup a simple system that I use time and time again that can be reused in any project.
The class itself is state based meaning the default state reads the notecard and then starts another state when the notecard is read and ready to use I explain this further below.

## Main Script

```lsl
string notecard_name = "configuration";  // name of notecard goes here

// internals
integer DEBUG = FALSE;
integer line;
key queryhandle;                   // to separate Dataserver requests
key notecarduuid;

init()
{
    queryhandle = llGetNotecardLine(notecard_name, line = 0);// request line
    notecarduuid = llGetInventoryKey(notecard_name);
}

// Config data loaded from notecard, with some sane defaults
integer channel = 1000;
string email_address = "revolution.perenti@skidzpartz.com";
default
{
    changed(integer change)
    {
        // We want to reload channel notecard if it changed
        if (change & CHANGED_INVENTORY)
            if(notecarduuid != llGetInventoryKey(notecard_name))
                init();
    }

    state_entry()
    {
        init();
    }

    dataserver(key query_id, string data)
    {
        if (query_id == queryhandle)
        {
            if (data != EOF)
            {   // not at the end of the notecard
                // yay!  Parsing time

                // pesky whitespace
                data = llStringTrim(data, STRING_TRIM_HEAD);

                // is it a comment?
                if (llGetSubString (data, 0, 0) != "#")
                {
                    integer s = llSubStringIndex(data, "=");
                    if(~s)//does it have an "=" in it?
                    {
                        string token = llToLower(llStringTrim(llDeleteSubString(data, s, -1), STRING_TRIM));
                        data = llStringTrim(llDeleteSubString(data, 0, s), STRING_TRIM);

                        //Insert your token parsers here.
                        if (token == "email_address")
                            email_address = data;
                        else if (token == "channel")
                            channel = (integer)data;
                    }
                }

                queryhandle = llGetNotecardLine(notecard_name, ++line);
                if(DEBUG) llOwnerSay("Notecard Data: " + data);
            }
            else
            {
                if(DEBUG) llOwnerSay("Done Reading Notecard");
                state configuration ;
            }
        }
    }
}

state configuration
{

    state_entry()
    {
        llListen(channel, "", "", "");
        llShout(0, "Channel set to " + (string)channel);
        llShout(0, "Email set to " + (string)email_address);
    }
}
```

## Notecard

```lsl
# This is the configuration file
channel = 1000
email_address = phoenixcms@hotmail.co.uk

# end
```

Lines that start with "#" are comments.

## How It Works

The default state reads and parses all the lines in the notecard. As it reads the notecard it overwrites the default values with the values in the notecard. More specifically after each line has been validated and tokenized, the token is checked against supported tokens. If the token is supported the specific parser for the token is called, in the above example it is just a simple convert and copy.

For technical support, requests, etc., use the Search under the Groups Tab and search for Dazzle Software

If you have any problems getting this script to work either contact me in-world [Revolution Perenti](https://wiki.secondlife.com/wiki/User:Revolution_Perenti)
Or visit our free scripts at our LSL scripts [www.dazzlesoftware.org](http://www.dazzlesoftware.org) Secondlife Open Source Section on Tutorials.
Latest version always available on [Marketplace](https://marketplace.secondlife.com/p/Dazzle-Software-DataServer-API/374436) or [Dazzle Software via Wyrd](http://maps.secondlife.com/secondlife/Wyrd/230/83/97)