---
name: "osNpcSayTo"
category: "function"
type: "function"
language: "OSSL"
description: "Instructs a given NPC (key) to say to a given avatar (key) a given message on a given channel."
signature: "void osNpcSayTo(key npc, key target, integer channel, string message)"
return_type: "void"
threat_level: "High"
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osNpcSayTo"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Instructs a given NPC (key) to say to a given avatar (key) a given message on a given channel.

## Syntax

```lsl
void osNpcSayTo(key npc, key target, integer channel, string message)
```

## Parameters

| Type | Name |
|------|------|
| `key` | `npc` |
| `key` | `target` |
| `integer` | `channel` |
| `string` | `message` |

## Return Value

`void`

## Timing, Energy and Permissions

- **Threat Level:** High
- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osNpcSayTo](https://opensimulator.org/wiki/osNpcSayTo)
