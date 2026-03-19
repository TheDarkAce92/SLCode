---
name: "LlMD5String"
category: "example"
type: "example"
language: "LSL"
description: "The MD5 hashing algorithm should not be used because it is too easy to generate collisions (two inputs which result in the same hash). http://www.kb.cert.org/vuls/id/836068"
wiki_url: "https://wiki.secondlife.com/wiki/LlMD5String"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

/LSL


MD5StringllMD5String

**Security Warning!**

The MD5 hashing algorithm should not be used because it is too easy to generate collisions (two inputs which result in the same hash). [http://www.kb.cert.org/vuls/id/836068](http://www.kb.cert.org/vuls/id/836068)

- 1 Summary
- 2 Specification
- 3 Examples

  - 3.1 Linux Example
- 4 See Also

  - 4.1 Functions
- 5 Deep Notes

  - 5.1 Signature

## Summary

 Function: string **llMD5String**( string src, integer nonce );

0.0

Forced Delay

10.0

Energy

Returns a string of 32 hex characters that is the  [MD5](https://en.wikipedia.org/wiki/MD5) checksum of src with a  [salt](https://en.wikipedia.org/wiki/salt_(cryptography)) of `":"+nonce`.

• string

src

• integer

nonce

## Specification

nonce is casted to string, then appended to src after a colon (`src + ":" + nonce`).  This is important to know if you are calculating a hash in another language and wish to compare with one calculated in LSL. It could be written as `MD5Hash(src + ":" + nonce)`

The character encoding used by llMD5String is the UTF-8 format.

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

•

llSHA1String

•

llSHA256String

## Deep Notes

#### Signature

```lsl
function string llMD5String( string src, integer nonce );
```