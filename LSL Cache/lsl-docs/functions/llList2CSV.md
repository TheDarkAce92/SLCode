---
name: "llList2CSV"
category: "function"
type: "function"
language: "LSL"
description: 'Returns a string of comma separated values taken in order from src.

More precisely the values are separated with a comma and a space (', ').

This function's functionality is equivalent to llDumpList2String(src, ', ');

The result of this function is more or less the CSV format, but it does not con'
signature: "string llList2CSV(list src)"
return_type: "string"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llList2CSV'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["lllist2csv"]
---

Returns a string of comma separated values taken in order from src.

More precisely the values are separated with a comma and a space (", ").

This function's functionality is equivalent to llDumpList2String(src, ", ");

The result of this function is more or less the CSV format, but it does not conform in all its details.

To reverse the process use llCSV2List. But see the Caveat.


## Signature

```lsl
string llList2CSV(list src);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `list` | `src` |  |


## Return Value

Returns `string`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llList2CSV)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llList2CSV) — scraped 2026-03-18_

Returns a string of comma separated values taken in order from src.

## Caveats

- llCSV2List will not reverse the process if there are commas or oddly matched angle brackets (**<** and **>**) in any of the original strings. For details see the article llCSV2List.

  - One way around this is to first use llEscapeURL on any user-supplied strings before adding them to the list. llUnescapeURL will reverse llEscapeURL.
  - If your strings may contain commas but not unmatched angle brackets you can wrap your strings with angle brackets (< and >) like you would use double quotes around the string and then use llGetSubString with START at 1 and END at -2 to remove them.

## Examples

```lsl
default
{
    state_entry()
    {
        list my_list = [FALSE, PI, "a string", ZERO_VECTOR, ZERO_ROTATION, NULL_KEY];
        llOwnerSay(llList2CSV(my_list));
    }
}
```

## See Also

### Functions

- llCSV2List
- llDumpList2String
- llParseString2List
- llParseStringKeepNulls

### Articles

- Typecast

<!-- /wiki-source -->
