---
name: "llList2ListStrided"
category: "function"
type: "function"
language: "LSL"
description: "Returns a list of all the entries in the strided list whose index is a multiple of stride in the range start to end."
signature: "list llList2ListStrided(list src, integer start, integer end, integer stride)"
return_type: "list"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llList2ListStrided'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["lllist2liststrided"]
---

Returns a list of all the entries in the strided list whose index is a multiple of stride in the range start to end.


## Signature

```lsl
list llList2ListStrided(list src, integer start, integer end, integer stride);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `list` | `src` |  |
| `integer` | `start` | start index |
| `integer` | `end` | end index |
| `integer` | `stride` | number of entries per stride, if less than 1 it is assumed to be 1 |


## Return Value

Returns `list`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llList2ListStrided)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llList2ListStrided) — scraped 2026-03-18_

Returns a list of all the entries in the strided list whose index is a multiple of stride in the range start to end.

## Caveats

- If either start or end are out of bounds  the script continues to execute without an error message.
- start & end will not form an exclusion range when start is past end (Approximately: start > end), instead it will act as if start was zero & end was -1.

## Examples

```lsl
list mylist = [0,1,2,3,4,5,6];
list result_a = llList2ListStrided(mylist,0,-1,2); //start at first item in list, go to the end, return every 2nd item
//result_a == [0,2,4,6]

list result_b = llList2ListStrided(mylist,1,-1,2); //start at second item in list, go to the end, return every 2nd item
//result_b == [2,4,6]

list result_c = llList2ListStrided(mylist,2,-1,2); //start at third item in list, go to the end, return every 2nd item
//result_c == [2,4,6]
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
        list buttons = llList2ListStrided(menu, 0, -1, 2);
        llDialog(llDetectedKey(0), "choose a number", buttons, 10);
    }
    listen(integer channel, string obj, key id, string message)
    {
        integer index = llListFindList(menu, [message]);
        if (index != -1)
        {
            llOwnerSay("you chose " + llList2String(menu, index + 1) + " (" + message + ")");
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

### Starting at an offset

If you want every second (or third, etc.) item in each stride returned, rather than the first, use llList2ListSlice instead.

## See Also

### Functions

- llList2ListSlice

### Articles

- Negative Index

<!-- /wiki-source -->
