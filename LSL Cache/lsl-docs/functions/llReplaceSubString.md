---
name: "llReplaceSubString"
category: "function"
type: "function"
language: "LSL"
description: 'Returns a string that is the result of replacing the first count matching instances pattern in src with replacement_pattern.

If count = 0, all matching substrings are replaced. If count > 0, substrings are replaced starting from the left/beginning of src. If count < 0, substrings are replaced start'
signature: "string llReplaceSubString(string source, string search, string replace, integer count)"
return_type: "string"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llReplaceSubString'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
---

Returns a string that is the result of replacing the first count matching instances pattern in src with replacement_pattern.

If count = 0, all matching substrings are replaced. If count > 0, substrings are replaced starting from the left/beginning of src. If count < 0, substrings are replaced starting from the right/end of src.


## Signature

```lsl
string llReplaceSubString(string source, string search, string replace, integer count);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `string` | `src` |  |
| `string` | `pattern` |  |
| `string` | `replacement_pattern` |  |
| `integer` | `count` |  |


## Return Value

Returns `string`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llReplaceSubString)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llReplaceSubString) — scraped 2026-03-18_

Returns a string that is the result of replacing the first count matching instances pattern in src with replacement_pattern.

## Examples

```lsl
default
{
    state_entry()
    {
        string ex = "red foxes, red hens, red turnips";
        // Replace first 2 matches, starting from the left side
        ex = llReplaceSubString(ex, "red", "blue", 2);
        llSay(0, ex); // Should say "blue foxes, blue hens, red turnips"
    }
}
```

```lsl
default
{
    state_entry()
    {
        string ex = "red foxes, red hens, red turnips";
        // Replace first match, starting from the right side
        ex = llReplaceSubString(ex, "red", "green", -1);
        llSay(0, ex); // Should say "red foxes, red hens, green turnips"
    }
}
```

```lsl
default
{
    state_entry()
    {
        string ex = "red foxes, red hens, red turnips";
        // Replace all matches
        ex = llReplaceSubString(ex, "red", "yellow", 0);
        llSay(0, ex); // Should say "yellow foxes, yellow hens, yellow turnips"
    }
}
```

## See Also

### Functions

- llGetSubString
- llDeleteSubString
- llInsertString
- llDeleteSubList

<!-- /wiki-source -->
