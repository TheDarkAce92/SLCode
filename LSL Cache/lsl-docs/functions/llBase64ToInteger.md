---
name: "llBase64ToInteger"
category: "function"
type: "function"
language: "LSL"
description: "Returns an integer that is str Base64 decoded as a big endian integer."
signature: "integer llBase64ToInteger(string str)"
return_type: "integer"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llBase64ToInteger'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llbase64tointeger"]
---

Returns an integer that is str Base64 decoded as a big endian integer.


## Signature

```lsl
integer llBase64ToInteger(string str);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `string` | `str` | Base64 string |


## Return Value

Returns `integer`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llBase64ToInteger)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llBase64ToInteger) — scraped 2026-03-18_

Returns an integer that is str Base64 decoded as a big endian integer.

## Caveats

- If str contains fewer than 6 characters, any incomplete least-significant bytes of the integer are set to 0.

  - For example, the Base64 value `"qqqqqq=="` corresponds to the hexadecimal value `0xAAAAAAAA`. If the padding "=" characters and the last "q" are dropped, there are 5*6=30 bits remaining and those can form only 3 full bytes (24 bits). The result is `0xAAAAAA00`.
  - The Base64 value `"qqqq"` has 4*6=24 bits available, which is enough for the same 3 full bytes. The result is also `0xAAAAAA00`.
  - Similarly, 3-character Base64 has 18 bits, enough for 2 bytes, and 2-character Base64 has 12 bits, enough for one byte.
  - Finally, single-character Base64 has only 6 bits and thus no complete bytes, and the result is always zero.
- Returns zero if str is longer than 8 characters.

## Examples

```lsl
integer value = llBase64ToInteger("3q0AAA==");

// writes out -559087616
llOwnerSay((string)value);
```

## See Also

### Functions

- llIntegerToBase64

### Articles

- Base64

<!-- /wiki-source -->
