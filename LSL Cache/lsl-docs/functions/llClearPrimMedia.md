---
name: "llClearPrimMedia"
category: "function"
type: "function"
language: "LSL"
description: 'Clears (deletes) the media and all params from the given face.

Returns a status (an integer) that is a STATUS_* flag which details the success/failure of the operation.'
signature: "integer llClearPrimMedia(integer face)"
return_type: "integer"
sleep_time: "1.0"
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llClearPrimMedia'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llclearprimmedia"]
---

Clears (deletes) the media and all params from the given face.

Returns a status (an integer) that is a STATUS_* flag which details the success/failure of the operation.


## Signature

```lsl
integer llClearPrimMedia(integer face);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `integer` | `face` | face number |


## Return Value

Returns `integer`.


## Caveats

- Forced delay: **1.0 seconds** — the script sleeps after each call.
- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llClearPrimMedia)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llClearPrimMedia) — scraped 2026-03-18_

Clears (deletes) the media and all params from the given face.Returns a status (an integer) that is a STATUS_* flag which details the success/failure of the operation.

## Caveats

- This function causes the script to sleep for 1.0 seconds.
- The function silently fails if its face value indicates a face that does not exist.

## Examples

```lsl
//  when dropping this script into a prim
//  it will remove all set media-on-a-prim
//  on all sides of the prim containing the script
//  and then the script will delete itself

publish_returned_status_flag(integer inputLink, integer inputFace, integer inputStatus)
{
    /* if (inputInteger == 0) */ string outputStatus = "STATUS_OK";
    if (inputStatus == 1000) outputStatus = "STATUS_MALFORMED_PARAMS";
    else if (inputStatus == 1001) outputStatus = "STATUS_TYPE_MISMATCH";
    else if (inputStatus == 1002) outputStatus = "STATUS_BOUNDS_ERROR";
    else if (inputStatus == 1003) outputStatus = "STATUS_NOT_FOUND";
    else if (inputStatus == 1004) outputStatus = "STATUS_NOT_SUPPORTED";
    else if (inputStatus == 1999) outputStatus = "STATUS_INTERNAL_ERROR";
    else if (inputStatus == 2001) outputStatus = "STATUS_WHITELIST_FAILED";

    // PUBLIC_CHANNEL has the integer value 0
    llSay(PUBLIC_CHANNEL, "llClearLinkMedia(link " + (string)inputLink
        + ", face " + (string)inputFace + ") = " + outputStatus + ";");
}

default
{
    state_entry()
    {
        integer link = llGetLinkNumber();
        integer numOfSides = llGetLinkNumberOfSides(link);
        integer face;

        do
        {
            integer clearMediaSucceeded = llClearPrimMedia(face);
            publish_returned_status_flag(link, face, clearMediaSucceeded);

            ++face;
        }
        while (face < numOfSides);

        string thisScript = llGetScriptName();
        llRemoveInventory(thisScript);
    }
}
```

## See Also

### Functions

- llClearLinkMedia
- llSetPrimMediaParams
- llGetPrimMediaParams

<!-- /wiki-source -->
