---
name: "dataserver"
category: "event"
type: "event"
language: "LSL"
description: "Fires when asynchronous data arrives from functions like llGetNotecardLine, llRequestAgentData, etc."
wiki_url: "https://wiki.secondlife.com/wiki/Dataserver"
first_fetched: "2026-03-09"
last_updated: "2026-03-09"
signature: "dataserver(key queryid, string data)"
parameters:
  - name: "queryid"
    type: "key"
    description: "Matches the key returned by the requesting function"
  - name: "data"
    type: "string"
    description: "The requested data, cast to string as needed"
deprecated: "false"
---

# dataserver

```lsl
dataserver(key queryid, string data)
{
    if (queryid != myQueryId) return;
    // process data
}
```

Fires when an asynchronous data request completes. Always compare `queryid` to filter responses, as the event fires in all scripts in the prim.

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `queryid` | key | Matches the return value of the requesting function |
| `data` | string | Requested data (always a string) |

## Functions That Trigger This Event

| Function | `data` content |
|----------|---------------|
| `llGetNotecardLine` | Line text, or `EOF` if past end |
| `llGetNumberOfNotecardLines` | Line count as string integer |
| `llRequestAgentData` | Agent info (online status, name, birth, payment) |
| `llRequestDisplayName` | Agent's display name |
| `llRequestUsername` | Agent's username |
| `llRequestUserKey` | Agent UUID from name |
| `llRequestInventoryData` | Landmark position vector as string |
| `llRequestSimulatorData` | Region info (position, status, rating) |
| Key-value store functions | Operation results |

## Caveats

- Fires in **all scripts in the same prim** — always filter by `queryid`.
- Responses may arrive out of order when multiple requests are pending.
- Requests may fail due to server load — no error is guaranteed; implement timeouts.
- New dataserver requests made from within the handler are valid, but no further `dataserver` events can be received until the current handler completes.

## Example — Reading a Notecard

```lsl
string NOTECARD = "Config";
key queryId;
integer lineNum = 0;

default
{
    state_entry()
    {
        queryId = llGetNotecardLine(NOTECARD, lineNum);
    }

    dataserver(key qid, string data)
    {
        if (qid != queryId) return;

        if (data == EOF)
        {
            llOwnerSay("Done — read " + (string)lineNum + " lines");
            return;
        }

        ++lineNum;
        llOwnerSay("Line " + (string)lineNum + ": " + data);
        queryId = llGetNotecardLine(NOTECARD, lineNum);
    }
}
```

## See Also

- `llGetNotecardLine` — read notecard lines
- `llRequestAgentData` — query agent data
- `llRequestDisplayName` — get display name
- `llRequestSimulatorData` — query region data


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/dataserver) — scraped 2026-03-18_

## Caveats

- Dataserver requests will trigger **dataserver** events in all scripts within the same prim where the request was made.

  - If there are multiple scripts with **dataserver** events in the same prim, always use the `queryid` key to determine which answer is being received.
  - **dataserver** events will not be triggered in scripts contained in other prims in the same linked object.
- When dealing with multiple dataserver queries it is possible to receive the responses in any order, if you receive a response at all. It is good practise to maintain variables (or a list) with keys of all data server events you are waiting for, then use `queryid`

  - When using `if (dKey == queryid)`, or similar, in your dataserver events it is important to remember that changes to `dKey` will cause your script to ignore any requests that were made earlier that have not yet arrived; consider using more than one variable (or a list) if such cases may cause desired events to be ignored.
  - When using a list to track events, it is important to periodically check the list for requests that have taken too long and either resend them, or remove them (see examples), as it is possible for any dataserver request to fail, usually due to high traffic or the script receiving too many other events.

## Examples

```lsl
// Example script handling sequential data server events (notecard reading)

string notecardNameOrKey = "name or key of the notecard goes here";
key notecardQueryId;
integer notecardLine;//  first notecard line is 0, so we don't have to set notecardLine = 1 here

default
{
    state_entry()
    {
        llSay(0, "Reading notecard...");
        notecardQueryId = llGetNotecardLine(notecardNameOrKey, notecardLine);
    }

    dataserver(key query_id, string data)
    {
        if (query_id == notecardQueryId)
        {
            if (data == EOF)//  we have reached the EOF (end of file)
            {
                llSay(0, "No more lines in notecard, read " + (string) notecardLine + " lines.");
            }
            else
            {
            //  increment line index first, both for line number reporting, and for reading the next line
                ++notecardLine;
                llSay(0, "Line " + (string) notecardLine + ": " + data);
                notecardQueryId = llGetNotecardLine(notecardNameOrKey, notecardLine);
            }
        }
    }
}
```

```lsl
// Example script handling multiple data server events

list events;
integer stride = 3;

default
{
    touch_start(integer num_detected)
    {
        key id = llDetectedKey(0);
        events += [llRequestDisplayName(id), id, llGetUnixTime()];
        llSetTimerEvent(35.0);
    }

    dataserver(key request_id, string data)
    {
        integer index = llListFindList(events, [ request_id] );
        // The chance of getting a match on an avatar UUID instead of the dataserver event key, is less than 1 in 2^100

        if (~index )
        {
            key id = llList2Key(events, index + 1);
            llRegionSayTo(id, 0, "Hello " + data + "!");

            events = llDeleteSubList(events, index, index + stride - 1);

            if (events == [])
                llSetTimerEvent(0);
        }
    }

    timer()
    {
        integer length = (events != []);

        // Loop until we find a valid entry (as all entries after will be valid too)
        while (length && llList2Integer(events, 2) < (llGetUnixTime() - 30))
        {
            events = llDeleteSubList(events, 0, stride - 1);
            length -= stride;
        }

        if (events == [])
            llSetTimerEvent(0);
    }
}
```

## Notes

- Requesting data from within the **dataserver** event is quite valid. However, be aware that further **dataserver** events cannot be received until the event that sent the request has been completed.

<!-- /wiki-source -->
