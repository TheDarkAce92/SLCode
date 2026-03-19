---
name: "llClearLinkMedia"
category: "function"
type: "function"
language: "LSL"
description: 'Clears (deletes) the media and all params from the given face on the linked prim(s).

Returns a status (an integer) that is a STATUS_* flag which details the success/failure of the operation.'
signature: "integer llClearLinkMedia(integer link, integer face)"
return_type: "integer"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llClearLinkMedia'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llclearlinkmedia"]
---

Clears (deletes) the media and all params from the given face on the linked prim(s).

Returns a status (an integer) that is a STATUS_* flag which details the success/failure of the operation.


## Signature

```lsl
integer llClearLinkMedia(integer link, integer face);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `integer (link)` | `link` | Link number (0: unlinked, 1: root prim, >1: child prims and seated avatars) or a LINK_* flag |
| `integer` | `face` | face number |


## Return Value

Returns `integer`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llClearLinkMedia)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llClearLinkMedia) — scraped 2026-03-18_

Clears (deletes) the media and all params from the given face on the linked prim(s).Returns a status (an integer) that is a STATUS_* flag which details the success/failure of the operation.

## Caveats

- link needs to be either an actual link number or a link constants that equate to a single prim, such as LINK_ROOT and LINK_THIS.

  - LINK_SET, LINK_ALL_CHILDREN and LINK_ALL_OTHERS will not work.
- The function silently fails if its face value indicates a face that does not exist.

## Examples

```lsl
//  when dropping this script into an object
//  it will remove all set media-on-a-prim
//  on all sides of every prim and then
//  the script will delete itself

integer GetPrimCount()
{
    if(llGetAttached())
        return llGetNumberOfPrims();

    return llGetObjectPrimCount(llGetKey());
}

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
        integer numOfPrims = GetPrimCount();
        integer numOfSides;

        integer link;
        integer face;

        if (1 < numOfPrims)
            link = 1;

        do
        {
            numOfSides = llGetLinkNumberOfSides(link);
            face = 0;
            do
            {
                integer clearLinkMediaSuccessFlag = llClearLinkMedia(link, face);
                publish_returned_status_flag(link, face, clearLinkMediaSuccessFlag);

                ++face;
            }
            while (face < numOfSides);

            if (numOfPrims == 1)
                jump continue;

            ++link;
        }
        while (link <= numOfPrims);

        @continue;

        string thisScript = llGetScriptName();
        llRemoveInventory(thisScript);
    }
}
```

## Notes

### Link Numbers

Each prim that makes up an object has an address, a link number. To access a specific prim in the object, the prim's link number must be known. In addition to prims having link numbers, avatars seated upon the object do as well.

- If an object consists of only one prim, and there are no avatars seated upon it, the (root) prim's link number is zero.
- However, if the object is made up of multiple prims or there is an avatar seated upon the object, the root prim's link number is one.

When an avatar sits on an object, it is added to the end of the link set and will have the largest link number. In addition to this, while an avatar is seated upon an object, the object is unable to link or unlink prims without unseating all avatars first.

#### Counting Prims & Avatars

There are two functions of interest when trying to find the number of prims and avatars on an object.

- `llGetNumberOfPrims()` - Returns the number of prims and seated avatars.
- `llGetObjectPrimCount(llGetKey())` - Returns only the number of prims in the object but will return zero for attachments.

```lsl
integer GetPrimCount() { //always returns only the number of prims
    if(llGetAttached())//Is it attached?
        return llGetNumberOfPrims();//returns avatars and prims but attachments can't be sat on.
    return llGetObjectPrimCount(llGetKey());//returns only prims but won't work on attachments.
}
```

See llGetNumberOfPrims for more about counting prims and avatars.

#### Errata

If a script located in a child prim erroneously attempts to access link 0, it will get or set the property of the linkset's root prim.  This bug ([BUG-5049](https://jira.secondlife.com/browse/BUG-5049)) is preserved for broken legacy scripts.

## See Also

### Functions

- **llGetLinkNumber** — prim
- llClearPrimMedia
- llSetLinkMedia
- llGetLinkMedia

<!-- /wiki-source -->
