---
name: "llCSV2List"
category: "example"
type: "example"
language: "LSL"
description: "This function takes a string of values separated by commas, and turns it into a list.Returns a list made by parsing src, a string of comma separated values."
wiki_url: "https://wiki.secondlife.com/wiki/LlCSV2List"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

/LSL


CSV2ListllCSV2List

- 1 Summary
- 2 Specification

  - 2.1 Vectors & Rotations
  - 2.2 Types
  - 2.3 Whitespace
- 3 Caveats
- 4 Examples
- 5 Notes
- 6 See Also

  - 6.1 Functions
  - 6.2 Articles
- 7 Deep Notes

  - 7.1 Signature

## Summary

 Function: list **llCSV2List**( string src );

0.0

Forced Delay

10.0

Energy

This function takes a string of values separated by commas, and turns it into a list.**Returns a list made by parsing src**, a string of comma separated values.

• string

src

To convert a list into a comma-separated string use llList2CSV.

Do not confuse this function with the * CSV format, it is not* the CSV format. ## Specification ### Vectors & Rotations Anything between "<" and ">" is considered a single value regardless of the existence of a comma between. This ensures that vectors and rotations get treated as a single value, with no additional cleanup needed afterward.

Note, though, that for every "<" there needs to be a corresponding ">" or it will consume the rest of the string. For example,

•

 `llCSV2List("<>,>,a")`

–

returns `["<>", ">", "a"]`

(Second ">" is isolated)

•

 `llCSV2List("<<>,>,a")`

–

returns `["<<>,>", "a"]`

(Regularly paired)

•

 `llCSV2List("<<<>,>,a")`

–

returns `["<<<>,>,a"]`

(Third "<" lost its opposite one)

### Types

The function makes no assumptions about what the list entry types should be, all elements in the resulting list will be strings. It is important to know that the llList2* functions implicit typecasts do not work the same as explicit typecast. The following table gives code examples for each type that will yield the best results.

Target

Code

Description

integer

`(integer)llList2String(mlist, mint)`

llList2Integer does not support the hex format

float

`(float)llList2String(mlist, mint)`

llList2Float does not support the scientific or hexadecimal notations

string

`llList2String(mlist, mint)`

Always Safe

key

`llList2Key(mlist, mint)`

Always Safe

vector

`(vector)llList2String(mlist, mint)`

llList2Vector will return a zero vector

rotation

`(rotation)llList2String(mlist, mint)`

llList2Rot will return a zero rotation

### Whitespace

llCSV2List consumes the first leading space from all values :

```lsl
list tmp = llCSV2List("first , second , third");
//returns ["first ","second ","third"]
//not ["first "," second "," third"]
```

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

•

llList2CSV

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
function list llCSV2List( string src );
```