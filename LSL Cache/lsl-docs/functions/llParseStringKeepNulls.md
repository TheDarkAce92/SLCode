---
name: "llParseStringKeepNulls"
category: "function"
type: "function"
language: "LSL"
description: "Returns a list that is src broken into a list, discarding separators, keeping spacers, keeping any null values generated."
signature: "list llParseStringKeepNulls(string src, list separators, list spacers)"
return_type: "list"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llParseStringKeepNulls'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llparsestringkeepnulls"]
---

Returns a list that is src broken into a list, discarding separators, keeping spacers, keeping any null values generated.


## Signature

```lsl
list llParseStringKeepNulls(string src, list separators, list spacers);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `string` | `src` | source string |
| `list` | `separators` | separators to be discarded |
| `list` | `spacers` | spacers to be kept |


## Return Value

Returns `list`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llParseStringKeepNulls)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llParseStringKeepNulls) — scraped 2026-03-18_

Returns a list that is src broken into a list, discarding separators, keeping spacers, keeping any null values generated.

## Caveats

- Only the first 8 separators and first 8 spacers will be used any extras will be ignored.
- All separators and spacers must be strings, all other types will be ignored.
- separators take precedent over spacers. The string is parsed from start to finish, each position is compared against the separators then spacers before moving onto the next position. The first match is the one that is returned. Using the list ["A", "AB"] will always act with "A" and never "AB".
- Duplicate or irrelevant separators or spacers count towards the limits and slow down parsing.
- All entries in the return are typed as string. Use explicit typecasting on llList2String to convert the values into other types. Do not rely upon the implicit typecasting of the other llList2* functions (as they typically return a default value).
- Remember to capture the result of the operation with a variable, unless you are planning to act directly on the results.

## Examples

```lsl
default
{
    state_entry()
    {
        // This will say:
        // <.><.><.>
        string my_string = "A crazy fox.  Saw the moon..";
        list my_list = llParseString2List(my_string,[" "],["."]);
        llOwnerSay("<" + llDumpList2String(my_list,"><") + ">");

        // This will say:
        //  <.><><><.><><.><>
        my_list = llParseStringKeepNulls(my_string,[" "],["."]);
        llOwnerSay("<" + llDumpList2String(my_list,"><") + ">");
    }
}
```

## See Also

### Functions

- llParseString2List
- llDumpList2String
- llCSV2List
- llList2CSV

<!-- /wiki-source -->
