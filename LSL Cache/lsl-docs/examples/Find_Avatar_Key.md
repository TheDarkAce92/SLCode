---
name: "Find Avatar Key"
category: "example"
type: "example"
language: "LSL"
description: "Explores UUID of avatar whose name is said in local chat or who touches the prim. Uses Name2Key code published in LSL Library."
wiki_url: "https://wiki.secondlife.com/wiki/Find_Avatar_Key"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

## Find Avatar Key

Explores UUID of avatar whose name is said in local chat or who touches the prim.
Uses Name2Key code published in LSL Library.

**Requirements:**

- Place this script into a single prim and decorate to taste.

**Operation:**

- No special instructions. It operates stand alone once installed.

```lsl
// Find Avatar Key Script
// by Huney Jewell
// based on Name2Key code published in LSL Library
//
// Put in single prim
// Explores UUID of avatar whose name is said in local chat or who touches the prim
// LL Search engine sometimes returns wrong profile, hence lookup may fail.
// Then the only method to explore the key is by touching the prim
//

// GLOBALS
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// System settings - Do Not Change Anything Below!

//string search    = "http://lawlinter.net/secondlifeutility/name2key.php5?name="; // Name2Key URL
string search    = "http://w-hat.com/name2key?terse=1&name="; // Alternate Name2Key URL
string notFound  = "00000000-0000-0000-0000-000000000000";

list   requests  = [];

// CODE ENTRY
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

default
{
    on_rez(integer i)
    {
        llResetScript();
    }

    state_entry()
    {
        llSay(0, "Ready. Say \"/1 firstname lastname\" or touch me");
        llListen(1, "", "", "");
    }

    touch_start(integer total_number)
    {
        integer i = 0;
        for (; i < total_number; ++i)
        {
            llSay(0, llDetectedName(i) + " = " + (string)llDetectedKey(i));
        }
    }

    listen(integer c, string n, key i, string msg)
    {
        list nameParts = llParseString2List(msg, [" "], []);
        if (llGetListLength(nameParts) < 2)
            llSay(0,"Name '" + msg + "' incomplete, try again.");
        else
        {
            string firstName = llList2String(nameParts, 0);
            string lastName = llList2String(nameParts, 1);
            string name = firstName + " " + lastName;
            llSay(0,"Requesting key for " + name);
            if(llListFindList(requests,[name]) == -1)
            {
                key id = llHTTPRequest(search + firstName + "+" + lastName, [], "");
                requests += [id,name];
            }
        }
    }

    http_response(key request_id, integer status, list metadata, string body)
    {
        //        llOwnerSay("Status:" + (string) status + "; Body: " + body); // DEBUG
        integer position = llListFindList(requests,[request_id]);
        if (position != -1)
        {
            string name = llList2String(requests,position+1);
            if (status == 200)
            {
                string avKey = llGetSubString(body,0,35);
                if (avKey != notFound)
                    llSay(0,name + " = " + avKey);
                else
                    llSay(0,"Lookup '" + name + "' failed: Not found.");
            }
            else
            {
                if (status == 499)
                    llSay(0,"Lookup '" + name + "' timed out, try again.");
                else
                    llSay(0,"Lookup '" + name + "' failed: HTTP error code " + (string)status);
            }
            requests = llDeleteSubList(requests,position,position+1);
        }
    }
}
```

## Comments

The search URL needed to be changed as of 2010-01-10 to comply with modification of LL HTML code, which apparently moved the requested key out of LSL limit for body parameter (within http_response event).

Also note that the original URL doesn't seem to respond, as of 2025. W-hat's website (set as 'secondary') is still fully operational! — Gwyneth Llewelyn (talk) 07:26, 4 January 2025 (PST)