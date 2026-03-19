---
name: "LlComputeHash"
category: "example"
type: "example"
language: "LSL"
description: "Returns a string hex-encoded hash digest of message using cryptographic algorithm"
wiki_url: "https://wiki.secondlife.com/wiki/LlComputeHash"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

/LSL


ComputeHashllComputeHash

- 1 Summary
- 2 Examples
- 3 See Also

  - 3.1 Functions
- 4 Deep Notes

  - 4.1 Signature

## Summary

 Function: string **llComputeHash**( string message, string algorithm );

0.0

Forced Delay

10.0

Energy

Returns a string hex-encoded hash digest of **message** using cryptographic **algorithm**

• string

message

• string

algorithm

Supported values of **algorithm** are **md5**, **md5_sha1**, **sha1**, **sha224**, **sha256**, **sha384**, **sha512**.

## Examples

```lsl
default
{
    state_entry()
    {
        llOwnerSay("Ready");
    }

    touch_start(integer touch_count)
    {
        string message = "your-test-message-here";

        list algorithms = ["md5", "md5_sha1", "sha1", "sha224", "sha256", "sha384", "sha512" ];

        integer num_algorithms = llGetListLength(algorithms);
        llOwnerSay("message='" + message + "'");

        integer i = 0;
        for (i = 0; i < num_algorithms; ++i)
        {
            string algorithm = llList2String(algorithms, i);
            string hash = llComputeHash(message, algorithm);
            llOwnerSay(algorithm + " : " + hash);
        }
    }
}
```

## See Also

### Functions

•

llSignRSA

•

llVerifyRSA

•

llHMAC

•

llSHA1String

•

llSHA256String

•

llMD5String

## Deep Notes

#### Signature

```lsl
function string llComputeHash( string message, string algorithm );
```