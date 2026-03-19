---
name: "osSetTerrainTextures"
category: "function"
type: "function"
language: "OSSL"
description: "Sets terrain textures for legacy viewers it types == 0 or 2, textures for new viewers it types == 1 or 2 or PBR materials if types == 1"
signature: "void osSetTerrainTextures(list textures, integer types)"
return_type: "void"
threat_level: ""
energy_cost: ""
sleep_time: ""
wiki_url: "https://opensimulator.org/wiki/osSetTerrainTextures"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-18"
last_updated: "2026-03-19"
---

Sets terrain textures for legacy viewers it types == 0 or 2, textures for new viewers it types == 1 or 2 or PBR materials if types == 1

## Syntax

```lsl
void osSetTerrainTextures(list textures, integer types)
```

## Parameters

| Type | Name |
|------|------|
| `list` | `textures` |
| `integer` | `types` |

## Return Value

`void`

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osSetTerrainTextures](https://opensimulator.org/wiki/osSetTerrainTextures)
