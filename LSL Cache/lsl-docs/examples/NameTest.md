---
name: "NameTest"
category: "example"
type: "example"
language: "LSL"
description: "key owner_key; // to filter out owner chat integer name_channel; integer name_listener = 0;"
wiki_url: "https://wiki.secondlife.com/wiki/NameTest"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

## Library

```lsl
string  previous_name;
key     previous_key;

key     owner_key; // to filter out owner chat
integer name_channel;
integer name_listener = 0;

key     requestor;

key     name_key_query;
key     key_name_query;

integer pickChannel()
{
   return (integer)("0x"+llGetSubString((string)llGetKey(),-8,-1));
}

askForPreviousName(key agent, string prompt)
{
    name_listener = llListen(name_channel, "", "", "");
    llTextBox( agent, prompt, name_channel );
}

string nameFilter(string possibleName)
{
    string candidate_name = "";

    list name_list = llParseString2List( llStringTrim(possibleName, STRING_TRIM), [" ","."], [] );

    integer number_of_words = llGetListLength(name_list);
    if (number_of_words == 0)
    {
        llRegionSayTo(requestor, 0, "No name found");
    }
    else if (number_of_words > 2)
    {
        llRegionSayTo(requestor, 0, "That is too many words to be a name");
    }
    else
    {
        candidate_name = llDumpList2String(name_list,".");
    }
    return candidate_name;
}

default
{
    on_rez(integer unused)
    {
        llResetScript();
    }

    state_entry()
    {
        owner_key = llGetOwner();
        name_channel = pickChannel();

        vector ORANGE  = <1    , 0.522, 0.106>;
        llSetText("Touch to translate a previous name", ORANGE, 1.0);
    }

    touch_start(integer num_touches)
    {
        requestor = llDetectedKey(0);
        if (owner_key == requestor)
        {
            askForPreviousName(owner_key, "Enter an old name:");
        }
        else
        {
            askForPreviousName(requestor, "Enter your previous name:");
        }
    }

    listen(integer channel, string name, key id, string message)
    {
        if (channel == name_channel)
        {
            previous_name = nameFilter(message); // will send any error message to the id
            if (llStringLength(previous_name) > 0)
            {
                state key_query;
            }
        }
    }
}

state key_query
{
    state_entry()
    {
        name_key_query = llRequestUserKey(previous_name);
    }

    dataserver(key queryid, string data)
    {
        if ( name_key_query == queryid )
        {
            previous_key = (key)data;
            if (previous_key == NULL_KEY)
            {
                llRegionSayTo(requestor, 0, "'"+previous_name+"' is not a valid name");
                state default;
            }
            else
            {
                state name_query;
            }
        }
    }

    state_exit()
    {
        name_key_query = NULL_KEY;
    }
}

state name_query
{
    state_entry()
    {
        key_name_query = llRequestUsername(previous_key);
    }

    dataserver(key queryid, string data)
    {
        if ( key_name_query == queryid )
        {
            if (data == previous_name)
            {
                llSay(0,"'"+previous_name+"' is the current name");
            }
            else
            {
                llSay(0,"'"+data+"' was '"+previous_name+"'");
            }
            state default;
        }
    }

    state_exit()
    {
        key_name_query = NULL_KEY;
        previous_name = "";
        previous_key = NULL_KEY;
    }
}
```