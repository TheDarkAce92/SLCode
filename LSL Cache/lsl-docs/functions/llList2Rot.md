---
name: "llList2Rot"
category: "function"
type: "function"
language: "LSL"
description: 'Returns a rotation that is at index in src.

index supports negative indexes.

If index describes a location not in src then ZERO_ROTATION is returned.
If the type of the element at index in src is not a rotation then ZERO_ROTATION is returned.
Here is a workaround: (rotation)llList2String(src, inde'
signature: "rotation llList2Rot(list src, integer index)"
return_type: "rotation"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llList2Rot'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["lllist2rot"]
---

Returns a rotation that is at index in src.

index supports negative indexes.

If index describes a location not in src then ZERO_ROTATION is returned.
If the type of the element at index in src is not a rotation then ZERO_ROTATION is returned.
Here is a workaround: (rotation)llList2String(src, index);


## Signature

```lsl
rotation llList2Rot(list src, integer index);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `list` | `src` | List containing the element of interest. |
| `integer` | `index` | Index of the element of interest. |


## Return Value

Returns `rotation`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llList2Rot)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llList2Rot) — scraped 2026-03-18_

Returns a rotation that is at index in src.

## Caveats

- If index is out of bounds  the script continues to execute without an error message.
- When used to typecast from a string it will result in a ZERO_ROTATION

  - A true typecast will solve this: (rotation)llList2String(src, index);

  - Unfortunately, if it was already a rotation type, using llList2String will cause the decimal values to be truncated to six decimal places.

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
- llList2String

### Articles

- Negative Index

<!-- /wiki-source -->
