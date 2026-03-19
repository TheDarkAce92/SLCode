---
name: "llList2String"
category: "function"
type: "function"
language: "LSL"
description: "Returns the element at the given index of a list, cast to string"
wiki_url: "https://wiki.secondlife.com/wiki/llList2String"
first_fetched: "2026-03-09"
last_updated: "2026-03-09"
signature: "string llList2String(list src, integer index)"
parameters:
  - name: "src"
    type: "list"
    description: "The source list"
  - name: "index"
    type: "integer"
    description: "Zero-based index. Supports negative indexing (-1 = last element)."
return_type: "string"
energy_cost: "10.0"
sleep_time: "0.0"
patterns: ["lllist2string"]
deprecated: "false"
---

# llList2String

```lsl
string llList2String(list src, integer index)
```

Returns the element at `index` in `src`, cast to string. Supports negative indexing.

## Index Reference

| Position | Positive | Negative |
|----------|----------|----------|
| First | 0 | -length |
| Last | length - 1 | -1 |

## Return Value

`string` — the element cast to string. Float values are truncated to 6 decimal places. Out-of-bounds index returns empty string (no error).

## Caveats

- Out-of-bounds index silently returns empty string.
- Float-to-string conversion truncates to 6 decimal places.
- Does not error — always check bounds if needed.

## Example

```lsl
list items = ["apple", "banana", "cherry"];
llOwnerSay(llList2String(items, 0));   // "apple"
llOwnerSay(llList2String(items, -1));  // "cherry"
llOwnerSay(llList2String(items, 1));   // "banana"

// Numeric list elements
list nums = [1, 2.5, <1,2,3>];
llOwnerSay(llList2String(nums, 0));    // "1"
llOwnerSay(llList2String(nums, 1));    // "2.500000"
llOwnerSay(llList2String(nums, 2));    // "<1.000000, 2.000000, 3.000000>"
```

## See Also

- `llList2Integer` — get element as integer
- `llList2Float` — get element as float
- `llList2Key` — get element as key
- `llList2Vector` — get element as vector
- `llList2Rot` — get element as rotation
- `llGetListLength` — count list elements


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llList2String) — scraped 2026-03-18_

Returns a string that is at index in src.

## Caveats

- If index is out of bounds  the script continues to execute without an error message.
- When using this function to typecast a list element to a string it will truncated float based types to 6 decimal places.

## Examples

```lsl
//This code demonstrates the differences in typecasting in LSL (and demonstrates how to use the llList2* functions).
// Best viewed in Chat History (ctrl-h)
default
{
    state_entry()
    {
        list my_list = ["a", "0xFF", "0xFF.FF", "1.0e3", 1, 2.0, <1,2,3>, <1,2,3,4>, llGetOwner()];
        integer i = 0;
        integer end = llGetListLength(my_list);
        for (; i

## Notes

- If you wish to extract a string from a list that you know will contain only a single item (for example if you extract a single entry from a list using llList2List()), then instead of using `llList2String(myList, 0)` you may wish to considering using the more efficient `(string)myList` as it will produce the same result for single-entry lists with less memory usage due to eliminating a function-call.
- To convert a string of hexadecimal notation to integer, call llList2Integer and it will automatically cast the value as decimal integer. To convert that integer back to a string of hexadecimal notation, use a user function like hex.

## See Also

### Functions

- llDumpList2String
- llGetListEntryType
- llList2Float
- llList2Integer
- llList2Key

### Articles

- Negative Index

<!-- /wiki-source -->
