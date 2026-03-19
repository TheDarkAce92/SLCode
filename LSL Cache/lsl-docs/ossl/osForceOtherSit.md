---
name: "osForceOtherSit"
category: "function"
type: "function"
language: "OSSL"
description: "Forces a given avatar to sit on a given target (object UUID) bypassing permissions."
signature: "void osForceOtherSit(string avatar, string target)"
return_type: "void"
threat_level: "VeryHigh"
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osForceOtherSit"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Forces a given avatar to sit on a given target (object UUID) bypassing permissions.

## Syntax

```lsl
void osForceOtherSit(string avatar, string target)
```

## Parameters

| Type | Name |
|------|------|
| `string` | `avatar` |
| `string` | `target` |

## Return Value

`void`

## Timing, Energy and Permissions

- **Threat Level:** VeryHigh
- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osForceOtherSit](https://opensimulator.org/wiki/osForceOtherSit)
