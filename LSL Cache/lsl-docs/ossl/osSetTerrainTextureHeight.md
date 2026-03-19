---
name: "osSetTerrainTextureHeight"
category: "function"
type: "function"
language: "OSSL"
description: "Sets the texture low and high values for a given region corner."
signature: "void osSetTerrainTextureHeight(integer corner, float low, float high)"
return_type: "void"
threat_level: "High"
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osSetTerrainTextureHeight"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Sets the texture low and high values for a given region corner.

## Syntax

```lsl
void osSetTerrainTextureHeight(integer corner, float low, float high)
```

## Parameters

| Type | Name |
|------|------|
| `integer` | `corner` |
| `float` | `low` |
| `float` | `high` |

## Return Value

`void`

## Timing, Energy and Permissions

- **Threat Level:** High
- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osSetTerrainTextureHeight](https://opensimulator.org/wiki/osSetTerrainTextureHeight)
