---
name: "LlHMAC"
category: "example"
type: "example"
language: "LSL"
description: "Returns a string that is the  Base64-encoded  HMAC hash of msg when using hash algorithm algorithm and secret key private_key."
wiki_url: "https://wiki.secondlife.com/wiki/LlHMAC"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

/LSL


HMACllHMAC

- 1 Summary
- 2 Examples
- 3 See Also

  - 3.1 Functions
- 4 Deep Notes

  - 4.1 Signature

## Summary

 Function: string **llHMAC**( string private_key, string msg, string algorithm );

0.0

Forced Delay

10.0

Energy

Returns a string that is the  [Base64-encoded](https://en.wikipedia.org/wiki/Base64)  [HMAC](https://en.wikipedia.org/wiki/HMAC) hash of **msg** when using hash algorithm **algorithm** and secret key **private_key**.

• string

private_key

• string

msg

• string

algorithm

This function supports md5, sha1, sha224, sha256, sha384, sha512 for **algorithm**.

## Examples

```lsl
default
{
    state_entry()
    {
        string private_key = "secret key";

        // Supported algorithims for llHMAC() include:
        // md5, sha1, sha224, sha256, sha384, sha512

        string algorithm = "sha1";
        string msg = "Hello, Avatar!";

        string digest = llHMAC(private_key, msg, algorithm);

        // For the given private_key/msg/algorithm, expect the HMAC
        // digest to be 'ffCDntkagRO5mIEtd2tYzM2Bg8I='
        llSay(0, "HMAC digest of message '" + msg + "' using algorithm "
            +  algorithm + " is " + digest);
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

llSHA1String

•

llSHA256String

•

llMD5String

## Deep Notes

#### Signature

```lsl
function string llHMAC( string private_key, string msg, string algorithm );
```