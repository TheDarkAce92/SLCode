---
name: "osTeleportObject"
category: "function"
type: "function"
language: "OSSL"
description: "Teleport a given primitive (object UUID) to a given position and rotation."
signature: "integer osTeleportObject(key objectUUID, vector targetPos, rotation targetrotation, integer flags)"
return_type: "integer"
threat_level: "Severe"
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osTeleportObject"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Teleport a given primitive (object UUID) to a given position and rotation.

## Syntax

```lsl
integer osTeleportObject(key objectUUID, vector targetPos, rotation targetrotation, integer flags)
```

## Parameters

| Type | Name |
|------|------|
| `key` | `objectUUID` |
| `vector` | `targetPos` |
| `rotation` | `targetrotation` |
| `integer` | `flags` |

## Return Value

`integer`

## Timing, Energy and Permissions

- **Threat Level:** Severe
- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osTeleportObject](https://opensimulator.org/wiki/osTeleportObject)
