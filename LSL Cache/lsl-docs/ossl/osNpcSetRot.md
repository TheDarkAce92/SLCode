---
name: "osNpcSetRot"
category: "function"
type: "function"
language: "OSSL"
description: "Sets the rotation of a given NPC (key)."
signature: "void osNpcSetRot(key npc, rotation rot)"
return_type: "void"
threat_level: "High"
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osNpcSetRot"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Sets the rotation of a given NPC (key).

## Syntax

```lsl
void osNpcSetRot(key npc, rotation rot)
```

## Parameters

| Type | Name |
|------|------|
| `key` | `npc` |
| `rotation` | `rot` |

## Return Value

`void`

## Timing, Energy and Permissions

- **Threat Level:** High
- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osNpcSetRot](https://opensimulator.org/wiki/osNpcSetRot)
