---
name: "osAgentSaveAppearance"
category: "function"
type: "function"
language: "OSSL"
description: "Save appearance of an avatar (with the choice to include Huds or no) to a notecard in the primitive inventory."
signature: "key osAgentSaveAppearance(key agentId, string notecard, integer includeHuds)"
return_type: "key"
threat_level: "VeryHigh"
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osAgentSaveAppearance"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Save appearance of an avatar (with the choice to include Huds or no) to a notecard in the primitive inventory.

## Syntax

```lsl
key osAgentSaveAppearance(key agentId, string notecard, integer includeHuds)
```

## Parameters

| Type | Name |
|------|------|
| `key` | `agentId` |
| `string` | `notecard` |
| `integer` | `includeHuds` |

## Return Value

`key`

## Timing, Energy and Permissions

- **Threat Level:** VeryHigh
- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osAgentSaveAppearance](https://opensimulator.org/wiki/osAgentSaveAppearance)
