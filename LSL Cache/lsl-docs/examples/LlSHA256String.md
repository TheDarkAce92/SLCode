---
name: "LlSHA256String"
category: "example"
type: "example"
language: "LSL"
description: "Returns a string of 64 hex characters that is the  SHA-256 security hash of src."
wiki_url: "https://wiki.secondlife.com/wiki/LlSHA256String"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

/LSL


SHA256StringllSHA256String

- 1 Summary
- 2 Specification
- 3 Caveats
- 4 Examples

  - 4.1 Linux Example
- 5 See Also

  - 5.1 Functions
  - 5.2 Articles
- 6 Deep Notes

  - 6.1 Signature

## Summary

 Function: string **llSHA256String**( string src );

0.0

Forced Delay

10.0

Energy

Returns a string of 64 hex characters that is the  [SHA-256](https://en.wikipedia.org/wiki/SHA-2) security hash of src.

• string

src

## Specification

LSL strings are stored in the UTF-8 format.

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

•

llMD5String

•

llSHA1String

### Articles

•

SHA-2

## Deep Notes

Prior to this, the only way to get the SHA-256 hash was to use the LSL SHA-256 port: SHA-2

#### Signature

```lsl
function string llSHA256String( string src );
```