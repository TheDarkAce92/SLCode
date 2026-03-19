---
name: "osNpcGetPos"
category: "function"
type: "function"
language: "OSSL"
description: "Returns the position of a given NPC (key)."
signature: "vector osNpcGetPos(key npc)"
return_type: "vector"
threat_level: "High"
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osNpcGetPos"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Returns the position of a given NPC (key).

## Syntax

```lsl
vector osNpcGetPos(key npc)
```

## Parameters

| Type | Name |
|------|------|
| `key` | `npc` |

## Return Value

`vector`

## Timing, Energy and Permissions

- **Threat Level:** High
- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osNpcGetPos](https://opensimulator.org/wiki/osNpcGetPos)
