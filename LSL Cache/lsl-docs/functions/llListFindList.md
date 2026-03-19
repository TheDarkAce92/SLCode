---
name: "llListFindList"
category: "function"
type: "function"
language: "LSL"
description: "Searches for the first occurrence of a test list (needle) in a source list (haystack); returns index or -1"
wiki_url: "https://wiki.secondlife.com/wiki/llListFindList"
first_fetched: "2026-03-09"
last_updated: "2026-03-09"
signature: "integer llListFindList(list src, list test)"
parameters:
  - name: "src"
    type: "list"
    description: "The list to search in (haystack)"
  - name: "test"
    type: "list"
    description: "The pattern to search for (needle)"
return_type: "integer"
energy_cost: "0.0"
sleep_time: "0.0"
patterns: ["lllistfindlist"]
deprecated: "false"
---

# llListFindList

```lsl
integer llListFindList(list src, list test)
```

Searches for `test` as a contiguous sublist within `src`. Returns the zero-based starting index of the first match, or -1 if not found.

## Return Value

`integer` — starting index of first match, or -1 if not found. Returns 0 for empty `test`.

## Caveats

- **Type-strict and case-sensitive:** `"1"` ≠ `1` (string vs integer), `"a"` ≠ `"A"`.
- **Type matching examples:**
  - Integer `1` ≠ Float `1.0`
  - String `"key-uuid"` ≠ key `(key)"key-uuid"` — cast explicitly
- Searching for an empty list returns 0, not -1.

## Examples

```lsl
list numbers = [1, 2, 3, 4, 5];

integer idx = llListFindList(numbers, [3]);
// idx = 2

if (idx != -1)
{
    list pair = llList2List(numbers, idx, idx + 1);
    llOwnerSay(llDumpList2String(pair, ","));  // "3,4"
}
```

```lsl
// Compact existence check using bitwise NOT
// ~(-1) == 0 (false), ~(any other value) != 0 (true)
list allowed = ["Alice", "Bob", "Carol"];
if (~llListFindList(allowed, ["Alice"]))
    llOwnerSay("Alice is allowed");
```

```lsl
// Remove an item from a list
string target = "Bob";
integer idx = llListFindList(myList, [target]);
if (idx != -1)
    myList = llDeleteSubList(myList, idx, idx);
```

## See Also

- `llDeleteSubList` — remove elements by index range
- `llList2List` — extract a sublist
- `llListReplaceList` — replace elements at index


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llListFindList) — scraped 2026-03-18_

Returns the integer index of the first instance of test in src.

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

## See Also

### Functions

- **llSubStringIndex** — Find a string in another string

<!-- /wiki-source -->
