---
name: "ParseString2List"
category: "example"
type: "example"
language: "LSL"
description: "Returns a list that is src broken into a list, discarding separators, keeping spacers."
wiki_url: "https://wiki.secondlife.com/wiki/Parse_String_To_List"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

## Function: list ParseString2List(string src

Returns a list that is **src** broken into a list, discarding **separators**, keeping **spacers**.

### if ParseStringKeepNulls

Same as **llParseString2List**, but not limited to 8 spacers or separators.

Thus substitute a call to the **llParseString2List** function by a call to **ParseString2List** whenever you have more than 8 separators or more than 8 spacers.

### if ParseStringKeepNulls

Same as **llParseStringKeepNulls**, but not limited to 8 spacers or separators.

Thus substitute a call to the **llParseStringKeepNulls** function by a call to **ParseString2List** whenever you have more than 8 separators or more than 8 spacers.

```lsl
list ParseString2List(string src, list separators, list spacers, integer ParseStringKeepNulls)
{//works just like llParseString2List and llParseStringKeepNulls
 //Instead of each list being limited to 8 items, it is now 1024.
 //The max length of src is 2,097,151 characters.
    integer i = ~(separators != []);
    integer r = (spacers != []);
    spacers += separators;
    list out = "" + (separators = []);
    string p;
    integer offset;
    while((i = -~i) < r)
        if(!~llListFindList(out, (list)(p = llList2String(spacers, i))))
            if(~(offset = llSubStringIndex(src, p)))
            {
                separators += ((offset + 0xFFF00000) << 11) | (i + 0x400);
                out += p;
            }
    out = [];
    offset = 0xFFF00000;
    while(separators != [])//Can't use just "while(separators)" because of JIRA:SVC-689
    {
        if(offset <= (i = ( (r = llList2Integer(separators = llListSort(separators, 1, TRUE), 0) ) >> 11) ) )
        {
            if(offset ^ i || ParseStringKeepNulls)
                out += llDeleteSubString(src, i - offset, -1);
            src = llDeleteSubString(src, 0, ~(offset - (i += llStringLength(p = llList2String(spacers, (r & 0x7FF) - 0x400)))));
            if(r & 0x400)
                out += p;
            offset = i;
        }
        separators = llDeleteSubList(separators, 0, 0);
        if(~(i = llSubStringIndex(src, p)))
            separators += ((i + offset) << 11) | (r & 0x7FF);
    }
    if(src != "" || ParseStringKeepNulls)
        out += src;
    return out;
}//Strife Onizuka
```

```lsl
//Use for testing the function.
string test(string src, list separators, list spacers, integer nulls)
{
    list t = [];
    if(nulls)
        t = llParseStringKeepNulls(src, separators, spacers);
    else
        t = llParseString2List(src, separators, spacers);
    string a = llList2CSV(t);
    string b = llList2CSV(ParseString2List(src, separators, spacers, nulls));
    return (string)(a==b) + " : " + a + "            " + b;
}

default
{
    state_entry()
    {
        llOwnerSay("----------------  " + (string)llGetFreeMemory());
        llOwnerSay(test("abcdefg", ["b"], ["b"], FALSE));
        llOwnerSay(test("abcdefg", ["b"], ["bc"], FALSE));
        llOwnerSay(test("abcdefg", ["bc"], ["b"], FALSE));
        llOwnerSay(test("abcdefg", ["b"], ["ab"], FALSE));
        llOwnerSay(test("abcdefg", ["b", "g"], ["ab"], FALSE));
        llOwnerSay(test("abcdefg", ["b"], ["ab", "g"], FALSE));
        llOwnerSay(test("abcdefg", ["b", "a"], ["a", "b"], FALSE));
        llOwnerSay(test("abcdefg", ["a", "b"], ["b", "a"], FALSE));
        llOwnerSay(test("abcdefg", ["b", "c"], ["a", "b"], FALSE));
        llOwnerSay(test("abcdefg", ["c", "b"], ["b", "a"], FALSE));
        llOwnerSay(test("abcdefg", ["b", "a"], ["c", "b"], FALSE));
        llOwnerSay(test("abcdefg", ["a", "b"], ["b", "c"], FALSE));
        llOwnerSay(test("abcdefg", ["b"], ["b"], TRUE));
        llOwnerSay(test("abcdefg", ["b"], ["bc"], TRUE));
        llOwnerSay(test("abcdefg", ["bc"], ["b"], TRUE));
        llOwnerSay(test("abcdefg", ["b"], ["ab"], TRUE));
        llOwnerSay(test("abcdefg", ["b", "g"], ["ab"], TRUE));
        llOwnerSay(test("abcdefg", ["b"], ["ab", "g"], TRUE));
        llOwnerSay("----------------  " + (string)llGetFreeMemory());
    }
}
```

See also: Script Library - Separate Words