---
name: "osNpcPlayAnimation"
category: "function"
type: "function"
language: "OSSL"
description: "Instructs a given NPC (key) to play a given animation (name) from the inventory of the object containing the script."
signature: "void osNpcPlayAnimation(key npc, string animation)"
return_type: "void"
threat_level: "High"
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osNpcPlayAnimation"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Instructs a given NPC (key) to play a given animation (name) from the inventory of the object containing the script.

## Syntax

```lsl
void osNpcPlayAnimation(key npc, string animation)
```

## Parameters

| Type | Name |
|------|------|
| `key` | `npc` |
| `string` | `animation` |

## Return Value

`void`

## Timing, Energy and Permissions

- **Threat Level:** High
- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osNpcPlayAnimation](https://opensimulator.org/wiki/osNpcPlayAnimation)
