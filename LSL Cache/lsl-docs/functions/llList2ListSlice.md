---
name: "llList2ListSlice"
category: "function"
type: "function"
language: "LSL"
description: 'Returns a list of the slice_index'th element of every stride in strided list whose index is a multiple of stride in the range start to end.

This function supports Strided Lists.
The index of the first entry in the list is 0
The index of the first entry in a slice is 0
If start, end, or slice_index '
signature: "list llList2ListSlice(list src, integer start, integer end, integer stride, integer slice_index)"
return_type: "list"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llList2ListSlice'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
---

Returns a list of the slice_index'th element of every stride in strided list whose index is a multiple of stride in the range start to end.

This function supports Strided Lists.
The index of the first entry in the list is 0
The index of the first entry in a slice is 0
If start, end, or slice_index are negative they are indexed from end of list. -1 is last element in the list. -list_length is the 1st element of the list.
If slice_index is negative it is counted from the end of its stride regardless of whether or not the stride exceeds the end of the list. e.g: -1 is the last element in a stride.
If start > end the range from start to end is treated as an exclusion range.


## Signature

```lsl
list llList2ListSlice(list src, integer start, integer end, integer stride, integer slice_index);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `list` | `src` |  |
| `integer` | `start` | start index |
| `integer` | `end` | end index |
| `integer` | `stride` | number of entries per stride, if less than 1 it is assumed to be 1 |
| `integer` | `slice_index` |  |


## Return Value

Returns `list`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llList2ListSlice)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llList2ListSlice) — scraped 2026-03-18_

Returns a list of the slice_index'th element of every stride in strided list whose index is a multiple of stride in the range start to end.

## Caveats

- If either start or end are out of bounds  the script continues to execute without an error message.
- start & end will form an exclusion range when start is past end (Approximately: start > end).

## Examples

```lsl
list mylist = [0,1,2,3,4,5,6];
list result_a = llList2ListSlice(mylist,0,-1,3,0); //start at first item in list, go to the end, return 1st slice of every stride of 3
//result_a == [0,3,6]

list result_b = llList2ListSlice(mylist,0,-1,3,1); //start at first item in list, go to the end, return 2nd slice of every stride of 3
//result_b == [1,4]

list result_c = llList2ListSlice(mylist,1,-1,3,1); //start at second item in list, go to the end, return 2nd slice of every stride of 3
//result_c == [2,5]

list result_d = llList2ListSlice(mylist,2,-1,3,-1); //start at third item in list, go to the end, return last slice of every stride of 3
//result_d == [4]

list result_e = llList2ListSlice(mylist,4,2,1,0); //4>2 so this is an exclusion. slice indices count from 0 and first element after exclusion. Return every element not in range with a stride of 1
//result_e == [0,1,2,4,5,6]
```

```lsl
list menu = ["1", "one", "2", "two", "3", "three"];
default
{
    state_entry()
    {
        llListen(10, "", llGetOwner(), "");
    }
    touch_start(integer detected)
    {
        list buttons = llList2ListSlice(menu, 0, -1, 2, 0);
        llDialog(llDetectedKey(0), "choose a number", buttons, 10); //display the digits
    }
    listen(integer channel, string obj, key id, string message)
    {
        integer index = llListFindList(menu, [message]);
        if (index != -1)
        {
            list names = llList2ListSlice(menu, 0, -1, 2, 1);
            llOwnerSay("you chose " + llList2String(names, index/2) + " (" + message + ")");
        }
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
If the list is not modulo the stride, elements up to the length of the list will be returned in the final slice matching conditions.  e.g.  a list of 5 elements with a stride of 2 will return 3 elements for a 0,5 range on slice index 0 but only 2 if the slice_index is 1.

## See Also

### Articles

- Negative Index

<!-- /wiki-source -->
