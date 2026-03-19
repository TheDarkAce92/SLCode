---
name: "osNpcLookAt"
category: "function"
type: "function"
language: "OSSL"
description: "Sets the look at direction of a NPC to a given object (key) and offset."
signature: "integer osNpcLookAt(key npckey, integer type, key objkey, vector offset)"
return_type: "integer"
threat_level: ""
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osNpcLookAt"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Sets the look at direction of a NPC to a given object (key) and offset.

## Syntax

```lsl
integer osNpcLookAt(key npckey, integer type, key objkey, vector offset)
```

## Parameters

| Type | Name |
|------|------|
| `key` | `npckey` |
| `integer` | `type` |
| `key` | `objkey` |
| `vector` | `offset` |

## Return Value

`integer`

## Timing, Energy and Permissions

- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osNpcLookAt](https://opensimulator.org/wiki/osNpcLookAt)
