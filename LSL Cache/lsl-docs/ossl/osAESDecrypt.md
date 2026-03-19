---
name: "osAESDecrypt"
category: "function"
type: "function"
language: "OSSL"
description: "Decrypt an encrypted text using osAESEncrypt() and the same Key (secret) used in the encryption. Returns the decrypted text."
signature: "string osAESDecrypt(string secret, string encryptedText)"
return_type: "string"
threat_level: ""
energy_cost: ""
sleep_time: ""
wiki_url: "https://opensimulator.org/wiki/osAESDecrypt"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-18"
last_updated: "2026-03-19"
---

Decrypt an encrypted text using osAESEncrypt() and the same Key (secret) used in the encryption. Returns the decrypted text.

## Syntax

```lsl
string osAESDecrypt(string secret, string encryptedText)
```

## Parameters

| Type | Name |
|------|------|
| `string` | `secret` |
| `string` | `encryptedText` |

## Return Value

`string`

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osAESDecrypt](https://opensimulator.org/wiki/osAESDecrypt)
