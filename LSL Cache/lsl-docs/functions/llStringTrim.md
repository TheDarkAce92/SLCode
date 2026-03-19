---
name: "llStringTrim"
category: "function"
type: "function"
language: "LSL"
description: "Returns a string that is src with leading and/or trailing white space (spaces, tabs, and line feeds) trimmed from it."
signature: "string llStringTrim(string src, integer trim_type)"
return_type: "string"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llStringTrim'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llstringtrim"]
---

Returns a string that is src with leading and/or trailing white space (spaces, tabs, and line feeds) trimmed from it.


## Signature

```lsl
string llStringTrim(string src, integer trim_type);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `string` | `src` |  |
| `integer` | `type` | STRING_TRIM* flag(s) |


## Return Value

Returns `string`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llStringTrim)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llStringTrim) — scraped 2026-03-18_

Returns a string that is src with leading and/or trailing white space (spaces, tabs, and line feeds) trimmed from it.

## Examples

Whenever you are accepting unstructured input from a user -- whether via chat or via a notecard -- it is a good idea to always full trim it:

```lsl
llStringTrim("User input", STRING_TRIM);
```

This example returns the number of leading and trailing 'white space' characters on a string that were removed (not particularly useful but shows how to use the function).

```lsl
default
{
    state_entry()
    {
        llListen(4, "", llGetOwner(), "");
    }

    on_rez(integer start_param)
    {
        llResetScript();
    }

    listen(integer channel, string name, key id, string message)
    {
        //track the length
        integer length = llStringLength(message);

        //trim message (not necessary to store these to variables but makes reading easier)
        string trim_left  = llStringTrim(message, STRING_TRIM_HEAD);
        string trim_right = llStringTrim(message, STRING_TRIM_TAIL);
        string trim_both  = llStringTrim(message, STRING_TRIM);

        //output the results
        llOwnerSay("Initial length  = " + (string)length +
                 "\nLeading Spaces  = " + (string)(length - llStringLength(trim_left))+
                 "\nTrailing Spaces = " + (string)(length - llStringLength(trim_right))+
                 "\nTrimmed Message = \"" + trim_both + "\"");
    }
}
```

## Notes

- The exact set of characters stripped are 0x09 (tab), line feed (0x0a, "\n"), vertical tab (0x0b), form feed (0x0c), carriage return (0x0d) and space (0x20, " ").

  - Only line feed and space function as true whitespace within SL, the others will produce some manner of a printable character.
  - The "\t" escape code doesn't actually represent the tab character, but several spaces instead.
  - Other whitespace characters defined in Unicode, such as non-breaking space (0xa0) or specific-width spaces in the 0x2000 range are not stripped.
- Aside from white space at the beginning and / or end, the actual string will be unaffected. This means too, though, that extraneous spaces within the string -- for instance, a mistaken double-space type -- will not be corrected.
- The following will remove all doubled (or further multiplied), leading and trailing spaces with iterated llReplaceSubString:

```lsl
while(llStringLength(s) != llStringLength(s = llReplaceSubString(s, "  ", " ", 0)));
s = llStringTrim(s, STRING_TRIM);
```

- llReplaceSubString is also the easiest way to remove all spaces from a string:

```lsl
llReplaceSubString("some words to remove the spaces from", " ", "", 0);
```

- llList2Json also trims strings contained in the list. Thus, an easy way to trim an entire list of strings is:

```lsl
list l = ["  a  ", " b", "c ", " d "];
list trimmedList = llJson2List(llList2Json(JSON_ARRAY, l));
```

- Some old, less efficient methods, no longer recommended for use:

- Intra-string space trimming:

```lsl
llDumpList2String(llParseString2List(src, [" "], []), " "); //works but can use a large quantity of memory
```

- An method to strip spaces from the sentence:

```lsl
//Added By To-mos Codewarrior
string str1 = "some words to remove the spaces from";
integer index;
while(~index=llSubStringIndex(str1," ")) {
    data=llDeleteSubString(str1,index,index);
}
```

- Variant of above:

```lsl
(string)llParseString2List(src, [" "], []); //works but can use a large quantity of memory
```

<!-- /wiki-source -->
