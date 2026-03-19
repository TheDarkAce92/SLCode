---
name: "llDumpList2String"
category: "function"
type: "function"
language: "LSL"
description: 'Returns a string that is the list src converted to a string with separator between the entries.

Use llParseString2List or llParseStringKeepNulls to undo the process.

Unlike llList2CSV, which dumps a list to a comma-separated formatted string with no choice over the separator, llDumpList2String giv'
signature: "string llDumpList2String(list src, string separator)"
return_type: "string"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llDumpList2String'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["lldumplist2string"]
---

Returns a string that is the list src converted to a string with separator between the entries.

Use llParseString2List or llParseStringKeepNulls to undo the process.

Unlike llList2CSV, which dumps a list to a comma-separated formatted string with no choice over the separator, llDumpList2String gives you more control. This can be useful if you don't trust commas as a separator because you might be working with data supplied to the script by a user who uses, say, commas as part of a street address.


## Signature

```lsl
string llDumpList2String(list src, string separator);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `list` | `src` |  |
| `string` | `separator` |  |


## Return Value

Returns `string`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llDumpList2String)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llDumpList2String) — scraped 2026-03-18_

Returns a string that is the list src converted to a string with separator between the entries.

## Examples

```lsl
list mylist = ["a", "b", "c", "d"];
string tmp = llDumpList2String(mylist, "**");
//tmp now equals: "a**b**c**d"
```

```lsl
list mylist = [<10,5,7>, 100, "c", "d"];
string tmp = llDumpList2String(mylist, "**");
//tmp now equals: "<10,5,7>**100**c**d"
```

```lsl
default{
    state_entry(){
        list my_list = [1, 2.0, "a string", llGetOwner()];
        llOwnerSay("<" + llDumpList2String(my_list,"><") + ">");
//says: "<1><2.000000>"
    }
}
```

## Notes

Instead of using `llDumpList2String(myList, "")` you may wish to consider using the more efficient `(string)myList` as it produces an identical result with less memory usage due to eliminating a function-call. Each element of the list is converted to string format in the result, so floats expand to six digits of precision, rotations and vectors are represented with "<" and ">" characters, etc.

## See Also

### Functions

- llParseString2List
- llParseStringKeepNulls
- llCSV2List
- llList2CSV

### Articles

- Typecast

<!-- /wiki-source -->
