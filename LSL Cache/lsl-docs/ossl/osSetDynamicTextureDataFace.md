---
name: "osSetDynamicTextureDataFace"
category: "function"
type: "function"
language: "OSSL"
description: "Generate a dynamic texture from a given draw string, returns the texture UUID, applies to a given face."
signature: "string osSetDynamicTextureDataFace(string dynamicID, string contentType, string data, string extraParams, integer timer, integer face)"
return_type: "string"
threat_level: ""
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osSetDynamicTextureDataFace"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Generate a dynamic texture from a given draw string, returns the texture UUID, applies to a given face.

## Syntax

```lsl
string osSetDynamicTextureDataFace(string dynamicID, string contentType, string data, string extraParams, integer timer, integer face)
```

## Parameters

| Type | Name |
|------|------|
| `string` | `dynamicID` |
| `string` | `contentType` |
| `string` | `data` |
| `string` | `extraParams` |
| `integer` | `timer` |
| `integer` | `face` |

## Return Value

`string`

## Timing, Energy and Permissions

- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osSetDynamicTextureDataFace](https://opensimulator.org/wiki/osSetDynamicTextureDataFace)
