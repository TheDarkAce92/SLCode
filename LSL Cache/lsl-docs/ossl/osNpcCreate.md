---
name: "osNpcCreate"
category: "function"
type: "function"
language: "OSSL"
description: "Creates a new NPC with a given name at a given position using a supplied notecard for appearance and additional options."
signature: "key osNpcCreate(string user, string name, vector position, string notecard, integer options)"
return_type: "key"
threat_level: "High"
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osNpcCreate"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Creates a new NPC with a given name at a given position using a supplied notecard for appearance and additional options.

## Syntax

```lsl
key osNpcCreate(string user, string name, vector position, string notecard, integer options)
```

## Parameters

| Type | Name |
|------|------|
| `string` | `user` |
| `string` | `name` |
| `vector` | `position` |
| `string` | `notecard` |
| `integer` | `options` |

## Return Value

`key`

## Timing, Energy and Permissions

- **Threat Level:** High
- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osNpcCreate](https://opensimulator.org/wiki/osNpcCreate)
