---
name: "llStringToBase64"
category: "function"
type: "function"
language: "LSL"
description: 'Returns the string Base64 representation of the str interpreted as an UTF-8 byte sequence

If extra bits are needed to complete the last base64 symbol, those extra bits will be zero.
To go in the other direction, use llBase64ToString.'
signature: "string llStringToBase64(string str)"
return_type: "string"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llStringToBase64'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llstringtobase64"]
---

Returns the string Base64 representation of the str interpreted as an UTF-8 byte sequence

If extra bits are needed to complete the last base64 symbol, those extra bits will be zero.
To go in the other direction, use llBase64ToString.


## Signature

```lsl
string llStringToBase64(string str);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `string` | `str` |  |


## Return Value

Returns `string`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llStringToBase64)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llStringToBase64) — scraped 2026-03-18_

Returns the string Base64 representation of the str interpreted as an UTF-8 byte sequence

## Examples

```lsl
integer getStringBytes(string msg) {
    return (llStringLength((string)llParseString2List(llStringToBase64(msg), ["="], [])) * 3) >> 2;
}
```

## See Also

### Functions

- llBase64ToString
- llBase64ToInteger
- llIntegerToBase64
- llXorBase64

<!-- /wiki-source -->
