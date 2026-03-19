---
name: "llHMAC"
category: "function"
type: "function"
language: "LSL"
description: 'Returns a string that is the Base64-encoded HMAC hash of msg when using hash algorithm algorithm and secret key private_key.

This function supports md5, sha1, sha224, sha256, sha384, sha512 for algorithm.'
signature: "string llHMAC(string authkey, string message, string alg)"
return_type: "string"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llHMAC'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
---

Returns a string that is the Base64-encoded HMAC hash of msg when using hash algorithm algorithm and secret key private_key.

This function supports md5, sha1, sha224, sha256, sha384, sha512 for algorithm.


## Signature

```lsl
string llHMAC(string authkey, string message, string alg);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `string` | `private_key` |  |
| `string` | `msg` |  |
| `string` | `algorithm` |  |


## Return Value

Returns `string`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llHMAC)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llHMAC) — scraped 2026-03-18_

Returns a string that is the  Base64-encoded  HMAC hash of msg when using hash algorithm algorithm and secret key private_key.

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

- llSignRSA
- llVerifyRSA
- llSHA1String
- llSHA256String
- llMD5String

<!-- /wiki-source -->
