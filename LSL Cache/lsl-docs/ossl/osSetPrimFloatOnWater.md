---
name: "osSetPrimFloatOnWater"
category: "function"
type: "function"
language: "OSSL"
description: "Sets whether the object should float on water."
signature: "void osSetPrimFloatOnWater(integer floatYN)"
return_type: "void"
threat_level: "VeryLow"
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osSetPrimFloatOnWater"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Sets whether the object should float on water.

## Syntax

```lsl
void osSetPrimFloatOnWater(integer floatYN)
```

## Parameters

| Type | Name |
|------|------|
| `integer` | `floatYN` |

## Return Value

`void`

## Timing, Energy and Permissions

- **Threat Level:** VeryLow
- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osSetPrimFloatOnWater](https://opensimulator.org/wiki/osSetPrimFloatOnWater)
