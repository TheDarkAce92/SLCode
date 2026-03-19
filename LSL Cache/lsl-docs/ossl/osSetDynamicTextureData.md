---
name: "osSetDynamicTextureData"
category: "function"
type: "function"
language: "OSSL"
description: "Generate a dynamic texture from a given draw string, returns the texture UUID, applies to all faces."
signature: "string osSetDynamicTextureData(string dynamicID, string contentType, string data, string extraParams, integer timer)"
return_type: "string"
threat_level: "VeryLow"
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osSetDynamicTextureData"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Generate a dynamic texture from a given draw string, returns the texture UUID, applies to all faces.

## Syntax

```lsl
string osSetDynamicTextureData(string dynamicID, string contentType, string data, string extraParams, integer timer)
```

## Parameters

| Type | Name |
|------|------|
| `string` | `dynamicID` |
| `string` | `contentType` |
| `string` | `data` |
| `string` | `extraParams` |
| `integer` | `timer` |

## Return Value

`string`

## Timing, Energy and Permissions

- **Threat Level:** VeryLow
- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osSetDynamicTextureData](https://opensimulator.org/wiki/osSetDynamicTextureData)
