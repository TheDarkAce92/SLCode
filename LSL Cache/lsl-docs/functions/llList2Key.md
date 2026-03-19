---
name: "llList2Key"
category: "function"
type: "function"
language: "LSL"
description: 'Returns a key that is at index in src.

index supports negative indexes.

If index describes a location not in src then null string is returned.
If the type of the element at index in src is not a key it is typecast to a key. If it cannot be typecast null string is returned.'
signature: "key llList2Key(list src, integer index)"
return_type: "key"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llList2Key'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["lllist2key"]
---

Returns a key that is at index in src.

index supports negative indexes.

If index describes a location not in src then null string is returned.
If the type of the element at index in src is not a key it is typecast to a key. If it cannot be typecast null string is returned.


## Signature

```lsl
key llList2Key(list src, integer index);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `list` | `src` | List containing the element of interest. |
| `integer` | `index` | Index of the element of interest. |


## Return Value

Returns `key`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llList2Key)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llList2Key) — scraped 2026-03-18_

Returns a key that is at index in src.

## Caveats

- If index is out of bounds  the script continues to execute without an error message.

## Examples

```lsl
// Best viewed in Chat History (ctrl-h)
default
{
    state_entry()
    {
        list my_list = ["a", 1, 2.0, <1,2,3>, <1,2,3,4>, llGetOwner()];
        integer i;
        for (i=0;i

## See Also

### Functions

- llGetListEntryType
- llList2String

### Articles

- Negative Index

<!-- /wiki-source -->
