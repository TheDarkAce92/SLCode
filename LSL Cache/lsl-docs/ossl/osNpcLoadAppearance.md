---
name: "osNpcLoadAppearance"
category: "function"
type: "function"
language: "OSSL"
description: "Loads a given appearance notecard to a given NPC (key)."
signature: "void osNpcLoadAppearance(key npc, string notecard)"
return_type: "void"
threat_level: "High"
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osNpcLoadAppearance"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Loads a given appearance notecard to a given NPC (key).

## Syntax

```lsl
void osNpcLoadAppearance(key npc, string notecard)
```

## Parameters

| Type | Name |
|------|------|
| `key` | `npc` |
| `string` | `notecard` |

## Return Value

`void`

## Timing, Energy and Permissions

- **Threat Level:** High
- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osNpcLoadAppearance](https://opensimulator.org/wiki/osNpcLoadAppearance)
