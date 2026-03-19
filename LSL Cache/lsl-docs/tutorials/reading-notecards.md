---
name: "Reading Notecards"
category: "tutorials"
type: "reference"
language: "LSL"
description: "Reading configuration and data from notecards line by line using llGetNotecardLine and the dataserver event"
wiki_url: ""
local_only: true
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
---

# Reading Notecards

Notecards in an object's inventory are a common way to store configuration data in LSL. Reading them is asynchronous: `llGetNotecardLine` submits a request and the line arrives later via the `dataserver` event.

## How It Works

1. Call `llGetNotecardLine(name, line)` — it returns a `key` handle.
2. When the line is ready, `dataserver(key queryid, string data)` fires.
3. Match `queryid` to your stored key to confirm it is your response.
4. Check for the `EOF` constant to detect the end of the notecard.
5. Request the next line from inside the `dataserver` handler.

Lines are **0-indexed** — the first line is line `0`.

## Basic Example

```lsl
key    query_id;
integer line_num;
string  NOTECARD = "config";  // name of notecard in object inventory

default
{
    state_entry()
    {
        if (llGetInventoryType(NOTECARD) != INVENTORY_NOTECARD)
        {
            llSay(0, "Notecard '" + NOTECARD + "' not found in inventory.");
            return;
        }
        line_num = 0;
        query_id = llGetNotecardLine(NOTECARD, line_num);
    }

    dataserver(key queryid, string data)
    {
        if (queryid != query_id)
            return;  // not our response

        if (data == EOF)
        {
            llSay(0, "Finished reading. " + (string)line_num + " lines total.");
            return;
        }

        llSay(0, "Line " + (string)line_num + ": " + data);

        line_num++;
        query_id = llGetNotecardLine(NOTECARD, line_num);
    }
}
```

## Skipping Blank Lines and Comments

A common pattern is to treat lines starting with `#` as comments and ignore blank lines:

```lsl
dataserver(key queryid, string data)
{
    if (queryid != query_id)
        return;

    if (data == EOF)
    {
        llSay(0, "Done.");
        return;
    }

    // Skip blank lines and comment lines
    if (data != "" && llGetSubString(data, 0, 0) != "#")
    {
        llSay(0, "Config: " + data);
    }

    line_num++;
    query_id = llGetNotecardLine(NOTECARD, line_num);
}
```

## Reloading When the Notecard Changes

If a user edits and saves the notecard while it is in your object's inventory, the `changed` event fires with `CHANGED_INVENTORY`. Reset the script to re-read from the start:

```lsl
changed(integer change)
{
    if (change & CHANGED_INVENTORY)
        llResetScript();
}
```

## Getting the Line Count First

If you need to know how many lines are in the notecard before reading, use `llGetNumberOfNotecardLines`. It is also asynchronous, has its own **0.1-second sleep**, and returns via `dataserver`. Cast the `data` string to an integer to get the count.

```lsl
key    count_query;
key    line_query;
integer line_num;
string  NOTECARD = "config";

default
{
    state_entry()
    {
        if (llGetInventoryType(NOTECARD) != INVENTORY_NOTECARD)
        {
            llSay(0, "Notecard not found.");
            return;
        }
        count_query = llGetNumberOfNotecardLines(NOTECARD);
    }

    dataserver(key queryid, string data)
    {
        if (queryid == count_query)
        {
            integer total = (integer)data;
            llSay(0, "Notecard has " + (string)total + " lines.");
            line_num = 0;
            line_query = llGetNotecardLine(NOTECARD, line_num);
        }
        else if (queryid == line_query)
        {
            if (data == EOF)
            {
                llSay(0, "Done.");
                return;
            }
            llSay(0, data);
            line_num++;
            line_query = llGetNotecardLine(NOTECARD, line_num);
        }
    }
}
```

## Parsing Key=Value Configuration

A typical notecard format is `key=value` on each line:

```lsl
dataserver(key queryid, string data)
{
    if (queryid != query_id)
        return;

    if (data == EOF)
    {
        llSay(0, "Config loaded.");
        return;
    }

    if (data != "" && llGetSubString(data, 0, 0) != "#")
    {
        integer eq = llSubStringIndex(data, "=");
        if (eq > 0)
        {
            string cfg_key = llStringTrim(llGetSubString(data, 0, eq - 1), STRING_TRIM);
            string cfg_val = llStringTrim(llGetSubString(data, eq + 1, -1), STRING_TRIM);
            llSay(0, "Key: " + cfg_key + "  Value: " + cfg_val);
        }
    }

    line_num++;
    query_id = llGetNotecardLine(NOTECARD, line_num);
}
```

## Caveats

- `llGetNotecardLine` has a built-in **0.1-second sleep** per call. Reading a 100-line notecard takes at least 10 seconds.
- Each line has a maximum length of **1024 bytes**.
- The `dataserver` event fires in all scripts in the object — always match `queryid`.
- Multiple requests can technically be in flight simultaneously, but responses may arrive out of order. Requesting one line at a time from inside the `dataserver` handler (as shown in the examples) avoids this entirely and is the simplest correct approach.
- If the notecard is not in inventory, errors are printed on the **DEBUG_CHANNEL** and no `dataserver` event fires for that request.
