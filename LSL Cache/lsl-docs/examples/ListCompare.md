---
name: "ListCompare"
category: "example"
type: "example"
language: "LSL"
description: "Efficiently compares two lists for equality (same contents in the same order).Returns an integer TRUE if the lists are equal, FALSE if not."
wiki_url: "https://wiki.secondlife.com/wiki/ListCompare"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

/LSL


ListCompareListCompare

- 1 Summary
- 2 Examples
- 3 Implementation for LSO or MONO

## Summary

 Function: integer **ListCompare**( list a, list b );

Efficiently compares two lists for equality (same contents in the same order).Returns an integer TRUE if the lists are equal, FALSE if not.

• list

a

–

The first list to compare.

• list

b

–

The second list to compare.

## Examples

```lsl
integer r = ListCompare([1, 2.0, "3"], [1, 2.0, "3"]); // Returns TRUE
integer s = ListCompare([1, 2.0, 3], [1, 2.0, "3"]);   // Returns FALSE
integer t = ListCompare([], [1, 2.0, "3"]);            // Returns FALSE
```


Implementation for LSO or MONO

```lsl
integer ListCompare(list a, list b)
{
    if (a != b)        return FALSE;    // Note: This is comparing list lengths only

    // The next line is only needed if compiling with LSO
    if (a == [])       return TRUE;     // both lists are empty (as both lists are the same length)

    return !llListFindList(a, b);
    // As both lists are the same length, llListFindList() can only return 0 or -1
    // Which we return as TRUE or FALSE respectively
}
```