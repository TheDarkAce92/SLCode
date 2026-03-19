---
name: "osAESEncrypt"
category: "function"
type: "function"
language: "OSSL"
description: "Encrypt a plain text using AES-256-CBC Symmetric Algorithm Key (secret) and a random Initialization Vector (IV). Returns the Hex string of the IV bytes and the Hex string of the encrypted text bytes separated with (:)."
signature: "string osAESEncrypt(string secret, string plainText)"
return_type: "string"
threat_level: ""
energy_cost: ""
sleep_time: ""
wiki_url: "https://opensimulator.org/wiki/osAESEncrypt"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-18"
last_updated: "2026-03-19"
---

Encrypt a plain text using AES-256-CBC Symmetric Algorithm Key (secret) and a random Initialization Vector (IV). Returns the Hex string of the IV bytes and the Hex string of the encrypted text bytes separated with (:).

## Syntax

```lsl
string osAESEncrypt(string secret, string plainText)
```

## Parameters

| Type | Name |
|------|------|
| `string` | `secret` |
| `string` | `plainText` |

## Return Value

`string`

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osAESEncrypt](https://opensimulator.org/wiki/osAESEncrypt)
