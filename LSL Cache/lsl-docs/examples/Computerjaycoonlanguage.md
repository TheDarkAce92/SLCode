---
name: "Computer:jaycoonlanguage"
category: "example"
type: "example"
language: "LSL"
description: "This is a language that is written in LSL. It reads a notecard specified by the user (meant for use with my computer that you can buy here: http://slurl.com/secondlife/Coda/249/46/73)"
wiki_url: "https://wiki.secondlife.com/wiki/Computer:jaycoonlanguage"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

This is a language that is written in LSL. It reads a notecard specified by the user (meant for use with my computer that you can buy here: [http://slurl.com/secondlife/Coda/249/46/73](http://slurl.com/secondlife/Coda/249/46/73))

```lsl
//  initialised: Starts un initialised
integer open  = FALSE;

string notecard;

key notecardLineQueryID;
key notecardTextQueryID;

integer lines;
string process;
string line;
string notcard;
list ints;
list strings;

default
{
    state_entry()
    {
    //  PUBLIC_CHANNEL has the integer value 0
        llListen(PUBLIC_CHANNEL, "", NULL_KEY, "");
        llListen(4, "", NULL_KEY, "");
    }

    listen(integer channel, string name, key id, string message)
    {
    //  init start
        if(message == "os:load progs")
            llSay(4, "prog:jaycoonlanguage");

        else if(message == "bios:startjaycoonlanguage")
            open = TRUE;

        else if(message == "close" && open)
            open = FALSE;
    //  init done

    //  set notecard
        if(~llSubStringIndex(message, "notecard:") && open)
            notecard = llDeleteSubString(message, 0, 9);

        if(message == "compile" && notecard != "" && open)
        {
        //  start compiling
            notecardLineQueryID = llGetNumberOfnotecardLineQueryIDs(notecard);
            process = "lines";
            integer contvar = 0;
            while (contvar <= lines)
            {
                notecardTextQueryID = llGetnotecardLineQueryID(notecard,contvar);

                if(~llSubStringIndex(line, "print:"))
                {
                    line = llDeleteSubString(line,0,6);

                    if(~llListFindList(ints, [line]))
                        llSay(PUBLIC_CHANNEL,
                            llList2String(ints,llListFindList(ints, [line])));

                    if(~llListFindList(strings, [line]))
                        llSay(PUBLIC_CHANNEL,
                            llList2String(ints,llListFindList(strings, [line])));

                    llSay(PUBLIC_CHANNEL, line);
                }
                if(~llSubStringIndex(line, "int:"))
                {
                    line = llDeleteSubString(line, 0, 4);
                    ints += (integer)line;
                }
                if(~llSubStringIndex(line, "string:"))
                {
                    line = llDeleteSubString(line, 0, 4);
                    strings += (string)line;
                }

                ++contvar;
            }
        }
    }

    dataserver(key query_id, string data)
    {
        if(query_id == notecardLineQueryID)
            lines = (integer)data;

        if(query_id == notecardTextQueryID)
            line = data;
    }
}
```