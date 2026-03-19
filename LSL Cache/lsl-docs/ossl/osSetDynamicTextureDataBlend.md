---
name: "osSetDynamicTextureDataBlend"
category: "function"
type: "function"
language: "OSSL"
description: "Generate a dynamic texture alpha blended from a given draw string, returns the texture UUID, applies to all faces."
signature: "string osSetDynamicTextureDataBlend(string dynamicID, string contentType, string data, string extraParams, integer timer, integer alpha)"
return_type: "string"
threat_level: "VeryLow"
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osSetDynamicTextureDataBlend"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Generate a dynamic texture alpha blended from a given draw string, returns the texture UUID, applies to all faces.

## Syntax

```lsl
string osSetDynamicTextureDataBlend(string dynamicID, string contentType, string data, string extraParams, integer timer, integer alpha)
```

## Parameters

| Type | Name |
|------|------|
| `string` | `dynamicID` |
| `string` | `contentType` |
| `string` | `data` |
| `string` | `extraParams` |
| `integer` | `timer` |
| `integer` | `alpha` |

## Return Value

`string`

## Timing, Energy and Permissions

- **Threat Level:** VeryLow
- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osSetDynamicTextureDataBlend](https://opensimulator.org/wiki/osSetDynamicTextureDataBlend)
