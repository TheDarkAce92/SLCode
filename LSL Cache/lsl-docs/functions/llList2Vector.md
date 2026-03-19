---
name: "llList2Vector"
category: "function"
type: "function"
language: "LSL"
description: "Returns a vector that is at index in src."
signature: "vector llList2Vector(list src, integer index)"
return_type: "vector"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llList2Vector'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["lllist2vector"]
---

Returns a vector that is at index in src.


## Signature

```lsl
vector llList2Vector(list src, integer index);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `list` | `src` | List containing the element of interest. |
| `integer` | `index` | Index of the element of interest. |


## Return Value

Returns `vector`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llList2Vector)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llList2Vector) — scraped 2026-03-18_

Returns a vector that is at index in src.

## Caveats

- If index is out of bounds  the script continues to execute without an error message.
- When used to typecast from a string it will result in a ZERO_VECTOR

  - A true typecast will solve this: (vector)llList2String(src, index);

  - Unfortunately, if it was already a vector type, using llList2String will cause the decimal values to be truncated to six decimal places.
  - In any string representation of a vector such as llList2String(src, index), or (string) llList2Vector (src, index), spaces are automatically added after the commas. When received by a listen, make sure NOT to parse by spaces.

## Examples

```lsl
// Best viewed in Chat History (ctrl-h)
default
{
    state_entry()
    {
        list my_list = ["a", 1, 2.0, <1,2,3>, <1,2,3,4>, llGetOwner()];
        integer i = ~llGetListLength(my_list);
        while(++i)
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
- llList2String

### Articles

- Negative Index

<!-- /wiki-source -->
