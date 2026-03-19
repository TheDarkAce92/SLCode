---
name: "llParseStringKeepNulls"
category: "example"
type: "example"
language: "LSL"
description: "Returns a list that is src broken into a list, discarding separators, keeping spacers, keeping any null values generated."
wiki_url: "https://wiki.secondlife.com/wiki/LlParseStringKeepNulls"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

/LSL


ParseStringKeepNullsllParseStringKeepNulls

- 1 Summary
- 2 Specification
- 3 Caveats
- 4 Examples
- 5 Useful Snippets
- 6 See Also

  - 6.1 Functions
- 7 Deep Notes

  - 7.1 Signature

## Summary

 Function: list **llParseStringKeepNulls**( string src, list separators, list spacers );

0.0

Forced Delay

10.0

Energy

Returns a list that is src broken into a list, discarding separators, keeping spacers, keeping any null values generated.

• string

src

–

source string

• list

separators

–

separators to be discarded

• list

spacers

–

spacers to be kept

## Specification

The behavior is identical to that for llParseString2List, except blank strings found in the list are kept. This is useful when parsing a list that contains values that can be null or empty (and subsequently removing the nulls would upset the distribution of data and the element indexes).

llParseStringKeepNulls("", ["~"], []) will return [""]

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

## Useful Snippets

**Replacement functions without or very large separator/spacer count limits**

•

ParseString2List

–

Functions exactly the same as llParseString2List and llParseStringKeepNulls.

•

separateWords

–

Functions the same as llParseString2List unless certain preconditions are not met.

## See Also

### Functions

•

llParseString2List

•

llDumpList2String

•

llCSV2List

•

llList2CSV

## Deep Notes

#### Signature

```lsl
function list llParseStringKeepNulls( string src, list separators, list spacers );
```