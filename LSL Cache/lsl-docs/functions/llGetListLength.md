---
name: "llGetListLength"
category: "function"
type: "function"
language: "LSL"
description: "Returns the number of elements in a list"
wiki_url: "https://wiki.secondlife.com/wiki/llGetListLength"
first_fetched: "2026-03-09"
last_updated: "2026-03-09"
signature: "integer llGetListLength(list src)"
parameters:
  - name: "src"
    type: "list"
    description: "The list to measure"
return_type: "integer"
energy_cost: "10.0"
sleep_time: "0.0"
patterns: ["llgetlistlength"]
deprecated: "false"
---

# llGetListLength

```lsl
integer llGetListLength(list src)
```

Returns the number of elements in `src`.

## Return Value

`integer` — element count. Empty list returns 0.

## Performance Tip

Cache the result before iterating — calling `llGetListLength` in a loop condition recalculates it every iteration:

```lsl
// SLOW: length recalculated every iteration
integer i = 0;
while (i < llGetListLength(myList))
    ++i;

// FAST: cache before loop
integer len = llGetListLength(myList);
integer i = 0;
while (i < len)
    ++i;
```

## LSO Optimisation

In LSO-compiled scripts, `(myList != [])` compares lengths and is slightly more bytecode-efficient than `llGetListLength(myList) > 0` for empty checks. In Mono, the difference is negligible.

## Example

```lsl
list names = ["Alice", "Bob", "Carol"];
integer count = llGetListLength(names);  // 3
llOwnerSay("There are " + (string)count + " names");
```

## See Also

- `llList2String` / `llList2Integer` — access list elements
- `llDeleteSubList` — remove elements
- `llListInsertList` — add elements
- `llListFindList` — search for a sublist


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetListLength) — scraped 2026-03-18_

Returns an integer that is the number of elements in the list src.

## Examples

```lsl
//Basic usage
default
{
    state_entry()
    {
        list testList = ["one", "two", "three"];
        integer length = llGetListLength(testList);
        llOwnerSay("There are " + (string)length + " entries in the list.");
    }
}
```

## Notes

### Best Practices

When using list length to help you loop through a list, it is better to determine the length first, then start your loop:

```lsl
integer length = llGetListLength(mylist);

integer index;// default is 0
while (index < length)
{
    llSay(0, llList2String(mylist, index));
    ++index;
}
```

The following example is to illustrate what not to do, it calculates the length in the "for" loop and is inefficient because the length gets recalculated at each pass through the loop. This should only ever be done if the list is in fact changing (in length) with each iteration of the loop.

```lsl
integer index;// default is 0
while (index < llGetListLength(mylist))
{
    llSay(0, llList2String(mylist, index));
    ++index;
}
```

|  | Important: Please read this intro of how to iterate over a list in LSL. |
| --- | --- |

### LSO Optimizations

A faster and lighter (in bytecode) way to determine the length of a list is to do a not-equals compare with a null list. This works because the list not-equals compare returns the difference between the lengths, meaning that it returns the same result as `llGetListLength()`, minus the overhead in bytecode, and performance penalty of calling a non-native function. Note: This optimization is much less beneficial time-wise in Mono as Mono's llGetListLength function is almost twice as fast, however the bytecode saving is still about 30 bytes.

```lsl
list in;
integer len_in = llGetListLength(in);
integer flen_in = (in != []);
//flen_in and len_in will be the same

integer neg_len_in = -llGetListLength(in);
integer fneg_len_in = ([] != in);
//fneg_len_in and neg_len_in will be the same
```

## See Also

### Functions

- **llListStatistics** — LIST_STAT_NUM_COUNT
- **llStringLength** — Returns the number of characters in a string.

<!-- /wiki-source -->
