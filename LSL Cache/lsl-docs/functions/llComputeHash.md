---
name: "llComputeHash"
category: "function"
type: "function"
language: "LSL"
description: 'Returns a string hex-encoded hash digest of message using cryptographic algorithm

Supported values of algorithm are md5, md5_sha1, sha1, sha224, sha256, sha384, sha512.'
signature: "string llComputeHash(string data, string algorithm)"
return_type: "string"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llComputeHash'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
---

Returns a string hex-encoded hash digest of message using cryptographic algorithm

Supported values of algorithm are md5, md5_sha1, sha1, sha224, sha256, sha384, sha512.


## Signature

```lsl
string llComputeHash(string data, string algorithm);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `string` | `message` |  |
| `string` | `algorithm` |  |


## Return Value

Returns `string`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llComputeHash)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llComputeHash) — scraped 2026-03-18_

Returns a string hex-encoded hash digest of message using cryptographic algorithm

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

- llSignRSA
- llVerifyRSA
- llHMAC
- llSHA1String
- llSHA256String
- llMD5String

<!-- /wiki-source -->
