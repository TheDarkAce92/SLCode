---
name: "osSHA256"
category: "function"
type: "function"
language: "OSSL"
description: "Returns the SHA256 representation of the input string."
signature: "string osSHA256(string input)"
return_type: "string"
threat_level: ""
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osSHA256"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Returns the SHA256 representation of the input string.

## Syntax

```lsl
string osSHA256(string input)
```

## Parameters

| Type | Name |
|------|------|
| `string` | `input` |

## Return Value

`string`

## Timing, Energy and Permissions

- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osSHA256](https://opensimulator.org/wiki/osSHA256)
