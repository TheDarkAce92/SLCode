---
name: "Update distributor"
category: "example"
type: "example"
language: "LSL"
description: "A simple device for distributing an updated version of a product to a list of existing customers, or in general for sending a thing to a bunch of people whose names you know."
wiki_url: "https://wiki.secondlife.com/wiki/Update_distributor"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

- 1 Introduction
- 2 Usage
- 3 Limitations and Notes
- 4 The Code

Introduction

A simple device for distributing an updated version of a product to a list of existing customers, or in general for sending a thing to a bunch of people whose names you know.

Usage

To use this script, put it into a prim, along with a notecard containing a list of names of residents (one per line), and the object to be distributed.  Then touch the prim, and it will read the notecard, determine the key of each resident, and tell you that it is not actually sending the object to each of them in turn.  Once you are satisfied that that's right, edit the script and change ACTUALLY_SEND to TRUE, save the script, and touch the object again.  This time it will actually send the thing to the people!  (Then edit it and change ACTUALLY_SEND back to FALSE, so you don't forget next time and send duplicates or something.)

Limitations and Notes

There should be exactly one notecard, and exactly one object, in the prim when you touch it.  Otherwise it will complain and not do anything.  To use it to send a texture or a script or a notecard or something, rather than an object, you'll have to modify the script.

The script uses the w-hat name2key server to get the keys of the people to send the thing to.  If that server stops working, so will this script.

The script pauses for one second after each HTTP call to the name2key server; this makes it take awhile (over a minute for a 60-name list, for instance), but also avoids HTTP throttling.  Another approach would be to explicitly check for HTTP throttling, and only slow down if it happens, but that would be more work.

The Code

You may do anything you like with this code, without limitation, subject only to the ToS, law, morality, etc.

```lsl
// Send the thing to the people listed in the notecard!
// Script by Dale Innis
// Do with this what you will, no rights reserved
// See https://wiki.secondlife.com/wiki/Update_distributor for instructions and notes

integer ACTUALLY_SEND = FALSE;   // Set to true to actually send the update to people

string URL   = "http://w-hat.com/name2key";

string ncname;
integer nextline;
string name;

key dsqkey;
key httpqkey;

order_notecard_line() {  // Request the next notecard line from the data server
    dsqkey = llGetNotecardLine(ncname,nextline);
    nextline++;
}

send_product(string name,key id) {  // Send, or pretend to, the object to the given key
    if (ACTUALLY_SEND) {
        llOwnerSay("Sending "+llGetInventoryName(INVENTORY_OBJECT,0)+" to "+name+" ("+(string)id+")");
        llGiveInventory( id, llGetInventoryName(INVENTORY_OBJECT,0) );
    } else {
        llOwnerSay("Not actually sending "+llGetInventoryName(INVENTORY_OBJECT,0)+" to "+name+" ("+(string)id+")");
    }
}

default
{
    state_entry()
    {
        // Not really anything to do here
    }

    touch_start(integer total_number)
    {
        if (llDetectedKey(0)!=llGetOwner()) return;  // Ignore non-owner touches
        if (llGetInventoryNumber(INVENTORY_NOTECARD)!=1) {
            llOwnerSay("There needs to be exactly one notecard!");
            return;
        }
        if (llGetInventoryNumber(INVENTORY_OBJECT)!=1) {
            llOwnerSay("There needs to be exactly one object!");
            return;
        }
        ncname = llGetInventoryName(INVENTORY_NOTECARD,0);
        nextline = 0;
        order_notecard_line();  // Request the first notecard line
    }

    dataserver(key id, string data) {  // A notecard line has arrived
        if (id != dsqkey) return;
        if (data==EOF) {
            llOwnerSay("Done!");
            return;
        }
        name = llStringTrim(data,STRING_TRIM);  // Strip blanks
        integer sent = FALSE;
        if (llStringLength(name)>2) {                // Ignore blanks lines
            if (llGetSubString(name,0,1)!="//") {    // Ignore lines starting with //
                httpqkey = llHTTPRequest( URL + "?terse=1&name=" + llEscapeURL(name), [], "" );
                sent = TRUE;
                llSleep(1.0);   // Avoid HTTP throttling
            }
        }
        if (sent==FALSE) {
            order_notecard_line();  // If we didn't just send for a key, send for next name.
        }
    }

    http_response(key id, integer status, list meta, string body) {  // A key has arrived
        if ( id != httpqkey )
            return;
        if ( status == 499 )
            llOwnerSay("name2key request timed out for "+name);
        else if ( status != 200 )
            llOwnerSay("the internet exploded!!  Blame "+name);
        else if ( (key)body == NULL_KEY )
            llOwnerSay("No key found for " + name);
        else
            send_product(name,(key)body);      // Send, or not, the product to the key
        order_notecard_line();                 // Then order the next name to process
    }

}
```