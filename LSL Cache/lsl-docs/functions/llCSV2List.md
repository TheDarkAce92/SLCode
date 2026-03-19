---
name: "llCSV2List"
category: "function"
type: "function"
language: "LSL"
description: 'This function takes a string of values separated by commas, and turns it into a list.

Returns a list made by parsing src, a string of comma separated values.

To convert a list into a comma-separated string use llList2CSV.
Do not confuse this function with the CSV format, it is not the CSV format.'
signature: "list llCSV2List(string src)"
return_type: "list"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llCSV2List'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llcsv2list"]
---

This function takes a string of values separated by commas, and turns it into a list.

Returns a list made by parsing src, a string of comma separated values.

To convert a list into a comma-separated string use llList2CSV.
Do not confuse this function with the CSV format, it is not the CSV format.


## Signature

```lsl
list llCSV2List(string src);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `string` | `src` |  |


## Return Value

Returns `list`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llCSV2List)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llCSV2List) — scraped 2026-03-18_

This function takes a string of values separated by commas, and turns it into a list.Returns a list made by parsing src, a string of comma separated values.

## Caveats

- If a "<" does not have a matching ">", the remainder of the string will be a single value, even if the "<" is in the middle of the value, see Vectors & Rotations for further details.
- All items in the returned list are strings.
- If an empty string is parsed, the result will a list containing an empty string: [""] (not an empty list).
- When used with lists that are generated based off assets in inventory, llCSV2List should not be used, as inventory assets can contain commas as part of their names.

## Examples

```lsl
default
{
    state_entry()
    {
        string csv = "first,second,third";
        list my_list = llCSV2List(csv);
        llOwnerSay("CSV: " + csv);
        integer i;
        integer num_list=llGetListLength(my_list);
        for (i=0; i

## Notes

To use separators other than commas (especially if you can't predict when a user might have sneaked a comma into data they supply the script), use llParseString2List instead, which allows you to specify separators other than commas. llParseString2List unfortunately does not support the special parsing required for handling rotations and vectors, nor does it consume leading and trailing whitespace.

## See Also

### Functions

- llList2CSV
- llDumpList2String
- llParseString2List
- llParseStringKeepNulls

### Articles

- Typecast

<!-- /wiki-source -->
