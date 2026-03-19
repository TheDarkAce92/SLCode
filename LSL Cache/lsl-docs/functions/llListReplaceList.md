---
name: "llListReplaceList"
category: "function"
type: "function"
language: "LSL"
description: "Returns a list that is a copy of dest with start through end removed and src inserted at start."
signature: "list llListReplaceList(list dest, list src, integer start, integer end)"
return_type: "list"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llListReplaceList'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["lllistreplacelist"]
---

Returns a list that is a copy of dest with start through end removed and src inserted at start.


## Signature

```lsl
list llListReplaceList(list dest, list src, integer start, integer end);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `list` | `dest` | destination |
| `list` | `src` | source |
| `integer` | `start` | start index |
| `integer` | `end` | end index |


## Return Value

Returns `list`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llListReplaceList)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llListReplaceList) — scraped 2026-03-18_

Returns a list that is a copy of dest with start through end removed and src inserted at start.

## Caveats

- If either start or end are out of bounds  the script continues to execute without an error message.
- start & end will form an exclusion range when start is past end (Approximately: start > end).
- If start is past the end of dest, then src is appended to dest, it will not add null entries.  To avoid this, create empty elements in the list first. A similar outcome occurs when using negative indexes.
- Just calling the function will not update the variable. You must store it (unless of course you are planning to act on the results straightway.)

| • Bad: | `llListReplaceList(MyList, ["New Item"], 2, 2)` |  |  |  |
| --- | --- | --- | --- | --- |
| • Good: | `MyList = llListReplaceList(MyList, ["New Item"], 2, 2)` |  |  |  |

- In LSO ONLY (not Mono): if you are storing to the same list, it can be more memory effective to clear the list before you store.

| • Good: | `MyList = llListReplaceList(MyList, ["New Item"], 2, 2)` |  |  |  |
| --- | --- | --- | --- | --- |
| • Better: | `MyList = llListReplaceList((MyList = []) + MyList, ["New Item"], 2, 2)` |  |  |  |

## Examples

```lsl
default
{
    state_entry()
    {
        list MyOldList = ["a", "b", "e", "d"];
        list MyNewList = llListReplaceList(MyOldList, ["c"], 2, 2);//replace the range starting and ending at
                                                   //index 2 with ["c"] and store it into MyNewList

        llOwnerSay("\""+llList2CSV(MyOldList) + "\"  ->  \"" + llList2CSV(MyNewList)+"\"");//display the change
        //Will say: "a, b, e, d"  ->  "a, b, c, d"
    }
}
```

```lsl
// More commonly, you will be updating an existing list, replacing 1 or more items
// Here we replace entries 2 and 3 and over-write our original list
default
{
    state_entry()
    {
        list MyList = ["a", "b", "x", "y"];
        MyList = llListReplaceList(MyList, ["c", "d"], 2, 3);   // Over-write MyList, with the modified list (having replaced entries 2 & 3)


        llOwnerSay("\"" + llList2CSV(MyList) + "\"");     // display the modified list
        // Will say: "a, b, c, d"
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
To be clear, the list you are replacing in doesn't have to actually be a list of many elements. It can be a single item that you make into a single element list just by placing square brackets around it.

```lsl
list TargetList = ["a", "b", "c", "z", "e"];
list InsertList = ["d"];
```

To act on a single element in a list, just quote its place in the list as both start and end. For instance, 0, 0 would act only on the first element in the list; 7,7 would act only on the 8th element.

For a function that will operate as llListReplaceList does, but work on strided lists, see ListStridedUpdate.

## See Also

### Functions

| • llDeleteSubList |  |  |  |  |
| --- | --- | --- | --- | --- |
| • llListInsertList |  |  |  |  |
| • llList2List |  |  |  |  |

### Articles

- Negative Index

<!-- /wiki-source -->
