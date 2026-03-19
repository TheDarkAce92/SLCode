---
name: "osCauseHealing"
category: "function"
type: "function"
language: "OSSL"
description: "Heals a given avatar by a given amount."
signature: "void osCauseHealing(key agentId, float healing)"
return_type: "void"
threat_level: "High"
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osCauseHealing"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Heals a given avatar by a given amount.

## Syntax

```lsl
void osCauseHealing(key agentId, float healing)
```

## Parameters

| Type | Name |
|------|------|
| `key` | `agentId` |
| `float` | `healing` |

## Return Value

`void`

## Timing, Energy and Permissions

- **Threat Level:** High
- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osCauseHealing](https://opensimulator.org/wiki/osCauseHealing)
