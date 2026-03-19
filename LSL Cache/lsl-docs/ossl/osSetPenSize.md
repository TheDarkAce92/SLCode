---
name: "osSetPenSize"
category: "function"
type: "function"
language: "OSSL"
description: "Sets the pen size to a square of penSize pixels by penSize pixels. If penSize is an odd number, the pen will be exactly centered on the coordinates provided in the various drawing commands."
signature: "string osSetPenSize(string drawList, integer penSize)"
return_type: "string"
threat_level: ""
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osSetPenSize"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Sets the pen size to a square of penSize pixels by penSize pixels. If penSize is an odd number, the pen will be exactly centered on the coordinates provided in the various drawing commands.

## Syntax

```lsl
string osSetPenSize(string drawList, integer penSize)
```

## Parameters

| Type | Name |
|------|------|
| `string` | `drawList` |
| `integer` | `penSize` |

## Return Value

`string`

## Timing, Energy and Permissions

- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osSetPenSize](https://opensimulator.org/wiki/osSetPenSize)
