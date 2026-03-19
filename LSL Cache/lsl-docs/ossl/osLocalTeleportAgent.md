---
name: "osLocalTeleportAgent"
category: "function"
type: "function"
language: "OSSL"
description: "Teleport a given avatar (key) to a given position and rotation as look at vector with a velocity vector and teleport flags."
signature: "void osLocalTeleportAgent(key agent, LSL_Types.Vector3 position, LSL_Types.Vector3 velocity, LSL_Types.Vector3 lookat, integer flags)"
return_type: "void"
threat_level: ""
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osLocalTeleportAgent"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Teleport a given avatar (key) to a given position and rotation as look at vector with a velocity vector and teleport flags.

## Syntax

```lsl
void osLocalTeleportAgent(key agent, LSL_Types.Vector3 position, LSL_Types.Vector3 velocity, LSL_Types.Vector3 lookat, integer flags)
```

## Parameters

| Type | Name |
|------|------|
| `key` | `agent` |
| `LSL_Types.Vector3` | `position` |
| `LSL_Types.Vector3` | `velocity` |
| `LSL_Types.Vector3` | `lookat` |
| `integer` | `flags` |

## Return Value

`void`

## Timing, Energy and Permissions

- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osLocalTeleportAgent](https://opensimulator.org/wiki/osLocalTeleportAgent)
