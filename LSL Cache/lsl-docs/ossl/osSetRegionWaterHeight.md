---
name: "osSetRegionWaterHeight"
category: "function"
type: "function"
language: "OSSL"
description: "Set the water height of the region."
signature: "void osSetRegionWaterHeight(float height)"
return_type: "void"
threat_level: "High"
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osSetRegionWaterHeight"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Set the water height of the region.

## Syntax

```lsl
void osSetRegionWaterHeight(float height)
```

## Parameters

| Type | Name |
|------|------|
| `float` | `height` |

## Return Value

`void`

## Timing, Energy and Permissions

- **Threat Level:** High
- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osSetRegionWaterHeight](https://opensimulator.org/wiki/osSetRegionWaterHeight)
