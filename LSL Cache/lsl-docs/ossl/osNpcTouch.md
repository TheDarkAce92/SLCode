---
name: "osNpcTouch"
category: "function"
type: "function"
language: "OSSL"
description: "Instructs a given NPC (key) to touch a given object (UUID) and link."
signature: "void osNpcTouch(key npc, key object_key, integer link_num)"
return_type: "void"
threat_level: "High"
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osNpcTouch"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Instructs a given NPC (key) to touch a given object (UUID) and link.

## Syntax

```lsl
void osNpcTouch(key npc, key object_key, integer link_num)
```

## Parameters

| Type | Name |
|------|------|
| `key` | `npc` |
| `key` | `object_key` |
| `integer` | `link_num` |

## Return Value

`void`

## Timing, Energy and Permissions

- **Threat Level:** High
- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osNpcTouch](https://opensimulator.org/wiki/osNpcTouch)
