---
name: "osSetFontSize"
category: "function"
type: "function"
language: "OSSL"
description: "Sets the size of the font used by subsequent osDrawTextText() calls. The fontSize parameter represents the font height in points."
signature: "string osSetFontSize(string drawList, integer fontSize)"
return_type: "string"
threat_level: ""
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osSetFontSize"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Sets the size of the font used by subsequent osDrawTextText() calls. The fontSize parameter represents the font height in points.

## Syntax

```lsl
string osSetFontSize(string drawList, integer fontSize)
```

## Parameters

| Type | Name |
|------|------|
| `string` | `drawList` |
| `integer` | `fontSize` |

## Return Value

`string`

## Timing, Energy and Permissions

- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osSetFontSize](https://opensimulator.org/wiki/osSetFontSize)
