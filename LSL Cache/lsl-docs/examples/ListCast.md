---
name: "ListCast"
category: "example"
type: "example"
language: "LSL"
description: "Iterates through the contents of a list, producing a resulting list whose contents are cast to a single type. Please refer to llGetListEntryType() for valid types. This function is useful for converting a list to a type which is more memory efficient, or to a type that you know you are going to access a lot (in order to remove extra casting later-on).Returns a list whose contents are all one type."
wiki_url: "https://wiki.secondlife.com/wiki/ListCast"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

/LSL


ListCastlistCast

- 1 Summary
- 2 Examples
- 3 Implementation

## Summary

 Function: list **listCast**( list mixedList, integer type );

Iterates through the contents of a list, producing a resulting list whose contents are cast to a single type. Please refer to llGetListEntryType() for valid types. This function is useful for converting a list to a type which is more memory efficient, or to a type that you know you are going to access a lot (in order to remove extra casting later-on).Returns a list whose contents are all one type.

• list

mixedList

–

The list to cast, its contents may be anything.

• integer

type

–

The type of variable to cast all entries to.

## Examples

```lsl
        list mixed = [1, 2.0, "3", "Four", (key)"8aef4875-6873-0919-f5ab-c9d6b48d18d4"];

        // Prints: 1, 2, 3, 0, 8
        llOwnerSay(llList2CSV(listCast(mixed, TYPE_INTEGER)));
        // Prints: 1.000000, 2.000000, 3.000000, 0.000000, 0.000000
        llOwnerSay(llList2CSV(listCast(mixed, TYPE_FLOAT)));
```


Implementation

```lsl
list listCast(list mixedList, integer type) {
    list result = []; integer x = mixedList != [];

    if (type == TYPE_INTEGER)
        while (x)
            result = [(integer)llList2String(mixedList, --x)] + result;
    else if (type == TYPE_FLOAT)
        while (x) {
            if (llGetListEntryType(mixedList, --x) == TYPE_FLOAT) result = [llList2Float(mixedList, x)] + result;
            else result = [(float)llList2String(mixedList, x)] + result;
        }
    else if (type == TYPE_VECTOR)
        while (x) {
            if (llGetListEntryType(mixedList, --x) == TYPE_VECTOR) result = [llList2Vector(mixedList, x)] + result;
            else result = [(vector)llList2String(mixedList, x)] + result;
        }
    else if (type == TYPE_ROTATION)
        while (x) {
            if (llGetListEntryType(mixedList, --x) == TYPE_ROTATION) result = [llList2Rot(mixedList, x)] + result;
            else result = [(rotation)llList2String(mixedList, x)] + result;
        }
    else if (type == TYPE_STRING)
        while (x)
            result = [llList2String(mixedList, --x)] + result;
    else if (type == TYPE_KEY)
        while (x)
            result = [llList2Key(mixedList, --x)] + result;
    else result = mixedList;

    return result;
}
```