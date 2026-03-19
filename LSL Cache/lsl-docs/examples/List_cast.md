---
name: "List cast"
category: "example"
type: "example"
language: "LSL"
description: "Iterates through the contents of a list, producing a resulting list whose contents are cast from strings to their identified type. This function is useful for converting a list of strings, such as from llParseString2List, to a list that could be used for llSetPrimitiveParams, or a list you know you are going to use a lot to save on casting all the time.Returns a list whose contents are cast to their identified types."
wiki_url: "https://wiki.secondlife.com/wiki/List_cast"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

/LSL


List_castlist_cast

- 1 Summary
- 2 Caveats
- 3 Examples
- 4 Implementation

## Summary

 Function: list **list_cast**( list in );

Iterates through the contents of a list, producing a resulting list whose contents are cast from strings to their identified type. This function is useful for converting a list of strings, such as from llParseString2List, to a list that could be used for llSetPrimitiveParams, or a list you know you are going to use a lot to save on casting all the time.Returns a list whose contents are cast to their identified types.

• list

in

–

The list to cast, its contents should be all strings.

## Caveats

- Any strings fed into this function (which are meant to stay strings) cannot contain pointed brackets (<>) They will be cast as vectors or rotations, if they do.

## Examples

```lsl
        list in = ["1", "<1.0,2.5,0.5>", "0.8", "0", "Four", "8aef4875-6873-0919-f5ab-c9d6b48d18d4"];

        in = list_cast(in);
        llSetScale( llList2Vector(in,1) );
        llSetAlpha( llList2Float(in,2), llList2Integer(in,3) );
```


Implementation

```lsl
//This function typecasts a list of strings, into the types they appear to be.
//Extremely useful for feeding user data into llSetPrimitiveParams
//It takes a list as an input, and returns that list, with all elements correctly typecast, as output
//Written by Fractured Crystal, 27 Jan 2010, Commissioned by WarKirby Magojiro, this function is Public Domain
list list_cast(list in)
{
    list out;
    integer i = 0;
    integer l= llGetListLength(in);
    while(i < l)
    {
        string d= llStringTrim(llList2String(in,i),STRING_TRIM);
        if(d == "")out += "";
        else
        {
            if(llGetSubString(d,0,0) == "<")
            {
                if(llGetSubString(d,-1,-1) == ">")
                {
                    list s = llParseString2List(d,[","],[]);
                    integer sl= llGetListLength(s);
                    if(sl == 3)
                    {
                        out += (vector)d;
                        //jump end;
                    }else if(sl == 4)
                    {
                        out += (rotation)d;
                        //jump end;
                    }
                }
                //either malformed,or identified
                jump end;
            }
            if(llSubStringIndex(d,".") != -1)
            {
                out += (float)d;
            }else
            {
                integer lold = (integer)d;
                if((string)lold == d)out += lold;
                else
                {
                    key kold = (key)d;
                    if(kold)out += [kold];
                    else out += [d];
                }
            }
        }
        @end;
        i += 1;
    }

    return out;
}
```