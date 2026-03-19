---
name: "llList2List"
category: "function"
type: "function"
language: "LSL"
description: 'Returns a list that is a slice of src from start to end.

start & end support negative indexes.'
signature: "list llList2List(list src, integer start, integer end)"
return_type: "list"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llList2List'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["lllist2list"]
---

Returns a list that is a slice of src from start to end.

start & end support negative indexes.


## Signature

```lsl
list llList2List(list src, integer start, integer end);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `list` | `src` |  |
| `integer` | `start` | start index |
| `integer` | `end` | end index |


## Return Value

Returns `list`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llList2List)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llList2List) — scraped 2026-03-18_

Returns a list that is a slice of src from start to end.

## Caveats

- If either start or end are out of bounds  the script continues to execute without an error message.
- start & end will form an exclusion range when start is past end (Approximately: start > end).

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
default
{
    state_entry()
    {
        //as shown below, there is no way to achieve a "wraparound" order of list elements [8,9,0,1]

        list NUMBERS = [0,1,2,3,4,5,6,7,8,9];
        list L2L;
        L2L = llList2List(NUMBERS, 8, 1); // [0,1,8,9]
        L2L = llList2List(NUMBERS, 8,-9); // [0,1,8,9]
        L2L = llList2List(NUMBERS,-2,-9); // [0,1,8,9]
        L2L = llList2List(NUMBERS,-2, 1); // [0,1,8,9]
    }
}
```

## Notes

### Ranges & Indexes

The easiest way to explain how ranges work is to make all indexes positive. Negative indexes are just a way of counting from the tail end instead of the beginning, all negative indexes have a corresponding equivalent positive index (assuming they are in range). Positive indexes past length (after the last index), or negative indexes past the beginning (before the first index) are valid and the effects are predictable and reliable: the entries are treated as if they were there but were removed just before output.

- If start <= end then the range operated on starts at start and ends at end. [start, end]
- Exclusion range: If start > end then the range operated on starts at 0 and goes to end and then starts again at start and goes to -1. [0, end] + [start, -1]

  - If end is a negative index past the beginning, then the operating range would be [start, -1].
  - If end is a positive index past the end, then the operating range would be [0, end].
  - If both start and end are out of bounds then the function would have no operating range (effectively inverting what the function is supposed to do).

See negative indexes for more information.

## See Also

### Functions

- **llList2ListStrided** — Similar function for strided lists.
- llDeleteSubList
- llListInsertList
- llListReplaceList

### Articles

- Negative Index

<!-- /wiki-source -->
