---
name: "osAESDecryptFrom"
category: "function"
type: "function"
language: "OSSL"
description: "Decrypt an encrypted text using osAESEncryptTo() and the same Key (secret) and Initialization Vector (ivString) used in the encryption. Returns the decrypted text."
signature: "string osAESDecryptFrom(string secret, string encryptedText, string ivString)"
return_type: "string"
threat_level: ""
energy_cost: ""
sleep_time: ""
wiki_url: "https://opensimulator.org/wiki/osAESDecryptFrom"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-18"
last_updated: "2026-03-19"
---

Decrypt an encrypted text using osAESEncryptTo() and the same Key (secret) and Initialization Vector (ivString) used in the encryption. Returns the decrypted text.

## Syntax

```lsl
string osAESDecryptFrom(string secret, string encryptedText, string ivString)
```

## Parameters

| Type | Name |
|------|------|
| `string` | `secret` |
| `string` | `encryptedText` |
| `string` | `ivString` |

## Return Value

`string`

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osAESDecryptFrom](https://opensimulator.org/wiki/osAESDecryptFrom)
