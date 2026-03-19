---
name: "osCollisionSound"
category: "function"
type: "function"
language: "OSSL"
description: "Sets a given collision sound and volume to the object containing the script."
signature: "void osCollisionSound(string impact_sound, float impact_volume)"
return_type: "void"
threat_level: ""
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osCollisionSound"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Sets a given collision sound and volume to the object containing the script.

## Syntax

```lsl
void osCollisionSound(string impact_sound, float impact_volume)
```

## Parameters

| Type | Name |
|------|------|
| `string` | `impact_sound` |
| `float` | `impact_volume` |

## Return Value

`void`

## Timing, Energy and Permissions

- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osCollisionSound](https://opensimulator.org/wiki/osCollisionSound)
