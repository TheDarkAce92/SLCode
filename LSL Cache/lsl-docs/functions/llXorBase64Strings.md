---
name: "llXorBase64Strings"
category: "function"
type: "function"
language: "LSL"
description: 'Returns a string that is a Base64 string of s1 xor'ed with s2.

s2 repeats if it is shorter than s1. Retained for backwards compatibility.'
signature: "string llXorBase64Strings(string str1, string str2)"
return_type: "string"
sleep_time: "0.3"
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llXorBase64Strings'
deprecated: "true"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
---

Returns a string that is a Base64 string of s1 xor'ed with s2.

s2 repeats if it is shorter than s1. Retained for backwards compatibility.


## Signature

```lsl
string llXorBase64Strings(string str1, string str2);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `string` | `str1` | Base64 string |
| `string` | `str2` | Base64 string |


## Return Value

Returns `string`.


## Caveats

- Forced delay: **0.3 seconds** — the script sleeps after each call.
- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llXorBase64Strings)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llXorBase64Strings) — scraped 2026-03-18_

Returns a string that is a Base64 string of s1 xor'ed with s2.

## Caveats

- This function causes the script to sleep for 0.3 seconds.
- This function has been deprecated, please use llXorBase64 instead.
- **Incorrectly performs an exclusive or on two Base64 strings and returns a Base64 string**

  - Use llXorBase64 instead.

## See Also

### Functions

- llXorBase64

<!-- /wiki-source -->
