---
name: "llGetNumberOfNotecardLines"
category: "function"
type: "function"
language: "LSL"
description: 'Requests the number of lines in notecard name via the dataserver event (cast dataserver value to integer)

Returns the handle (a key) for a dataserver event response.'
signature: "key llGetNumberOfNotecardLines(string name)"
return_type: "key"
sleep_time: "0.1"
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetNumberOfNotecardLines'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgetnumberofnotecardlines"]
---

Requests the number of lines in notecard name via the dataserver event (cast dataserver value to integer)

Returns the handle (a key) for a dataserver event response.


## Signature

```lsl
key llGetNumberOfNotecardLines(string name);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `string` | `name` | a notecard in the inventory of the prim this script is in or a UUID of a notecard |


## Return Value

Returns `key`.


## Caveats

- Forced delay: **0.1 seconds** — the script sleeps after each call.
- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetNumberOfNotecardLines)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetNumberOfNotecardLines) — scraped 2026-03-18_

Requests the number of lines in notecard name via the dataserver event (cast dataserver value to integer)Returns the handle (a key) for a dataserver event response.

## Caveats

- This function causes the script to sleep for 0.1 seconds.
- If name is missing from the prim's inventory  and it is not a UUID or it is not a notecard then an error is shouted on DEBUG_CHANNEL.
- If name is a UUID then there are no new asset permissions consequences for the object.

  - The resulting object develops no new usage restrictions that might have occurred if the asset had been placed in the prims inventory.
- If name is a new empty notecard (never saved) then an error "Couldn't find notecard ~NAME~" (~NAME~ being the value of name) will be shouted on the DEBUG_CHANNEL. This is because until a notecard is saved for the first time, it does not exist as an asset only as an inventory placeholder.

  - If the notecard is full-perms you can check for this with llGetInventoryKey which will return NULL_KEY in this case. However if notecard is not full-perms, there is no way to avoid the error message.
- If notecard contains embedded inventory items (such as textures and landmarks), invalid data will be returned.

## Examples

```lsl
// Ascertain the number of lines in a notecard in the prim's contents

string  gNotecard = "Config";       // Name of notecard to be examined
key     gLineRequestID;             // Identity of expected dataserver event
integer gLineCounter;               // The number of lines in the NC, as determined by this script

default
{
    state_entry()
    {
        // Ask how many lines are in the notecard.
        // The answer will arrive via a dataserver event
        gLineRequestID = llGetNumberOfNotecardLines(gNotecard);
    }

    dataserver(key requested, string data)
    {
        if (requested == gLineRequestID)
        {
            llOwnerSay( "The notecard '" + gNotecard + "' contains " + data + " lines" );
            // cast the data string to an integer if you need to access the counter later
            gLineCounter = (integer) data;
        }
    }
}
```

```lsl
// Check for a valid existant notecard, and read it into a list
// On touch, say the total number of lines, number of lines containing data, and say each line
// Omei Qunhua  7-Jan-2013

string  gNotecard = "Config";       // Name of notecard to be examined
key     gLineRequestID;             // Identity of expected line count dataserver event
key     gReadRequestID;             // Identity of expected data read dataserver event
integer gLineTotal;                 // The number of lines in the NC, as determined by this script
integer gLineIndex;                 // Index for data read requests
list    gDataLines;                 // List containing all data lines from notecard, excluding blank and comment lines
string  gStatus;                    // Will contain EOF when notecard reading has finished

default
{
    state_entry()
    {
        if (llGetInventoryKey(gNotecard) )         // Test if notecard exists and has been saved (returned key will be NULL_KEY otherwise)
            gLineRequestID = llGetNumberOfNotecardLines(gNotecard);       // Kick off a request for the total number of lines that the notecard contains
        else
            llOwnerSay("Notecard '" + gNotecard + "' does not exist or has no saved data");
    }
    changed(integer change)
    {
        if (change & CHANGED_INVENTORY)
            llResetScript();
    }
    dataserver(key requested, string data)
    {
        if (requested == gLineRequestID)
        {
            gLineTotal = (integer) data;           // Cast the data string to an integer to get the number of lines
            gReadRequestID = llGetNotecardLine(gNotecard, gLineIndex);      // Request a read of the first notecard line
            return;
        }
        if (requested != gReadRequestID)
            return;
        if ( (gStatus = data) == EOF)              // Save and test the current data (so that other code can tell when we've finished too)
            return;

        // A notecard line has been read. Kick off the process of fetching the next line, while we process this line
        gReadRequestID = llGetNotecardLine(gNotecard, ++gLineIndex);

        data = llStringTrim(data, STRING_TRIM);    // chop off any leading or trailing blanks
        if (data == "" || llGetSubString(data, 0, 0) == "#")
            return;                                // ignore blank or comment lines

        // Do any further processing of the data here
        gDataLines += data;                        // Add this data line to our global list
    }
    touch_start(integer total_number)
    {
        if (gStatus != EOF)
        {
            llOwnerSay("Please wait");             // Still reading the notecard
            return;
        }
        integer count = (gDataLines != [] );       // Get list length (efficient shortcut)
        llOwnerSay(gNotecard + " had a total of  " + (string) gLineTotal + " lines, of which " + (string) count + " contained data." );

        integer x;
        for ( ; x < count; ++x)                    // Loop through the data list
        {
            llOwnerSay( llList2String(gDataLines, x) );
        }
        llOwnerSay("---- end of data ----");
    }
}
```

## See Also

### Events

- dataserver

### Functions

- llGetNotecardLine

<!-- /wiki-source -->
