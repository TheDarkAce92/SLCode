---
name: "llStringLength"
category: "function"
type: "function"
language: "LSL"
description: "Returns the number of characters (not bytes) in a string"
wiki_url: "https://wiki.secondlife.com/wiki/llStringLength"
first_fetched: "2026-03-09"
last_updated: "2026-03-09"
signature: "integer llStringLength(string str)"
parameters:
  - name: "str"
    type: "string"
    description: "The string to measure"
return_type: "integer"
energy_cost: "0.0"
sleep_time: "0.0"
patterns: ["llstringlength"]
deprecated: "false"
---

# llStringLength

```lsl
integer llStringLength(string str)
```

Returns the number of **characters** in `str` (not bytes — multibyte UTF-8 characters count as 1).

## Return Value

`integer` — character count. Empty string returns 0.

## Caveats

- Returns character count, not byte count. Some functions limit by bytes (e.g., `llSetText` limits to 254 bytes, not 254 characters).
- Index of last character is `llStringLength(str) - 1`, not `llStringLength(str)`.

## Example

```lsl
default
{
    state_entry()
    {
        string s = "Hello!";
        integer len = llStringLength(s);  // 6
        llOwnerSay("Length: " + (string)len);
        llOwnerSay("Last char: " + llGetSubString(s, -1, -1));  // "!"
    }
}
```

## See Also

- `llGetSubString` — extract substring
- `llSubStringIndex` — find substring position
- `llDeleteSubString` — remove substring


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llStringLength) — scraped 2026-03-18_

Returns an integer that is the number of characters in str.

## Caveats

- The index of the last character is not equal to the string length.

  - Character indexes start at zero (the index of the first character is zero).
- llStringLength returns the number of characters - not bytes - in the string.

  - Some functions that accept strings are limited to bytes, not characters.
  - LSL-2 uses UTF-8 strings and Mono uses UTF-16; both support multibyte characters.
  - To get the number of bytes in a string instead, use the example snippet on llStringToBase64 (there is no native LSL function to do this).

## Examples

```lsl
// assumptions:
//    object name: LSLWiki
//    script name: _lslwiki

default
{
    state_entry()
    {
        string HowLongAmI = "123";
        integer strlen = llStringLength(HowLongAmI);
        llOwnerSay( "'" + HowLongAmI + "' has " +(string) strlen + " characters.");
        // The owner of object LSLWiki will hear
        // LSLWiki: '123' has 3 characters.
    }
}
```

## See Also

### Functions

- llGetListLength

<!-- /wiki-source -->
