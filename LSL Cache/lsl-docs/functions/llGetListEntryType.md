---
name: "llGetListEntryType"
category: "function"
type: "function"
language: "LSL"
description: 'Returns the type (an integer) of the entry at index in src.

index supports negative indexes.

If index describes a location not in src then TYPE_INVALID is returned.'
signature: "integer llGetListEntryType(list src, integer index)"
return_type: "integer"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetListEntryType'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgetlistentrytype"]
---

Returns the type (an integer) of the entry at index in src.

index supports negative indexes.

If index describes a location not in src then TYPE_INVALID is returned.


## Signature

```lsl
integer llGetListEntryType(list src, integer index);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `list` | `src` | List containing the element of interest. |
| `integer` | `index` | Index of the element of interest. |


## Return Value

Returns `integer`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetListEntryType)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetListEntryType) — scraped 2026-03-18_

Returns the type (an integer) of the entry at index in src.

## Caveats

- If index is out of bounds  the script continues to execute without an error message.
- If a vector is stored in a list as "<7,5,0>" (as a string type, as opposed to <7,5,0> which is a vector type), its type will be returned as TYPE_STRING, not TYPE_VECTOR. The same applies for "1" being returned as a string instead of an integer, etc. There is no easy way to guess what the type should be from a string value.

## Examples

```lsl
string get_list_entry_type_info(integer inputInteger)
{
    if (inputInteger == TYPE_INTEGER)
        return "integer";

    else if (inputInteger == TYPE_FLOAT)
        return "float";

    else if (inputInteger == TYPE_STRING)
        return "string";

    else if (inputInteger == TYPE_KEY)
        return "key";

    else if (inputInteger == TYPE_VECTOR)
        return "vector";

    else if (inputInteger == TYPE_ROTATION)
        return "rotation";

//  else
        return "";
}

default
{
    touch_start(integer num_detected)
    {
        list listOfStuff = [
            <1.0, 2.0, 3.0, 4.0>,
            <1.0, 2.0, 3.0>,
            llGetKey(),
            "some random text",
            382.4,
            1];

        integer index = ~llGetListLength(listOfStuff);

        // start with -length and end with -1
        while (++index)
        {
            integer type = llGetListEntryType(listOfStuff, index);
            string entry2string = llList2String(listOfStuff, index);

            llSay(0, "'" + entry2string + "' has the list-entry-type: '" + get_list_entry_type_info(type) + "'");
        }
    }
}
```

## See Also

### Functions

- llList2Float
- llList2Integer
- llList2Key
- llList2Rot
- llList2String
- llList2Vector

### Articles

- Negative Index

<!-- /wiki-source -->
