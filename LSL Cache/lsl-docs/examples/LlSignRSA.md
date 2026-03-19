---
name: "LlSignRSA"
category: "example"
type: "example"
language: "LSL"
description: "Returns a string that is the  Base64-encoded  RSA signature of msg when using hash algorithm algorithm and secret key private_key. Can be paired with llVerifyRSA to pass verifiable messages."
wiki_url: "https://wiki.secondlife.com/wiki/LlSignRSA"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

/LSL


SignRSAllSignRSA

- 1 Summary
- 2 Examples
- 3 Notes
- 4 See Also

  - 4.1 Functions
  - 4.2 Articles
- 5 Deep Notes

  - 5.1 Signature

## Summary

 Function: string **llSignRSA**( string private_key, string msg, string algorithm );

0.0

Forced Delay

10.0

Energy

Returns a string that is the  [Base64-encoded](https://en.wikipedia.org/wiki/Base64)  [RSA](https://en.wikipedia.org/wiki/RSA_(cryptosystem)) signature of **msg** when using hash algorithm **algorithm** and secret key **private_key**.  Can be paired with llVerifyRSA to pass verifiable messages.

• string

private_key

• string

msg

• string

algorithm

This function supports sha1, sha224, sha256, sha384, sha512 for **algorithm**.

## Examples

```lsl
// Generate an signature, then immediately verify if it is valid.

default
{
    state_entry()
    {
        // Key pair generated using LibreSSL 3.3.6
        // For demonstration purposes only
        string private_key = "-----BEGIN RSA PRIVATE KEY-----
MIIEogIBAAKCAQEAqxXSIhFHzYO9UNEUvMMXwhB4vf32fPirCxxV/w4m88jKPmFH
QQe9DOwj7illmvg+81vzBNGt+uNYy/2zFegUtwvxKCEioeoanRpPcvn9r/d/kXad
WL/DyKJwHbF1EtTfPAZSl6ZIBIYis8HQ/RAln3olS705AmCKBRkbz3cZ+dTzqX1v
7ohqqPPoCaXQFgLTMYnqU8ZTsq1Sl8BwKK735HPmKLCEjZaMn97lvzGHufY/JdRs
dwdRHqKnpe2w2c0AzNpQtjoRCnPtj7cFgCeztjAcbdtuS8ipJTEIuBLWHCVVXIlD
DQ6jJvIEW7tt+6kde/NUskRASd7Rtoy5AeS7cwIDAQABAoIBABwvix/7stWj55Oh
7oWuqoJZTlsWtP4fxaYd8/kCLt6o7NDcG+4VxUqUuNKq1UdzsINNWbsohD46KE3r
LQ7l3kvN1twioV8Ff370b7RkhSvxXX3sib2uUiYCxO/PZZdFpMVx0TeUuHauVpdA
zhpzB4+/gtd4hCTlHLf8S/2hBJGJA9e37Vo3MqXh43QRFTD8pgjb0mUWa4xJeZlz
3vGmQl0uMS04wX+r7Pq1HKs7gk93WeLrNhEQgRwUPgumrMGHey9eF1kDb14m3O7Z
qWU7MWWME2lxcUV0YT/iHPfvStvLHiEdi1z2TGKkMmlHX7RGpk7Js5GGQfeEKEsv
ihXuFmkCgYEA2y6V2+HCmViA8V1qY907z5dvG3ar9zbm3qfcJDJFoNOzDZNU0NRJ
eZu/LhwTHW7PArAuWhxh7ENu9Bhl5FjvMuyqrMPud1Tf0GsrYKQJITgbW6IC6w/N
a+2ZMm6VDCztS5MNNmWRCTTEecd4lnPLfyX9XYfUvUovzv5mM65Hzl0CgYEAx9Ly
RR1tkjgiIJHmpv95MkaHg4O4NZT0eiyykRz1qENESZOtJ00l+/p4vZSOdQjwPl+q
vjMhlZc9a2292UEy3BsBOPB/nJybLXBDFa0KYUCc3/aHGSgq+ZbUKNhdBq2c83hb
Dpw2ajHluLtXO7D4kDGvEDLPN+/19NElI6EL9A8CgYAVRu5xS/cyH69UvvbG/wEB
Y/f7OIf1FbVPxAfQ07iCpkppdPX018bSMVZbyYnpf4pE/olhYgP3hYxN0diCVEfU
L7lZ0CNkHi8j8mNhnErumJ2/RXj3DK+qXIRUqvt5FRtsDLhpoW508FRqZfzEzjTh
APUZkUgLoBoIBBYzyiVaWQKBgD3GvHmbmHVc/0f8c0drsedWIK0K+tct3ssqqGXu
gw/rA+CPVDfTRQv6qntJwyTxh3xxDRNSMW7S2/0rZ0cUPgoIGz+kMn+TdvH8Q/Ee
lxfr5tPinm+rmGWjOKIMCe53nA81RUlmB/iaxn9vA5ADrUS+53Vlj+SmPe7a/dVf
A5gHAoGAbS4sMlUkUd449PT33rqx26aNKkKLI9PLxgWE7YBfwzaUkG0MBryQqP5L
aIY2a+8ZvUeHxmY0oQfPQkH5KKbAaC0ozaXf+3qX0Gfkt8vxsh41ON5esr0tfcm2
BFdQrdBOACefo2kOFfdMSP6KWKI3HZMJAr9SDcAiL23IQZ/wl/c=
-----END RSA PRIVATE KEY-----";

        string public_key = "-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAqxXSIhFHzYO9UNEUvMMX
whB4vf32fPirCxxV/w4m88jKPmFHQQe9DOwj7illmvg+81vzBNGt+uNYy/2zFegU
twvxKCEioeoanRpPcvn9r/d/kXadWL/DyKJwHbF1EtTfPAZSl6ZIBIYis8HQ/RAl
n3olS705AmCKBRkbz3cZ+dTzqX1v7ohqqPPoCaXQFgLTMYnqU8ZTsq1Sl8BwKK73
5HPmKLCEjZaMn97lvzGHufY/JdRsdwdRHqKnpe2w2c0AzNpQtjoRCnPtj7cFgCez
tjAcbdtuS8ipJTEIuBLWHCVVXIlDDQ6jJvIEW7tt+6kde/NUskRASd7Rtoy5AeS7
cwIDAQAB
-----END PUBLIC KEY-----";

        // Supported algorithims for llSignRSA() include:
        // sha1, sha224, sha256, sha384, sha512

        string algorithm = "sha1";
        string msg = "Hello, Avatar!";

        string signature = llSignRSA(private_key, msg, algorithm);

        // For the given private_key/msg/algorithm, expect the signature
        // to resemble 'SgqafXI/M70FJr5th0VR3U36L...O76Bg=='
        llSay(0, "RSA signature of message '" + msg + "' using algorithm "
            +  algorithm + " is " + signature);

        /* Now, imagine that msg and signature were transmitted to another
        script over chat or similar.  The other script has access to public_key
        but not to private_key, but can still verify the authenticity of msg
        using the signature. */

        integer valid_signature = llVerifyRSA(public_key, msg, signature, algorithm);

        if(valid_signature)
        {
            llSay(0, "Signature verified successfully!");
        }
        else
        {
            llSay(0, "Signature verification failed!");
        }
    }
}
```

## Notes

- If you do not have an RSA key you wish to use already, you can easily generate an RSA key using [this generator.](https://cryptotools.net/rsagen)

## See Also

### Functions

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

### Articles

•

JSON Web Token in LSL

## Deep Notes

#### Signature

```lsl
function string llSignRSA( string private_key, string msg, string algorithm );
```