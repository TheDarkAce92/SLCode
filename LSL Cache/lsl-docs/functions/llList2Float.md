---
name: "llList2Float"
category: "function"
type: "function"
language: "LSL"
description: 'Returns a float that is at index in src.

index supports negative indexes.

If index describes a location not in src then zero is returned.
If the type of the element at index in src is not a float it is typecast to a float. If it cannot be typecast zero is returned.'
signature: "float llList2Float(list src, integer index)"
return_type: "float"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llList2Float'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["lllist2float"]
---

Returns a float that is at index in src.

index supports negative indexes.

If index describes a location not in src then zero is returned.
If the type of the element at index in src is not a float it is typecast to a float. If it cannot be typecast zero is returned.


## Signature

```lsl
float llList2Float(list src, integer index);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `list` | `src` | List containing the element of interest. |
| `integer` | `index` | Index of the element of interest. |


## Return Value

Returns `float`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llList2Float)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llList2Float) — scraped 2026-03-18_

Returns a float that is at index in src.

## Caveats

- If index is out of bounds  the script continues to execute without an error message.
- A string of hexadecimal notation (e.g. "0x12A") or scientific notation (e.g. "6.2e+1") will be parsed as float and contain the correct value.

## Examples

```lsl
// Best viewed in Chat History (ctrl-h)
default
{
    state_entry()
    {
        list my_list = ["a", 1, 2.0, <1,2,3>, <1,2,3,4>, llGetOwner()];
        integer i = ~llGetListLength(my_list);
        while (++i)
        {
            llOwnerSay("string=" + llList2String(my_list,i)
                        + "\n   integer=" + (string)llList2Integer(my_list,i)
                        + "\n   float=" + (string)llList2Float(my_list,i)
                        + "\n   vector=" + (string)llList2Vector(my_list,i)
                        + "\n   rot=" + (string)llList2Rot(my_list,i)
                        + "\n   key=" + (string)llList2Key(my_list,i) );
        }
    }
}
```

## See Also

### Functions

- llGetListEntryType
- llList2Integer
- llList2String

### Articles

- Negative Index

<!-- /wiki-source -->
