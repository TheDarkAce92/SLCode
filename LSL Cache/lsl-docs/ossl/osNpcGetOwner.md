---
name: "osNpcGetOwner"
category: "function"
type: "function"
language: "OSSL"
description: "Returns the owner key of a given NPC. NULL_KEY if the NPC is unowned."
signature: "key osNpcGetOwner(key npc)"
return_type: "key"
threat_level: "None"
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osNpcGetOwner"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Returns the owner key of a given NPC. NULL_KEY if the NPC is unowned.

## Syntax

```lsl
key osNpcGetOwner(key npc)
```

## Parameters

| Type | Name |
|------|------|
| `key` | `npc` |

## Return Value

`key`

## Timing, Energy and Permissions

- **Threat Level:** None
- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osNpcGetOwner](https://opensimulator.org/wiki/osNpcGetOwner)
