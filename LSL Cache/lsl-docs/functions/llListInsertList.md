---
name: "llListInsertList"
category: "function"
type: "function"
language: "LSL"
description: "Returns a list that contains all the elements from dest but with the elements from src inserted at position start."
signature: "list llListInsertList(list dest, list src, integer start)"
return_type: "list"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llListInsertList'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["lllistinsertlist"]
---

Returns a list that contains all the elements from dest but with the elements from src inserted at position start.


## Signature

```lsl
list llListInsertList(list dest, list src, integer start);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `list` | `dest` |  |
| `list` | `src` |  |
| `integer` | `start` |  |


## Return Value

Returns `list`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llListInsertList)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llListInsertList) — scraped 2026-03-18_

Returns a list that contains all the elements from dest but with the elements from src inserted at position start.

## Caveats

- If start is out of bounds  the script continues to execute without an error message.

## Examples

```lsl
list numbers = [3, "three", 2, "two", 1, "one"];
default
{
    state_entry()
    {
        llOwnerSay(llDumpList2String(numbers, ","));
        // Object: 3,three,2,two,1,one
        integer index = llListFindList(numbers, [2]);
        if (index != -1)
        {
            numbers = llListInsertList(numbers, [2.5, "two and a half"], index);
            llOwnerSay(llDumpList2String(numbers, ","));
            // Object: 3,three,2.500000,two and a half,2,two,1,one
        }
    }
}
```

## Notes

Bear in mind that the source list will remain unchanged. Instead, a new list will be produced. So, it's important that you capture this with a variable (unless you are acting directly on the results.)



Tip! To insert something at the start of a list, you can just add the two lists (putting the list with the new item(s) first)

```lsl
list oldList = ["B", "C", "D"];
list newItem = ["A"];
list newlist = newItem + oldList;
```

## See Also

### Functions

| • llDeleteSubList |  |  |  |  |
| --- | --- | --- | --- | --- |
| • llList2List |  |  |  |  |
| • llListReplaceList |  |  |  |  |

### Articles

- Negative Index

<!-- /wiki-source -->
