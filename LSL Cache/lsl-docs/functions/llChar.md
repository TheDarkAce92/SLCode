---
name: "llChar"
category: "function"
type: "function"
language: "LSL"
description: 'Construct a single character string from the supplied Unicode value.

This function returns a single character string generated from the character at the indicated UTF-32 codepoint.
If val is negative, the codepoint has no valid single-character UTF-16 representation such as a part of a surrogate pa'
signature: "string llChar(integer code)"
return_type: "string"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llChar'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
---

Construct a single character string from the supplied Unicode value.

This function returns a single character string generated from the character at the indicated UTF-32 codepoint.
If val is negative, the codepoint has no valid single-character UTF-16 representation such as a part of a surrogate pair, or is outside defined range, the Unicode replacement character "�" (0xFFFD) is returned.
If val is 0, an empty string is returned.


## Signature

```lsl
string llChar(integer code);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `integer` | `val` | Unicode value for character. |


## Return Value

Returns `string`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llChar)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llChar) — scraped 2026-03-18_

Construct a single character string from the supplied Unicode value.Returns a string

## Caveats

- Value range is between `0x1`–`0x10FFFF`
- Values in the surrogate range `0xD800`–`0xDFFF` will return the replacement character "�" (`0xFFFD`) instead
- Values for the special noncharacters `0xFFFE` and `0xFFFF` will return the replacement character instead
- SLua's equivilant `utf8.char` has none of the above caveats, and also handles `0x0` (the null character) correctly ([validation script, in SLua](https://github.com/secondlife/lsl-definitions/pull/74#discussion_r2934141244))
- Values for UTF-8 multibyte ranges are:

  - 1 byte: `0x0`–`0x7F`
  - 2 bytes: `0x80`–`0x07FF`
  - 3 bytes: `0x0800`–`0xFFFF`
  - 4 bytes: `0x10000`–`0x10FFFF`

## Examples

```lsl
default
{
    touch_start(integer total_number)
    {
        string test_string = "The quick brown fox jumped over the lazy dog";
        list test_list = [];
        string test_string2 = "";

        integer index;
        integer ord;
        for (index = 0; index < llStringLength(test_string); ++index)
        {
            ord = llOrd(test_string, index);
            test_list = test_list + [ ord ];
        }

        string char;
        for (index = 0; index < llGetListLength(test_list); ++index)
        {
            ord = llList2Integer(test_list, index);
            char = llChar(ord);
            test_string2 = test_string2 + char;
        }

        llSay(0, "\"" + test_string + "\" -> [" +
            llDumpList2String(test_list, ", ") + "] -> \"" + test_string2 + "\"");
    }
}
```

## See Also

### Functions

| • llOrd | Convert a character into an ordinal |  |  |  |
| --- | --- | --- | --- | --- |
| • llHash | Calculate a 32bit hash for a string |  |  |  |

### Articles

<!-- /wiki-source -->
