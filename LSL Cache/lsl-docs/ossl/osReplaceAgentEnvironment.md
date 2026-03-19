---
name: "osReplaceAgentEnvironment"
category: "function"
type: "function"
language: "OSSL"
description: "Sets the environment of a given avatar (key) to a given settings item (asset UUID) with transition time."
signature: "integer osReplaceAgentEnvironment(key agentkey, integer transition, string daycycle)"
return_type: "integer"
threat_level: ""
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osReplaceAgentEnvironment"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Sets the environment of a given avatar (key) to a given settings item (asset UUID) with transition time.

## Syntax

```lsl
integer osReplaceAgentEnvironment(key agentkey, integer transition, string daycycle)
```

## Parameters

| Type | Name |
|------|------|
| `key` | `agentkey` |
| `integer` | `transition` |
| `string` | `daycycle` |

## Return Value

`integer`

## Timing, Energy and Permissions

- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osReplaceAgentEnvironment](https://opensimulator.org/wiki/osReplaceAgentEnvironment)
