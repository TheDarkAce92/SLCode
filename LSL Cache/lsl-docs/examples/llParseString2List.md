---
name: "llParseString2List"
category: "example"
type: "example"
language: "LSL"
description: "Returns a list that is src broken into a list of strings, discarding separators, keeping spacers, discards any null (empty string) values generated."
wiki_url: "https://wiki.secondlife.com/wiki/LlParseString2List"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

/LSL


ParseString2ListllParseString2List

- 1 Summary
- 2 Caveats
- 3 Examples
- 4 Useful Snippets
- 5 Notes
- 6 See Also

  - 6.1 Functions
  - 6.2 Articles
- 7 Deep Notes

  - 7.1 History
  - 7.2 Footnotes
  - 7.3 Signature

## Summary

 Function: list **llParseString2List**( string src, list separators, list spacers );

0.0

Forced Delay

10.0

Energy

Returns a list that is src broken into a list of strings, discarding separators, keeping spacers, discards any null (empty string) values generated.

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

In most situations llParseStringKeepNulls should be used instead. Discarding null values is rarely desired.

When dealing with vector and rotation data, consider using llCSV2List instead, since it can correctly parse them.

## Caveats

- All empty strings (that would arise from a spacer or separator being adjacent to each other or the ends) are removed;

  - If you want them (to keep the order of a list, for example) use llParseStringKeepNulls instead;
- Only the first 8 separators and first 8 spacers supplied will be used. Any beyond that will be ignored. To work around this see #Useful Snippets section below. The only limit on the number of items in the output is available script memory.
- All separators and spacers must be strings. All other types will be ignored;
- Separators take precedent over spacers. The string is parsed from start to finish. Each position is compared against the separators then spacers before moving onto the next position;
- Duplicate separators and spacers have no ill effects;
- All elements in the list returned by llParseString2List are strings, and must be explicitly typecast if they are to be used as other types. Do not rely upon the implicit typecasting of the other llList2* functions (as they typically return a default value);
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

While LSL does not support lists-in-lists, you can emulate lists-in-lists by making successive calls or you could use JSON.

In this example some items have additional information supplied.

```lsl

string shoppinglist = "macaroni::pepperoni::bread#wheat::sausage#italian::coffee::syrup::apple::ice cream#strawberry#chocolate#vanilla";

default
{
    state_entry()
    {
        list items = llParseString2List(shoppinglist, ["::"], []);
        integer i = 0;
        integer j = llGetListLength(items);
        for(;i < j; ++i)
        {
            list desc = llParseString2List(llList2String(items, i), ["#"], []);
            if(llGetListLength(desc) > 1)
            {
                list types = llDeleteSubList(desc,0,0);
                llOwnerSay("Item: "+ llList2String(desc, 0) + "  Type: " + llList2CSV(llDeleteSubList(types,-2,-1) + llDumpList2String(llList2List(types,-2,-1), " & ")));
            } else {
                llOwnerSay("Item: "+ (string)desc);
            }
        }
    }
}
```

## Useful Snippets

**Examples of processing more than 8 spacers or separators:**

•

ParseString2List

–

Functions exactly the same as llParseString2List and llParseStringKeepNulls.

•

separateWords

–

Functions exactly the same as llParseString2List unless you violate it's additional preconditions.

Appears to be correct at a glance.

## Notes

Whenever you need to process the resulting list entries further (eg. typecasting), remember to llStringTrim any whitespace characters from the string. This can prevent issues such as unexpected values for vectors and rotations.

If you indicate some items as separators, it will split the string where it finds the indicated separators, and strip out the separators.

If instead you indicate some items as spacers, it will split the string where it finds the spacers, but leave the spacers there, including them as separate entries in the result list.

```lsl
string myString = "What Are You Looking At?";

llSay(0, llList2CSV( llParseString2List(myString,  ["W", "A", "Y", "L"], [] ) ) );
//returns:  hat , re , ou , ooking , t?

llSay(0, llList2CSV( llParseString2List(myString, [], ["W", "A", "Y", "L"] ) ) );
//returns: W, hat , A, re , Y, ou , L, ooking , A, t?
```

Using " " as a separator will parse a sentence into words.

If there is no spacer you care about, just use `[]` as the spacer.

If an empty string is used as a separator or a spacer, it will have no effect.

## See Also

### Functions

•

llParseStringKeepNulls

•

llDumpList2String

•

llCSV2List

•

llList2CSV

### Articles

•

Separate Words

•

LSL-Editor/Bugs

## Deep Notes

#### History

- llParseString2List Added in [SL 0.6.0](http://secondlife.wikia.com/wiki/Version_0.6.0)

#### Footnotes

1. **^** Early release notes were not very accurate or thorough, they sometimes included information about features added in previous releases or failed to include information about features added in that release.

#### Signature

```lsl
function list llParseString2List( string src, list separators, list spacers );
```