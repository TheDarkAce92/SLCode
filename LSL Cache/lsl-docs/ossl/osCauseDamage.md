---
name: "osCauseDamage"
category: "function"
type: "function"
language: "OSSL"
description: "Subtracts health from a given avatar by a given amount."
signature: "void osCauseDamage(key avatar, float damage)"
return_type: "void"
threat_level: "High"
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osCauseDamage"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Subtracts health from a given avatar by a given amount.

## Syntax

```lsl
void osCauseDamage(key avatar, float damage)
```

## Parameters

| Type | Name |
|------|------|
| `key` | `avatar` |
| `float` | `damage` |

## Return Value

`void`

## Timing, Energy and Permissions

- **Threat Level:** High
- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osCauseDamage](https://opensimulator.org/wiki/osCauseDamage)
