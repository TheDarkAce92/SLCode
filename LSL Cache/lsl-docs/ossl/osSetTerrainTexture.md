---
name: "osSetTerrainTexture"
category: "function"
type: "function"
language: "OSSL"
description: "Sets the terrain texture for a given level."
signature: "void osSetTerrainTexture(integer level, key texture)"
return_type: "void"
threat_level: "High"
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osSetTerrainTexture"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Sets the terrain texture for a given level.

## Syntax

```lsl
void osSetTerrainTexture(integer level, key texture)
```

## Parameters

| Type | Name |
|------|------|
| `integer` | `level` |
| `key` | `texture` |

## Return Value

`void`

## Timing, Energy and Permissions

- **Threat Level:** High
- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osSetTerrainTexture](https://opensimulator.org/wiki/osSetTerrainTexture)
