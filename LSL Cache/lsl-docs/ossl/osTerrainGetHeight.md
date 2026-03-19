---
name: "osTerrainGetHeight"
category: "function"
type: "function"
language: "OSSL"
description: "DEPRECATED. Use osGetTerrainHeight instead."
signature: "float osTerrainGetHeight(integer x, integer y)"
return_type: "float"
threat_level: ""
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osTerrainGetHeight"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

DEPRECATED. Use osGetTerrainHeight instead.

## Syntax

```lsl
float osTerrainGetHeight(integer x, integer y)
```

## Parameters

| Type | Name |
|------|------|
| `integer` | `x` |
| `integer` | `y` |

## Return Value

`float`

## Timing, Energy and Permissions

- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osTerrainGetHeight](https://opensimulator.org/wiki/osTerrainGetHeight)
