---
name: "llListFindList"
category: "example"
type: "example"
language: "LSL"
description: "Returns the integer index of the first instance of test in src."
wiki_url: "https://wiki.secondlife.com/wiki/LlListFindList"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

/LSL


ListFindListllListFindList

- 1 Summary
- 2 Caveats
- 3 Examples
- 4 Useful Snippets
- 5 See Also

  - 5.1 Functions
- 6 Deep Notes

  - 6.1 Signature
  - 6.2 Haiku

## Summary

 Function: integer **llListFindList**( list src, list test );

0.0

Forced Delay

10.0

Energy

Returns the integer index of the first instance of test in src.

• list

src

–

what to search in (haystack)

• list

test

–

what to search for (needle)

If test is not found in src, -1 (in LSL) or nil (in SLua) is returned.

The index of the first entry in the list is 0

If test is found at the last index in src the positive index is returned (5th entry of 5 returns 4).

## Caveats

- Strict type matching and case sensitivity is enforced.

  - "1" != 1
  - "1.0" != 1.0
  - 1 != 1.0
  - "a822ff2b-ff02-461d-b45d-dcd10a2de0c2" != (key)"a822ff2b-ff02-461d-b45d-dcd10a2de0c2"
  - "Justice" != "justice"
- If test is an empty list the value returned is 0 rather than -1.

## Examples

```lsl
list numbers = [1, 2, 3, 4, 5];
default
{
    state_entry()
    {
        integer index = llListFindList(numbers, [3]);
        if (index != -1)
        {
            list three_four = llList2List(numbers, index, index + 1);
            llOwnerSay(llDumpList2String(three_four, ","));
            // Object: 3,4
        }
    }
}
```

```lsl
//You can also search for two items at once to find a pattern in a list
list avatarsWhoFoundMagicLeaves = ["Fire Centaur","Red Leaf"];
default
{
    state_entry()
    {
        integer index = llListFindList(avatarsWhoFoundMagicLeaves, ["Fire Centaur","Red Leaf"]);
        if (index != -1)
        {
            list output = llList2List(avatarsWhoFoundMagicLeaves, index, index + 1);
            llOwnerSay(llDumpList2String(output, ","));
            // Object: Fire Centaur, Red Leaf
        }
    }
}
```

## Useful Snippets

An easy way to see if an item exists in a list...

```lsl
if(~llListFindList(myList, (list)item))
{//it exists
    // This works because ~(-1) produces 0, but ~ of any other value produces non-zero and causes the 'if' to succeed
    // So any return value (including 0) that corresponds to a found item, will make the condition succeed
    // It saves bytecode and is faster then doing != -1
    // This is a bitwise NOT (~) not a negation (-)
}
```

## See Also

### Functions

•

llSubStringIndex

–

Find a string in another string

## Deep Notes

#### Signature

```lsl
function integer llListFindList( list src, list test );
```

#### Haiku

Where are my car keys?


Has anyone seen my keys?


Oh! In my pocket.