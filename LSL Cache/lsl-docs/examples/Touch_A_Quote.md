---
name: "Touch A Quote"
category: "example"
type: "example"
language: "LSL"
description: "This script will deliver quotes sequentially from a notecard when touched."
wiki_url: "https://wiki.secondlife.com/wiki/Touch_A_Quote"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

This script will deliver quotes sequentially from a notecard when touched.

In the same object you drop this script, create a notecard called "_quotes" and simply put your quotes in it, max. 255 characters per line or they will be truncated. Watch out not to bust the script memory stack by adding too much, but you can use Mono to compile it and create a very long notecard.

```lsl
// Touch a quote script
// By CodeBastard Redgrave
// Reads quotes from a notecard and displays them sequentially when you touch!
// BEWARE it cannot handle quotes more than 256 characters. Split them into multiple lines if needed.

// This is a free script, DO NOT RESELL!
// It's loosely based on the classic dataserver script from the LSL wiki.
// Feel free to modify it to make your own book! Make code not war <3

string notecardName = "<--the notecard name goes here -->";

integer currentLine;
key notecardRequestID;

integer quoteIndex;
integer numberOfQuotes;
list listOfQuotes;

init()
{
    integer numberOfNotecards = llGetInventoryNumber(INVENTORY_NOTECARD);

    if (numberOfNotecards)
    {
        currentLine = 0;
        notecardRequestID = llGetNotecardLine(notecardName, currentLine);

        llOwnerSay("Loading notecards now...");
    }
}

default
{
    on_rez(integer start_param)
    {
         llResetScript();
    }

    changed(integer change)
    {
        if (change & CHANGED_INVENTORY)
            llResetScript();
    }

    state_entry()
    {
        init();
    }

    touch_start(integer num_detected)
    {
        llSay(PUBLIC_CHANNEL, llList2String(listOfQuotes, quoteIndex));

        if (numberOfQuotes <= ++quoteIndex)
            quoteIndex = 0;

    }

    dataserver(key id, string data)
    {
        notecardRequestID = NULL_KEY;

        if (data == EOF)
        {
            currentLine = 0;

            numberOfQuotes = llGetListLength(listOfQuotes);
            integer freeMemory = llGetFreeMemory();

            llOwnerSay("Done loading notecards!\n"
                + (string)numberOfQuotes + " quotes loaded, free memory " + (string)freeMemory);
        }
        else
        {
            if (data != "")
                listOfQuotes += [data];

            notecardRequestID = llGetNotecardLine(notecardName, ++currentLine);
        }
    }
}
```