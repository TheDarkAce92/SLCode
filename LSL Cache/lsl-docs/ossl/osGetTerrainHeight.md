---
name: "osGetTerrainHeight"
category: "function"
type: "function"
language: "OSSL"
description: "Returns the height of terrain at a given x and y coordinate (meters)."
signature: "float osGetTerrainHeight(integer x, integer y)"
return_type: "float"
threat_level: ""
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osGetTerrainHeight"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Returns the height of terrain at a given x and y coordinate (meters).

## Syntax

```lsl
float osGetTerrainHeight(integer x, integer y)
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
- Reference: [https://opensimulator.org/wiki/osGetTerrainHeight](https://opensimulator.org/wiki/osGetTerrainHeight)
