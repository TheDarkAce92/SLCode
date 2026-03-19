---
name: "llGetObjectLinkKey"
category: "function"
type: "function"
language: "LSL"
description: "Returns the key of the linked prim link in the linkset identified by object_id"
signature: "key llGetObjectLinkKey(key id, integer link)"
return_type: "key"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetObjectLinkKey'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
---

Returns the key of the linked prim link in the linkset identified by object_id


## Signature

```lsl
key llGetObjectLinkKey(key id, integer link);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `key` | `object_id` |  |
| `integer (link)` | `link` | Link number (0: unlinked, 1: root prim, >1: child prims and seated avatars) or a LINK_* flag |


## Return Value

Returns `key`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetObjectLinkKey)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetObjectLinkKey) — scraped 2026-03-18_

Returns the key of the linked prim link

## Examples

Drag this script on to linked and unlinked prims, with avatars sitting or not, to see how llGetLinkKey relates to llGetKey, llGetLinkNumber, llGetNumberOfPrims, LINK_ROOT, etc.

```lsl
// Return the name of a link num else the empty string.
string getLinkNumName(integer link)
{
    if (LINK_THIS == link) return "LINK_THIS";
    if (LINK_ALL_CHILDREN == link) return "LINK_ALL_CHILDREN";
    if (LINK_ALL_OTHERS == link) return "LINK_ALL_OTHERS";
    if (LINK_SET == link) return "LINK_SET";
    if (LINK_ROOT == link) return "LINK_ROOT";
    return "";
}

// Say the key of each linked prim.
default
{
    state_entry()
    {
        integer theLink = llGetLinkNumber();

        key theLinkKey = llGetKey();
        key owner = llGetOwner();
        key creator = llGetCreator();

        // Visit each link num.

        integer link;
        integer primmed = llGetNumberOfPrims();
        for (link = -5; link <= (primmed + 5); ++link)
        {
            key linkKey = llGetLinkKey(link);

            // Detail the key at the link num.

            string line = (string) linkKey; // large constant width

            if (linkKey == owner) line += " llGetOwner";
            if (linkKey == creator) line += " llGetCreator";
            if (linkKey == theLinkKey) line += " llGetKey";

            // Detail the link num.

            line += " @ " + (string) link;
            line += " " + getLinkNumName(link);
            if (link == theLink) line += " llGetLinkNumber";
            if (link == primmed) line += " llGetNumberOfPrims";

            // Say the detail if fun.

            if (linkKey != NULL_KEY)
            {
                llOwnerSay(line);
            }
        }

        // Always count the linked prims.

        llOwnerSay((string) primmed + " llGetNumberOfPrims");
        llOwnerSay("OK");
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
- llGetKey
- llGetLinkName

<!-- /wiki-source -->
