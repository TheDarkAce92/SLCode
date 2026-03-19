---
name: "osGetHealRate"
category: "function"
type: "function"
language: "OSSL"
description: "Returns the rate of healing for a given avatar."
signature: "float osGetHealRate(key agentId)"
return_type: "float"
threat_level: "None"
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osGetHealRate"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Returns the rate of healing for a given avatar.

## Syntax

```lsl
float osGetHealRate(key agentId)
```

## Parameters

| Type | Name |
|------|------|
| `key` | `agentId` |

## Return Value

`float`

## Timing, Energy and Permissions

- **Threat Level:** None
- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osGetHealRate](https://opensimulator.org/wiki/osGetHealRate)
