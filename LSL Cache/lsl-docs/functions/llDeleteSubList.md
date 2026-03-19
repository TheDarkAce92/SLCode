---
name: "llDeleteSubList"
category: "function"
type: "function"
language: "LSL"
description: 'Returns a list that is a copy of src but with the slice from start to end removed.

start & end support negative indexes.
While the function result is different than src, src is not modified, remember to use or store the result of this function.
The opposite function would be llListInsertList.'
signature: "list llDeleteSubList(list src, integer start, integer end)"
return_type: "list"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llDeleteSubList'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["lldeletesublist"]
---

Returns a list that is a copy of src but with the slice from start to end removed.

start & end support negative indexes.
While the function result is different than src, src is not modified, remember to use or store the result of this function.
The opposite function would be llListInsertList.


## Signature

```lsl
list llDeleteSubList(list src, integer start, integer end);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `list` | `src` | source |
| `integer` | `start` | start index |
| `integer` | `end` | end index |


## Return Value

Returns `list`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llDeleteSubList)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llDeleteSubList) — scraped 2026-03-18_

Returns a list that is a copy of src but with the slice from start to end removed.

## Caveats

- If either start or end are out of bounds  the script continues to execute without an error message.
- start & end will form an exclusion range when start is past end (Approximately: start > end).

## Examples

```lsl
src = llDeleteSubList( src, start, end )
```

```lsl
default
{
    state_entry()
    {
        // Create a list of names
        list names = ["Anthony", "Bob", "Charlie", "Diane", "Edgar", "Gabriela"];

        // Now let's remove values at position 1 through 2.
        names = llDeleteSubList(names, 1, 2);

        // Result:
        // list names = ["Anthony", "Diane", "Edgar", "Gabriela"];

        // Now let's use an start number higher then our end number
        names = llDeleteSubList(names, 3, 1);

        // Result:
        // list names = ["Edgar"];
        // If start number higher then our end number, then we should imagine that the start and the end are missing before start and end.
        // Imagine it should be FROM_THE_LISTSTART_CUT: start, AND_FROM_THE_LISTEND_CUT: end ... more or less :))
        // names = llDeleteSubList(names, 3 -> , <- 1);

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

- llListInsertList
- llListReplaceList
- llList2List

### Articles

- Negative Index

<!-- /wiki-source -->
