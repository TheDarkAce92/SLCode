---
name: "llDeleteSubString"
category: "function"
type: "function"
language: "LSL"
description: 'Returns a string that is the result of removing characters from src from start to end.

start & end support negative indexes.
Characters at positions start and end are removed.'
signature: "string llDeleteSubString(string src, integer start, integer end)"
return_type: "string"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llDeleteSubString'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["lldeletesubstring"]
---

Returns a string that is the result of removing characters from src from start to end.

start & end support negative indexes.
Characters at positions start and end are removed.


## Signature

```lsl
string llDeleteSubString(string src, integer start, integer end);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `string` | `src` |  |
| `integer` | `start` | start index |
| `integer` | `end` | end index |


## Return Value

Returns `string`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llDeleteSubString)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llDeleteSubString) — scraped 2026-03-18_

Returns a string that is the result of removing characters from src from start to end.

## Caveats

- If either start or end are out of bounds  the script continues to execute without an error message.
- start & end will form an exclusion range when start is past end (Approximately: start > end).

## Examples

```lsl
default
{
    state_entry()
    {
        string ex = "abcdefghi";
        llDeleteSubString(ex, 4, 7); //Incorrect!
    }
}
```

```lsl
default
{
    state_entry()
    {
        string ex = "abcdefghi";
        ex = llDeleteSubString(ex, 4, 7); //Correct
        llSay(0, ex); //Would say "abcdi"
    }
}
```

```lsl
//-- special case
default
{
    state_entry()
    {
        string ex = "abcdefghi";
        llSay( 0, llDeleteSubString(ex, 4, 7) ); //Would say "abcdi"
        //-- acceptable if you do NOT want to change the contents of 'ex', only the output
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
Indexes start at zero, the index of the first character is zero. Using 0,0 as start and end positions would delete the first character only. Negative indexes count from the far end of the string towards the beginning, so -1 is short form for the last character in a string. Positive and negative indexes can be mixed so using 0, -1 as start and end positions would delete the entire string.

To ascertain how long a string is, use llStringLength.

Granted, wondering how to use this can be bewildering at times: with random text strings being handled by your script, you may wonder how you can know what positions you should be starting and ending the deletion at. llSubStringIndex is the preferred method of finding a string in a string but it can be a rather involved process. If the user just wants to remove all occurrences of a string from a string they may wish to consider simply using Strife Onizuka's str_replace function instead, to looks for a value without having to know where it starts and ends, and replacing it with "".

## See Also

### Functions

- llGetSubString
- llReplaceSubString
- llInsertString
- llDeleteSubList

### Articles

- Negative Index
- CombinedLibrary: str_replace

<!-- /wiki-source -->
