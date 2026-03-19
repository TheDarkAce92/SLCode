---
name: "llSHA256String"
category: "function"
type: "function"
language: "LSL"
description: "Returns a string of 64 hex characters that is the SHA-256 security hash of src."
signature: "string llSHA256String(string src)"
return_type: "string"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llSHA256String'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
---

Returns a string of 64 hex characters that is the SHA-256 security hash of src.


## Signature

```lsl
string llSHA256String(string src);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `string` | `src` |  |


## Return Value

Returns `string`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llSHA256String)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llSHA256String) — scraped 2026-03-18_

Returns a string of 64 hex characters that is the  SHA-256 security hash of src.

## Caveats

There's no way to input a zero-byte value into this function, nor any byte value from 128-255, therefore it's currently broken for many purposes (like HMAC-SHA1). The reason is because LSL strings cannot have a unicode null character (U+0000) in them, and LSL has no escape code for the null character (many programming languages use \0 but LSL does not have this feature). llEscapeURL("%00") yields an empty string. As well, inside this function, each character with a Unicode integer value over U+0127 / 007F are dealt with in UTF-8 fashion: in the hex values, 0xC2 is prepended to the byte value (hence 0x0080-0x00FF become 0xC280-0xC2FF inside the llSHA256String() routine).

## Examples

```lsl
llSay(0, llSHA256String("Hello, Avatar!")); // returns 3a9f9d2e4360319a62139d19bd425c16fb8439b832d74d5221ca75b54c35b4f2
```

#### Linux Example

```lsl
$ echo -n 'Hello, Avatar!' | openssl sha256
3a9f9d2e4360319a62139d19bd425c16fb8439b832d74d5221ca75b54c35b4f2
```

## See Also

### Functions

- llMD5String
- llSHA1String

### Articles

- SHA-2

<!-- /wiki-source -->
