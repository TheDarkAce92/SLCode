---
name: "llGetSubString"
category: "function"
type: "function"
language: "LSL"
description: "Returns a substring from start to end index (inclusive), supporting negative indexing"
wiki_url: "https://wiki.secondlife.com/wiki/llGetSubString"
first_fetched: "2026-03-09"
last_updated: "2026-03-09"
signature: "string llGetSubString(string src, integer start, integer end)"
parameters:
  - name: "src"
    type: "string"
    description: "Source string"
  - name: "start"
    type: "integer"
    description: "Start index (0 = first char; negative counts from end, -1 = last)"
  - name: "end"
    type: "integer"
    description: "End index (inclusive; negative counts from end)"
return_type: "string"
energy_cost: "10.0"
sleep_time: "0.0"
patterns: ["llgetsubstring"]
deprecated: "false"
---

# llGetSubString

```lsl
string llGetSubString(string src, integer start, integer end)
```

Returns the substring of `src` from `start` to `end` (inclusive). Original string is not modified.

## Index Reference

| Position | Positive | Negative |
|----------|----------|----------|
| First | 0 | -length |
| Last | length - 1 | -1 |

## When start > end (Exclusion Range)

Returns the complement: characters from `[0, end]` plus `[start, -1]`.

## Examples

```lsl
string word = "Hello!";
llOwnerSay(llGetSubString(word, 0, 0));    // "H"   (first char)
llOwnerSay(llGetSubString(word, -1, -1));  // "!"   (last char)
llOwnerSay(llGetSubString(word, 0, 4));    // "Hello"
llOwnerSay(llGetSubString(word, 2, 3));    // "ll"

// Exclusion range (start > end): returns everything EXCEPT chars 1-4
llOwnerSay(llGetSubString(word, 1, -2));   // exclusion — "H!"
```

```lsl
// Get first name from "John Doe"
string fullName = "John Doe";
integer spacePos = llSubStringIndex(fullName, " ");
string firstName = llGetSubString(fullName, 0, spacePos - 1);  // "John"
```

## See Also

- `llDeleteSubString` — remove a substring
- `llInsertString` — insert at position
- `llSubStringIndex` — find position of substring
- `llStringLength` — length of string


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetSubString) — scraped 2026-03-18_

Returns a string that is the substring of src from start to end, leaving the original string intact.

## Caveats

- If either start or end are out of bounds  the script continues to execute without an error message.
- start & end will form an exclusion range when start is past end (Approximately: start > end).

## Examples

```lsl
default
{
    state_entry()
    {
        string word = "Hello!";
        llOwnerSay(llGetSubString(word, 0, 0));
        // Object: H
        llOwnerSay(llGetSubString(word, -1, -1));
        // Object: !
        llOwnerSay(llGetSubString(word, 2, 3));
        // Object: ll
    }
}
```

```lsl
// display SL time using a script without an 'if'
default
{
    state_entry()
    {
        // synchronise our clock to a fraction of a second
        float fnow = llGetWallclock();
        while (fnow == llGetWallclock() )   ;   // await a change in seconds

        llSetTimerEvent(1.0);
    }

    timer()
    {
        integer seconds = (integer) llGetWallclock();
        integer minutes = seconds / 60;
        seconds = seconds % 60;
        integer hours = minutes / 60;
        minutes = minutes % 60;

        string stringHours   = llGetSubString("0" + (string)hours,   -2, -1);
        string stringMinutes = llGetSubString("0" + (string)minutes, -2, -1);
        string stringSeconds = llGetSubString("0" + (string)seconds, -2, -1);

        string time = stringHours + ":" + stringMinutes + ":" + stringSeconds;

        llSetText(time, <1.0, 1.0, 1.0>, 1.0);
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
The counting of the characters starts at 0. Using 0,0 as start and end positions would return the first character only. Using negative numbers causes backwards counting, so -1 is shortform for the last character in a string. Ergo, using 0, -1 as start and end positions would return the entire string.

To ascertain how long a string is, use llStringLength.

## See Also

### Functions

- llReplaceSubString
- llDeleteSubString
- llInsertString

### Articles

- Negative Index
- CombinedLibrary: str_replace

<!-- /wiki-source -->
