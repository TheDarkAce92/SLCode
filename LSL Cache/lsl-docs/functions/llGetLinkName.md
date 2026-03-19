---
name: "llGetLinkName"
category: "function"
type: "function"
language: "LSL"
description: "Returns a string that is the name of link in link set"
signature: "string llGetLinkName(integer linknumber)"
return_type: "string"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetLinkName'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgetlinkname"]
---

Returns a string that is the name of link in link set


## Signature

```lsl
string llGetLinkName(integer linknumber);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `integer (link)` | `link` | Link number (0: unlinked, 1: root prim, >1: child prims and seated avatars) or a LINK_* flag  |


## Return Value

Returns `string`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetLinkName)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetLinkName) — scraped 2026-03-18_

Returns a string that is the name of link in link set

## Caveats

- link needs to be either an actual link number or a link constants that equate to a single prim, such as LINK_ROOT and LINK_THIS.

  - LINK_SET, LINK_ALL_CHILDREN and LINK_ALL_OTHERS will not work.
- If **link** is out of bounds, NULL_KEY is returned.
- The prim name attribute is limited to 63 bytes, any string longer then that will be truncated. This truncation does not always happen when the attribute is set or read.
- There is no corresponding **llSetLinkName**, use `llSetLinkPrimitiveParamsFast(link, [PRIM_NAME, name]);` instead.

## Examples

Listen on channel 10 for a name; check if a prim with that name is part of this object

```lsl
integer check_for_prim(string name)
{
    integer i = llGetNumberOfPrims();
    for (; i >= 0; --i)
    {
        if (llGetLinkName(i) == name)
        {
            return TRUE;
        }
    }
    return FALSE;
}
default
{
    state_entry()
    {
        llListen(10, "", llGetOwner(), "");
    }
    listen(integer chan, string obj, key id, string msg)
    {
        if (check_for_prim(msg))
        {
            llOwnerSay("found a linked prim named \"" + msg + "\"");
        }
        else
        {
            llOwnerSay("this object does not have any linked prims named \"" + msg + "\"");
        }
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
- **llGetLinkKey** — Gets the instance UUID of the link
- **llGetObjectName** — Get the prims name
- **llSetObjectName** — Set the prims name
- **llGetObjectDesc** — Get the prims description
- **llSetObjectDesc** — Set the prims description
- llGetObjectDetails

### Articles

- **Limits** — SL limits and constrictions
- Prim Attribute Overloading

<!-- /wiki-source -->
