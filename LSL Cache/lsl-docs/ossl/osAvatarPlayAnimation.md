---
name: "osAvatarPlayAnimation"
category: "function"
type: "function"
language: "OSSL"
description: "Forcefully plays a given animation for a given avatar bypassing animation permissions."
signature: "void osAvatarPlayAnimation(key avatar, string animation)"
return_type: "void"
threat_level: "VeryHigh"
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osAvatarPlayAnimation"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Forcefully plays a given animation for a given avatar bypassing animation permissions.

## Syntax

```lsl
void osAvatarPlayAnimation(key avatar, string animation)
```

## Parameters

| Type | Name |
|------|------|
| `key` | `avatar` |
| `string` | `animation` |

## Return Value

`void`

## Timing, Energy and Permissions

- **Threat Level:** VeryHigh
- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osAvatarPlayAnimation](https://opensimulator.org/wiki/osAvatarPlayAnimation)
