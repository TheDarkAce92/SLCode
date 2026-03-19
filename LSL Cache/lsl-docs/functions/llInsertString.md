---
name: "llInsertString"
category: "function"
type: "function"
language: "LSL"
description: 'Returns the string dst with src inserted starting at pos.

pos does not support negative indexes.
i.e. unlike other somewhat similar string functions such as llGetSubString and llDeleteSubString, you cannot use -1 for the counting with this function. You may use instead the function provided a bit f'
signature: "string llInsertString(string dst, integer position, string src)"
return_type: "string"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llInsertString'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llinsertstring"]
---

Returns the string dst with src inserted starting at pos.

pos does not support negative indexes.
i.e. unlike other somewhat similar string functions such as llGetSubString and llDeleteSubString, you cannot use -1 for the counting with this function. You may use instead the function provided a bit further below.


## Signature

```lsl
string llInsertString(string dst, integer position, string src);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `string` | `dst` | destination of insertion |
| `integer` | `pos` | position index for insert, first is 0 |
| `string` | `src` | source string to be inserted |


## Return Value

Returns `string`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llInsertString)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llInsertString) — scraped 2026-03-18_

Returns the string dst with src inserted starting at pos.

## Caveats

- If pos is out of bounds  the script continues to execute without an error message.

## Examples

```lsl
llInsertString("input", 2, "put out")// returns "input output"
```

## See Also

### Functions

- llDeleteSubString
- llGetSubString
- llReplaceSubString

### Articles

- **Examples:** — Replace all instances of a string with another string in a target string
- **Examples:** — Insert 'new line' escape codes at certain positions of a string

<!-- /wiki-source -->
