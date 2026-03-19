---
name: "llList2CSV"
category: "example"
type: "example"
language: "LSL"
description: "Returns a string of comma separated values taken in order from src."
wiki_url: "https://wiki.secondlife.com/wiki/LlList2CSV"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

/LSL


List2CSVllList2CSV

- 1 Summary
- 2 Caveats
- 3 Examples
- 4 See Also

  - 4.1 Functions
  - 4.2 Articles
- 5 Deep Notes

  - 5.1 Signature

## Summary

 Function: string **llList2CSV**( list src );

0.0

Forced Delay

10.0

Energy

Returns a string of comma separated values taken in order from **src**.

• list

src

More precisely the values are separated with a comma and a space (", ").


This function's functionality is equivalent to `llDumpList2String(src, ", ");`


The result of this function is more or less the  [CSV](https://en.wikipedia.org/wiki/Comma-separated_values) format, but it does not conform in all its details.


To reverse the process use llCSV2List.  But see the Caveat.

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

•

llCSV2List

•

llDumpList2String

•

llParseString2List

•

llParseStringKeepNulls

### Articles

•

Typecast

## Deep Notes

#### Signature

```lsl
function string llList2CSV( list src );
```