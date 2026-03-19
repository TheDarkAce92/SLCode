---
name: "llXorBase64StringsCorrect"
category: "function"
type: "function"
language: "LSL"
description: 'Correctly performs an exclusive or on two Base 64 strings.Returns a string that is a Base64 XOR of str1 and str2.

str2 repeats if it is shorter than str1. If the inputs are not Base64 strings the result will be erratic.'
signature: "string llXorBase64StringsCorrect(string str1, string str2)"
return_type: "string"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llXorBase64StringsCorrect'
deprecated: "true"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
---

Correctly performs an exclusive or on two Base 64 strings.Returns a string that is a Base64 XOR of str1 and str2.

str2 repeats if it is shorter than str1. If the inputs are not Base64 strings the result will be erratic.


## Signature

```lsl
string llXorBase64StringsCorrect(string str1, string str2);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `string` | `str1` | Base64 string |
| `string` | `str2` | Base64 string |


## Return Value

Returns `string`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llXorBase64StringsCorrect)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llXorBase64StringsCorrect) — scraped 2026-03-18_

Correctly performs an exclusive or on two Base 64 strings.Returns a string that is a Base64 XOR of str1 and str2.

## Caveats

- This function has been deprecated, please use llXorBase64 instead.
- During the conversion to a byte array the last `(bitcount % 8)` are discarded from both str1 and str2. See Implementation for details.
- Considers any null encountered in str2 to mark the end of str2.

<!-- /wiki-source -->
