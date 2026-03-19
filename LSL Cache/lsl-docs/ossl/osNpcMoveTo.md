---
name: "osNpcMoveTo"
category: "function"
type: "function"
language: "OSSL"
description: "Moves a given NPC (key) to a position."
signature: "void osNpcMoveTo(key npc, vector position)"
return_type: "void"
threat_level: "High"
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osNpcMoveTo"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Moves a given NPC (key) to a position.

## Syntax

```lsl
void osNpcMoveTo(key npc, vector position)
```

## Parameters

| Type | Name |
|------|------|
| `key` | `npc` |
| `vector` | `position` |

## Return Value

`void`

## Timing, Energy and Permissions

- **Threat Level:** High
- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osNpcMoveTo](https://opensimulator.org/wiki/osNpcMoveTo)
