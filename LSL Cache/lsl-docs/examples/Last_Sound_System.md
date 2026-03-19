---
name: "Last Sound System"
category: "example"
type: "example"
language: "LSL"
description: "integer gDialogChannel = 7777; list gInfo; integer gDialogHandle; key gDialogKey; key gHandshakeRequestKey; string gStationURL;"
wiki_url: "https://wiki.secondlife.com/wiki/Last_Sound_System"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

```lsl
// Last Sound System by Babbage Linden
//
// An Open Source last.fm radio client for Second Life
// based on lastFMProxy by Vidar Madsen
//
// Available under the Creative Commons Attribution-ShareAlike 2.5 license
// http://creativecommons.org/licenses/by-sa/2.5/

integer gDialogChannel = 7777;
list gInfo;
integer gDialogHandle;
key gDialogKey;
key gHandshakeRequestKey;
string gStationURL;

list parseLine(string line)
{
    list tokens;
    integer lineIndex = llSubStringIndex(line, "=");
    tokens += llGetSubString(line, 0, lineIndex - 1);
    tokens += llGetSubString(line, lineIndex + 1, -1);
    return tokens;
}

list parseLines(string lines)
{
    list tokens;
    integer index = llSubStringIndex(lines, "\n");
    while(index != -1)
    {
        string line = llGetSubString(lines, 0, index - 1);
        tokens += parseLine(line);
        lines = llDeleteSubString(lines, 0, index);
        index = llSubStringIndex(lines, "\n");
    }
    tokens += parseLine(lines);
    return tokens;
}

string getValue(list pairs, string name)
{
    integer length = llGetListLength(pairs);
    integer i;
    for(i = 0; i < length; i += 2)
    {
        if(llList2String(pairs, i) == name)
        {
            return llList2String(pairs, i + 1);
        }
    }
    return "";
}

reset()
{
    if(llGetInventoryType("Config") != INVENTORY_NOTECARD)
    {
        llSay(0, "ERROR: Config notecard not found");
    }
    else
    {
        llGetNotecardLine("Config", 0);
    }
}

default
{
    state_entry()
    {
        gDialogHandle = llListen(gDialogChannel, "", NULL_KEY, "");
    }

    state_exit()
    {
        llListenRemove(gDialogHandle);
    }

    touch_start(integer num)
    {
        key gDialogKey = llDetectedKey(0);
        llDialog(gDialogKey, "Last Sound System Control", ["skip", "love", "ban", "reset"], gDialogChannel);
    }

    listen(integer channel, string name, key id, string message)
    {
        if(channel == gDialogChannel)
        {
            if(message == "reset")
            {
                reset();
            }
            else
            {
                // Send command.
                string url = "http://" + getValue(gInfo, "base_url");
                url += "/" + getValue(gInfo, "base_path");
                url += "/control.php?command=" + message + "&session=" + getValue(gInfo, "session");
                llHTTPRequest(url, [], "");
            }
        }
    }

    dataserver(key id, string data)
    {
        list values = llCSV2List(data);
        if(llGetListLength(values) != 3)
        {
            llSay(0, "ERROR: Config notecard must contain \",,\"");
        }
        else
        {
            string username = llList2String(values, 0);
            string md5password = llToLower(llList2String(values, 1));
            gStationURL = llList2String(values, 2);

            // Create session.
            string url = "http://ws.audioscrobbler.com/radio/handshake.php?";
            url += "version=1.0.1&platform=linux&username=" + username;
            url += "&passwordmd5=" + md5password + "&debug=0";
            gHandshakeRequestKey = llHTTPRequest(url, [], "");
        }
    }

    http_response(key id, integer status, list metadata, string body)
    {
        if(status == 200)
        {
            if(id == gHandshakeRequestKey)
            {
                gInfo = parseLines(body);

                llSetParcelMusicURL(getValue(gInfo, "stream_url"));

                // Set station.
                string url = "http://" + getValue(gInfo, "base_url");
                url += "/" + getValue(gInfo, "base_path");
                url += "/adjust.php?session=" + getValue(gInfo, "session");
                url += "&url=" + gStationURL;
                llHTTPRequest(url, [], "");
            }
        }
        else
        {
            llSay(0, "ERROR:" + (string)status + ":" + body);
        }
    }
}
```