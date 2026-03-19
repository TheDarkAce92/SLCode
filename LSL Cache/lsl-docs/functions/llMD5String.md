---
name: "llMD5String"
category: "function"
type: "function"
language: "LSL"
description: 'Returns a string of 32 hex characters that is the MD5 checksum of src with a salt of ':'+nonce.'
signature: "string llMD5String(string src, integer nonce)"
return_type: "string"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llMD5String'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llmd5string"]
---

Returns a string of 32 hex characters that is the MD5 checksum of src with a salt of ":"+nonce.


## Signature

```lsl
string llMD5String(string src, integer nonce);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `string` | `src` |  |
| `integer` | `nonce` |  |


## Return Value

Returns `string`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llMD5String)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llMD5String) — scraped 2026-03-18_

Returns a string of 32 hex characters that is the  MD5 checksum of src with a  salt of ":"+nonce.

## Examples

```lsl
llSay(0, llMD5String("Hello, Avatar!", 0)); // returns 112abd47ceaae1c05a826828650434a6
```

#### Linux Example

```lsl
$ echo -n 'Hello, Avatar!:0' | openssl md5
112abd47ceaae1c05a826828650434a6
```

## See Also

### Functions

- llSHA1String
- llSHA256String

<!-- /wiki-source -->
