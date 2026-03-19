---
name: "LlSHA1String"
category: "example"
type: "example"
language: "LSL"
description: "The SHA-1 hashing algorithm is considered broken but the attacks are largely still theoretical and not very practical. Consider the more secure llSHA256String.  Comparison of SHA functions"
wiki_url: "https://wiki.secondlife.com/wiki/LlSHA1String"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

/LSL


SHA1StringllSHA1String

**Security Warning!**

The SHA-1 hashing algorithm is considered broken but the attacks are largely still theoretical and not very practical. Consider the more secure llSHA256String.  [Comparison of SHA functions](https://en.wikipedia.org/wiki/SHA-1%23Comparison_of_SHA_functions)

- 1 Summary
- 2 Specification
- 3 Caveats
- 4 Examples

  - 4.1 Linux Example
- 5 See Also

  - 5.1 Functions
  - 5.2 Articles
- 6 Deep Notes

  - 6.1 History
  - 6.2 Signature

## Summary

 Function: string **llSHA1String**( string src );

0.0

Forced Delay

10.0

Energy

Returns a string of 40 hex characters that is the  [SHA-1](https://en.wikipedia.org/wiki/SHA-1) security hash of src.

• string

src

## Specification

LSL strings are stored in the UTF-8 format.

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

•

llMD5String

•

llSHA256String

### Articles

•

SHA-1 (script implementation)

## Deep Notes

Prior to this, the only way to get the SHA-1 hash was to use the LSL SHA-1 port: SHA-1

#### History

- [SVN:1291 r98903 Trunk c:1.21.5.97417 s:1.24.9.98650](http://svn.secondlife.com/trac/linden/changeset/1291?new_path=%2F#file13) Initial introduction.
- [SVN:1298 r99021 Branch:OpenAL c:1.21.5.97417 s:1.24.9.98650](http://svn.secondlife.com/trac/linden/changeset/1298?new_path=branches/openal/indra/lscript/lscript_library/lscript_library.cpp)

Integration into OpenAL branch.

- Date of Release 2008-10-31

#### Signature

```lsl
function string llSHA1String( string src );
```