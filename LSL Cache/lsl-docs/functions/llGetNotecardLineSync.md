---
name: "llGetNotecardLineSync"
category: "function"
type: "function"
language: "LSL"
description: 'Gets the line line of the notecard name from the dataserver immediately, provided it is cached, and without raising a dataserver event.

line does not support negative indexes.
Returns EOF if line is past the end of the notecard.'
signature: "string llGetNotecardLineSync(string name, integer line)"
return_type: "string"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetNotecardLineSync'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
---

Gets the line line of the notecard name from the dataserver immediately, provided it is cached, and without raising a dataserver event.

line does not support negative indexes.
Returns EOF if line is past the end of the notecard.


## Signature

```lsl
string llGetNotecardLineSync(string name, integer line);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `string` | `name` | a notecard in the inventory of the prim this script is in or a UUID of a notecard |
| `integer` | `line` | Line number in a notecard (the index starts at zero). |


## Return Value

Returns `string`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetNotecardLineSync)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetNotecardLineSync) — scraped 2026-03-18_

Gets the line of the notecard name from the region's notecard cache immediately without raising a dataserver event.Returns the string containing the text of the requested line from the notecard.

## Caveats

- If line is out of bounds  the script continues to execute without an error message.
- If name is missing from the prim's inventory  and it is not a UUID or it is not a notecard then an error is shouted on DEBUG_CHANNEL.
- If name is a UUID then there are no new asset permissions consequences for the object.

  - The resulting object develops no new usage restrictions that might have occurred if the asset had been placed in the prims inventory.
- If name is a new empty notecard (never saved) then an error "Couldn't find notecard ~NAME~" (~NAME~ being the value of name) will be shouted on the DEBUG_CHANNEL. This is because until a notecard is saved for the first time, it does not exist as an asset only as an inventory placeholder.

  - If the notecard is full-perms you can check for this with llGetInventoryKey which will return NULL_KEY in this case. However if notecard is not full-perms, there is no way to avoid the error message.
- If notecard contains embedded inventory items (such as textures and landmarks), EOF will be returned, regardless of the line requested.
- If the requested line is longer than 1024 bytes (*not* characters), llGetNotecardLineSync will only return the first 1024 *bytes* of the line.

  - To check that the returned line has not been truncated, use the example snippet on llStringToBase64 to check the number of bytes returned by llGetNotecardLineSync. If the string is exactly 1024 bytes, it *may* have been truncated.

  - Do not use llStringLength for this, because strings in LSL support multi-byte characters (UTF-8 for LSL-2, UTF-16 for Mono).
- A dataserver event does **not** get raised. Therefore, other scripts in the linkset are unaware of the processed notecard lines.
- Since this function does not idle the script while waiting for a dataserver event, garbage collection will not run while loading an entire notecard by calling llGetNotecardLineSync in a loop. For large notecards, you can quickly run out of free memory, even if you overwrite each line as you read it.

  - This does not occur with llGetNotecardLine, which runs garbage collection while waiting for the dataserver event.
  - This can be mitigated using timers (any length will do), but not llSleep, which also blocks garbage collection.

## Examples

```lsl
string NOTECARD_NAME = "notecard";
key READ_KEY = NULL_KEY;

default
{

    touch_start(integer total_number)
    {
        READ_KEY = llGetNumberOfNotecardLines(NOTECARD_NAME);
    }

    dataserver(key request, string data)
    {
        if (request == READ_KEY)
        {
            integer count = (integer)data;
            integer index;

            for (index = 0; index < (count+1); ++index)
            {
                string line = llGetNotecardLineSync(NOTECARD_NAME, index);
                if (line == NAK)
                {
                    llOwnerSay("---NAK---");
                }
                else if (line == EOF)
                {
                    llOwnerSay("---EOF---");
                }
                else
                {
                    llOwnerSay(line);
                }
            }
        }
    }
}
```

Following example to call a normal dataserver notecard read using llGetNotecardLine if llGetNotecardlineSync fails with a NAK.  Keep in mind to clear any lists you are reading data into when using the following example to keep from corrupting the integrity of the list data.

```lsl
// llGetNotecardLineSync example with fall back to the old dataserver read
// if llGetNotecardLineSync fails with a NAK.

string  NOTECARD_NAME = "notecard";
key     READ_KEY = NULL_KEY;

key     noteCard_qry;
integer noteCard_line;

default
{

    state_entry()
    {
        // read the notecards number of lines to the
        // simulators cache memory
        READ_KEY = llGetNumberOfNotecardLines(NOTECARD_NAME);
    }

    dataserver(key request, string data)
    {
        // read notecards using the new llGetNotecardLineSync function
        // from simulator cache.
        if (request == READ_KEY)
        {
            integer count = (integer)data;
            integer index;

            for (index = 0; index < (count+1); ++index)
            {
                string line = llGetNotecardLineSync(NOTECARD_NAME, index);
                if (line == NAK)
                {
                    // Got a notecard NAK meaning llGetNotecardLineSync had and error.
                    // falling back to the old dataserver event to read notecards.
                    llOwnerSay("---NAK---");
                    noteCard_qry = llGetNotecardLine(NOTECARD_NAME, noteCard_line);
                    return;  // return is needed to break the for/next loop once the NAK is encountered.
                }
                else if (line == EOF)
                {
                    // End of notecard.
                    llOwnerSay("---EOF---");
                }
                else
                {
                    // do work here.
                    llOwnerSay(line);
                }
            }
        }

        // old system takes over if a NAK is encountered.
        if(request == noteCard_qry)
        {
            if(data == EOF)
            {
                // End of notecard encountered.
                llOwnerSay("EOF encountered");
            }
            else
            {
                // process normal notecard line, then read the next line
                // of the notecard.
                llOwnerSay(data);
                noteCard_qry = llGetNotecardLine(NOTECARD_NAME, ++noteCard_line);
            }
        }
    }
}
```

Here is a more compact implementation that returns to using llGetNotecardLineSync whenever possible:

```lsl
string file_name;
integer file_line_number;
key file_request;

default {
    state_entry() {
        file_name = llGetInventoryName(INVENTORY_NOTECARD, 0); // get the name of the first notecard in the object's inventory
    }

    touch_start(integer n) {
        // start reading text when the object is touched (you'll probably want to move these lines to another place depending on your needs):
        file_line_number = 0;
        file_request = llGetNotecardLine(file_name, file_line_number);
    }

    dataserver(key id, string message) {
        if (id == file_request) {
            while (message != EOF && message != NAK) {
                llOwnerSay(message); // do useful things with the text here
                message = llGetNotecardLineSync(file_name, ++file_line_number);
            }
            if (message == NAK)
                file_request = llGetNotecardLine(file_name, file_line_number);
            if (message == EOF)
                llOwnerSay("End of file.");
        }
    }
}
```

## See Also

### Functions

- llGetNumberOfNotecardLines
- llGetNotecardLine

<!-- /wiki-source -->
