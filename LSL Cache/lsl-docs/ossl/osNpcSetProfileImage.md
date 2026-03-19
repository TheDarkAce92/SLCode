---
name: "osNpcSetProfileImage"
category: "function"
type: "function"
language: "OSSL"
description: "Sets a given NPC (key) profile image to a given image (asset UUID)."
signature: "void osNpcSetProfileImage(key npc, string image)"
return_type: "void"
threat_level: "Low"
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osNpcSetProfileImage"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Sets a given NPC (key) profile image to a given image (asset UUID).

## Syntax

```lsl
void osNpcSetProfileImage(key npc, string image)
```

## Parameters

| Type | Name |
|------|------|
| `key` | `npc` |
| `string` | `image` |

## Return Value

`void`

## Timing, Energy and Permissions

- **Threat Level:** Low
- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osNpcSetProfileImage](https://opensimulator.org/wiki/osNpcSetProfileImage)
