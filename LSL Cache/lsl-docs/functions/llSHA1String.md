---
name: "llSHA1String"
category: "function"
type: "function"
language: "LSL"
description: "Returns a string of 40 hex characters that is the SHA-1 security hash of src."
signature: "string llSHA1String(string src)"
return_type: "string"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llSHA1String'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llsha1string"]
---

Returns a string of 40 hex characters that is the SHA-1 security hash of src.


## Signature

```lsl
string llSHA1String(string src);
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

- [SL Wiki](https://wiki.secondlife.com/wiki/llSHA1String)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llSHA1String) — scraped 2026-03-18_

Returns a string of 40 hex characters that is the  SHA-1 security hash of src.

## Caveats

There's no way to input a zero-byte value into this function, nor any byte value from 128-255, therefore it's currently broken for many purposes (like HMAC-SHA1). The reason is because LSL strings cannot have a unicode null character (U+0000) in them, and LSL has no escape code for the null character (many programming languages use \0 but LSL does not have this feature). llEscapeURL("%00") yields an empty string. As well, inside this function, each character with a Unicode integer value over U+0127 / 007F are dealt with in UTF-8 fashion: in the hex values, 0xC2 is appended to the byte value (hence 0x0080-0x00FF become 0xC280-0xC2FF inside the llSHA1String() routine). A JIRA has been filed for this.

## Examples

```lsl
llSay(0, llSHA1String("Hello, Avatar!")); // returns 2E73318E547AF1B28CC0C96F95DDC9B1EE906B8D
```

#### Linux Example

```lsl
$ echo -n 'Hello, Avatar!' | openssl sha1
2E73318E547AF1B28CC0C96F95DDC9B1EE906B8D
```

## See Also

### Functions

- llMD5String
- llSHA256String

### Articles

- SHA-1

<!-- /wiki-source -->
