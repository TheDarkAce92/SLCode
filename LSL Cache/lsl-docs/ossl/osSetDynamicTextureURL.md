---
name: "osSetDynamicTextureURL"
category: "function"
type: "function"
language: "OSSL"
description: "Generate a dynamic texture from a given URL, returns the texture UUID, applies to all faces."
signature: "string osSetDynamicTextureURL(string dynamicID, string contentType, string url, string extraParams, integer timer)"
return_type: "string"
threat_level: "VeryHigh"
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osSetDynamicTextureURL"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Generate a dynamic texture from a given URL, returns the texture UUID, applies to all faces.

## Syntax

```lsl
string osSetDynamicTextureURL(string dynamicID, string contentType, string url, string extraParams, integer timer)
```

## Parameters

| Type | Name |
|------|------|
| `string` | `dynamicID` |
| `string` | `contentType` |
| `string` | `url` |
| `string` | `extraParams` |
| `integer` | `timer` |

## Return Value

`string`

## Timing, Energy and Permissions

- **Threat Level:** VeryHigh
- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osSetDynamicTextureURL](https://opensimulator.org/wiki/osSetDynamicTextureURL)
