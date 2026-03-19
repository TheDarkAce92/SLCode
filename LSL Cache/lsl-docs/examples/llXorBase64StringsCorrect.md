---
name: "llXorBase64StringsCorrect"
category: "example"
type: "example"
language: "LSL"
description: "Correctly performs an exclusive or on two Base 64 strings.Returns a string that is a Base64 XOR of str1 and str2."
wiki_url: "https://wiki.secondlife.com/wiki/LlXorBase64StringsCorrect"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

/LSL


XorBase64StringsCorrectllXorBase64StringsCorrect

***Deprecated** (This function has been deprecated, please use llXorBase64 instead.)* - 1 Summary - 2 Caveats - 3 Examples - 4 Deep Notes - 4.1 Signature ## Summary 1/2 Bugs  Function: string **llXorBase64StringsCorrect**( string str1, string str2 );

0.0

Forced Delay

10.0

Energy

Correctly performs an exclusive or on two Base 64 strings.Returns a string that is a Base64 XOR of str1 and str2.

• string

str1

–

Base64 string

• string

str2

–

Base64 string

str2 repeats if it is shorter than str1. If the inputs are not Base64 strings the result will be erratic.

## Caveats

- This function has been deprecated, please use llXorBase64 instead.
- During the conversion to a byte array the last `(bitcount % 8)` are discarded from both str1 and str2. See Implementation for details.
- Considers any null encountered in str2 to mark the end of str2.

## Examples

## Deep Notes

#### Signature

```lsl
function string llXorBase64StringsCorrect( string str1, string str2 );
```