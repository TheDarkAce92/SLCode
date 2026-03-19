---
name: "osNpcSaveAppearance"
category: "function"
type: "function"
language: "OSSL"
description: "Creates a new notecard with a given name from a given NPC (key) with the option to include HUDs."
signature: "key osNpcSaveAppearance(key npc, string notecard, integer includeHuds)"
return_type: "key"
threat_level: "High"
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osNpcSaveAppearance"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Creates a new notecard with a given name from a given NPC (key) with the option to include HUDs.

## Syntax

```lsl
key osNpcSaveAppearance(key npc, string notecard, integer includeHuds)
```

## Parameters

| Type | Name |
|------|------|
| `key` | `npc` |
| `string` | `notecard` |
| `integer` | `includeHuds` |

## Return Value

`key`

## Timing, Energy and Permissions

- **Threat Level:** High
- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osNpcSaveAppearance](https://opensimulator.org/wiki/osNpcSaveAppearance)
