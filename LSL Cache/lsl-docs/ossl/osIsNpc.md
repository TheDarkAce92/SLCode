---
name: "osIsNpc"
category: "function"
type: "function"
language: "OSSL"
description: "Returns an integer whether a given key is an NPC or avatar."
signature: "integer osIsNpc(key npc)"
return_type: "integer"
threat_level: ""
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osIsNpc"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Returns an integer whether a given key is an NPC or avatar.

## Syntax

```lsl
integer osIsNpc(key npc)
```

## Parameters

| Type | Name |
|------|------|
| `key` | `npc` |

## Return Value

`integer`

## Timing, Energy and Permissions

- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osIsNpc](https://opensimulator.org/wiki/osIsNpc)
