---
name: "llParseString2List"
category: "function"
type: "function"
language: "LSL"
description: "Splits a string into a list using separator and spacer delimiters; discards separators, keeps spacers, removes empty entries"
wiki_url: "https://wiki.secondlife.com/wiki/llParseString2List"
first_fetched: "2026-03-09"
last_updated: "2026-03-09"
signature: "list llParseString2List(string src, list separators, list spacers)"
parameters:
  - name: "src"
    type: "string"
    description: "Source string to parse"
  - name: "separators"
    type: "list"
    description: "Delimiter strings to discard (max 8)"
  - name: "spacers"
    type: "list"
    description: "Delimiter strings to keep in output (max 8)"
return_type: "list"
energy_cost: "10.0"
sleep_time: "0.0"
patterns: ["llparsestring2list"]
deprecated: "false"
---

# llParseString2List

```lsl
list llParseString2List(string src, list separators, list spacers)
```

Breaks `src` into list elements. Separators are discarded; spacers are kept as elements. All resulting empty strings are discarded.

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `src` | string | Source string |
| `separators` | list | Delimiters to discard (max 8 entries) |
| `spacers` | list | Delimiters to keep (max 8 entries) |

## Caveats

- **Empty strings removed:** Adjacent separators and separators at string boundaries produce empty entries that are automatically removed.
- **Maximum 8 separators and 8 spacers** — additional entries are silently ignored.
- **Separators take priority** over spacers.
- **All output elements are strings** — cast as needed.
- Use `llParseStringKeepNulls` to preserve empty entries.
- Use `llCSV2List` for comma-separated data with vectors/rotations.

## Examples

```lsl
// Split words, keeping periods
list result = llParseString2List("A crazy fox. Saw the moon..", [" "], ["."]);
// Result: ["A", "crazy", "fox", ".", "Saw", "the", "moon", ".", "."]

// Split CSV manually
list parts = llParseString2List("one,two,three", [","], []);
// Result: ["one", "two", "three"]

// Split command with arguments
string input = "move 5 10 20";
list tokens = llParseString2List(input, [" "], []);
string cmd = llList2String(tokens, 0);    // "move"
float x = (float)llList2String(tokens, 1); // 5.0
```

## See Also

- `llParseStringKeepNulls` — same but preserves empty elements
- `llCSV2List` — parse comma-separated values (handles vectors/rotations)
- `llList2CSV` — join list to CSV string
- `llDumpList2String` — join list with custom separator


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llParseString2List) — scraped 2026-03-18_

Returns a list that is src broken into a list of strings, discarding separators, keeping spacers, discards any null (empty string) values generated.

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

- llParseStringKeepNulls
- llDumpList2String
- llCSV2List
- llList2CSV

### Articles

- Separate Words
- LSL-Editor/Bugs

<!-- /wiki-source -->
