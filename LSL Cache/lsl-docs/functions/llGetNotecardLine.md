---
name: "llGetNotecardLine"
category: "function"
type: "function"
language: "LSL"
description: 'Requests the line line of the notecard name from the dataserver.

Returns the handle (a key) for a dataserver event response.

line does not support negative indexes.
If line is past the end of the notecard EOF is returned by the dataserver.'
signature: "key llGetNotecardLine(string name, integer line)"
return_type: "key"
sleep_time: "0.1"
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetNotecardLine'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgetnotecardline"]
---

Requests the line line of the notecard name from the dataserver.

Returns the handle (a key) for a dataserver event response.

line does not support negative indexes.
If line is past the end of the notecard EOF is returned by the dataserver.


## Signature

```lsl
key llGetNotecardLine(string name, integer line);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `string` | `name` | a notecard in the inventory of the prim this script is in or a UUID of a notecard |
| `integer` | `line` | Line number in a notecard (the index starts at zero). |


## Return Value

Returns `key`.


## Caveats

- Forced delay: **0.1 seconds** — the script sleeps after each call.
- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetNotecardLine)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetNotecardLine) — scraped 2026-03-18_

Requests the line line of the notecard name from the dataserver.Returns the handle (a key) for a dataserver event response.

## Caveats

- This function causes the script to sleep for 0.1 seconds.
- If line is out of bounds  the script continues to execute without an error message.
- If name is missing from the prim's inventory  and it is not a UUID or it is not a notecard then an error is shouted on DEBUG_CHANNEL.
- If name is a UUID then there are no new asset permissions consequences for the object.

  - The resulting object develops no new usage restrictions that might have occurred if the asset had been placed in the prims inventory.
- If name is a new empty notecard (never saved) then an error "Couldn't find notecard ~NAME~" (~NAME~ being the value of name) will be shouted on the DEBUG_CHANNEL. This is because until a notecard is saved for the first time, it does not exist as an asset only as an inventory placeholder.

  - If the notecard is full-perms you can check for this with llGetInventoryKey which will return NULL_KEY in this case. However if notecard is not full-perms, there is no way to avoid the error message.
- If notecard contains embedded inventory items (such as textures and landmarks), EOF will be returned, regardless of the line requested.
- If the requested line is longer than 1024 bytes (*not* characters), dataserver will only return the first 1024 *bytes* of the line.

  - To check that the returned line has not been truncated, use the example snippet on llStringToBase64 to check the number of bytes returned in the dataserver event. If the string is exactly 1024 bytes, it *may* have been truncated.

  - Do not use llStringLength for this, because strings in LSL support multi-byte characters (UTF-8 for LSL-2, UTF-16 for Mono).
  - The maximum bytes returned by this function was increased from 255 bytes to 1024 bytes with server version [2021-10-25.565008](https://releasenotes.secondlife.com/simulator/2021-10-25.565008.html).

## Examples

```lsl
key notecardQueryId; //Identifier for the dataserver event

string notecardName = "MyNotecard"; //Name of a notecard in the object's inventory. Needs to be Full Perm for key checking for changed contents to work

integer notecardLine; //Initialize the counter value at 0

key notecardKey; //Store the notecard's key, so we don't read it again by accident.

list notecardData; //List to store data read from the notecard.

ReadNotecard()
{
    if (llGetInventoryKey(notecardName) == NULL_KEY)
    { //Check if the notecard exists in inventory, and is has been saved since it's creation (newly created notecards that are yet to be saved are assigned NULL_KEY).
        llOwnerSay( "Notecard '" + notecardName + "' is missing, unwritten, or not full permission."); //Notify user.
        return; //Don't do anything else.
    }
    else if (llGetInventoryKey(notecardName) == notecardKey) return;
    //This notecard has already been read - call to read was made in error, so don't do anything. (Notecards are assigned a new key each time they are saved.)

    llOwnerSay("Began reading notecard: " + notecardName); //Notify user that read has started.
    notecardData = []; //Clear the memory of the previous notecard.
    notecardKey = llGetInventoryKey(notecardName); //Remember the key of this iteration of the notecard, so we don't read it again by accident.
    notecardQueryId = llGetNotecardLine(notecardName, notecardLine);
}

default
{
    state_entry()
    {
        ReadNotecard(); //Pass off to the read function.
    }

    changed(integer change)
    {
        if(change & CHANGED_INVENTORY)
        { //The object's inventory just changed - the notecard could have been modified!
            ReadNotecard();
        }
    }

    dataserver(key query_id, string data)
    {
        if (query_id == notecardQueryId)
        {
            if (data == EOF) //Reached end of notecard (End Of File).
            {
                llOwnerSay("Done reading notecard, read " + (string) notecardLine + " notecard lines."); //Notify user.
                llSay(DEBUG_CHANNEL,"=== READ FROM NOTECARD: " + notecardName + " ===\n" + llDumpList2String(notecardData,"\n"));
                //Dump the contents of the notecard (for testing purposes).
            }
            else
            {
                notecardData += data; //Add the line being read to a new entry on the list.
                ++notecardLine; //Increment line number (read next line).
                notecardQueryId = llGetNotecardLine(notecardName, notecardLine); //Query the dataserver for the next notecard line.
            }
        }
    }
}
```

## See Also

### Events

- dataserver

### Functions

- llGetNumberOfNotecardLines
- llGetNotecardLineSync

<!-- /wiki-source -->
