---
name: "osNpcWhisper"
category: "function"
type: "function"
language: "OSSL"
description: "Instructs a given NPC (key) to whisper a given message on a given channel."
signature: "void osNpcWhisper(key npc, integer channel, string message)"
return_type: "void"
threat_level: "High"
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osNpcWhisper"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Instructs a given NPC (key) to whisper a given message on a given channel.

## Syntax

```lsl
void osNpcWhisper(key npc, integer channel, string message)
```

## Parameters

| Type | Name |
|------|------|
| `key` | `npc` |
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
- Reference: [https://opensimulator.org/wiki/osNpcWhisper](https://opensimulator.org/wiki/osNpcWhisper)
