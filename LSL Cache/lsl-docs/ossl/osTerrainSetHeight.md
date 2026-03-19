---
name: "osTerrainSetHeight"
category: "function"
type: "function"
language: "OSSL"
description: "DEPRECATED. Use osSetTerrainHeight instead."
signature: "integer osTerrainSetHeight(integer x, integer y, float val)"
return_type: "integer"
threat_level: "High"
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osTerrainSetHeight"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

DEPRECATED. Use osSetTerrainHeight instead.

## Syntax

```lsl
integer osTerrainSetHeight(integer x, integer y, float val)
```

## Parameters

| Type | Name |
|------|------|
| `integer` | `x` |
| `integer` | `y` |
| `float` | `val` |

## Return Value

`integer`

## Timing, Energy and Permissions

- **Threat Level:** High
- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osTerrainSetHeight](https://opensimulator.org/wiki/osTerrainSetHeight)
