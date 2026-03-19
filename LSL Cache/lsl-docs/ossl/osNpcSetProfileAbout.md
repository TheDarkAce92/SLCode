---
name: "osNpcSetProfileAbout"
category: "function"
type: "function"
language: "OSSL"
description: "Sets a given NPC (key) profile about text to a given string."
signature: "void osNpcSetProfileAbout(key npc, string about)"
return_type: "void"
threat_level: "Low"
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osNpcSetProfileAbout"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Sets a given NPC (key) profile about text to a given string.

## Syntax

```lsl
void osNpcSetProfileAbout(key npc, string about)
```

## Parameters

| Type | Name |
|------|------|
| `key` | `npc` |
| `string` | `about` |

## Return Value

`void`

## Timing, Energy and Permissions

- **Threat Level:** Low
- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osNpcSetProfileAbout](https://opensimulator.org/wiki/osNpcSetProfileAbout)
