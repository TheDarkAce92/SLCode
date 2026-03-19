---
name: "osNpcStand"
category: "function"
type: "function"
language: "OSSL"
description: "Instructs a given NPC (key) to stand up."
signature: "void osNpcStand(key npc)"
return_type: "void"
threat_level: "High"
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osNpcStand"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Instructs a given NPC (key) to stand up.

## Syntax

```lsl
void osNpcStand(key npc)
```

## Parameters

| Type | Name |
|------|------|
| `key` | `npc` |

## Return Value

`void`

## Timing, Energy and Permissions

- **Threat Level:** High
- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osNpcStand](https://opensimulator.org/wiki/osNpcStand)
