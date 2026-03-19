---
name: "osTeleportAgent"
category: "function"
type: "function"
language: "OSSL"
description: "Teleport a given avatar (key) to a given position and rotation as look at vector."
signature: "void osTeleportAgent(string agent, LSL_Types.Vector3 position, LSL_Types.Vector3 lookat)"
return_type: "void"
threat_level: "Severe"
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osTeleportAgent"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Teleport a given avatar (key) to a given position and rotation as look at vector.

## Syntax

```lsl
void osTeleportAgent(string agent, LSL_Types.Vector3 position, LSL_Types.Vector3 lookat)
```

## Parameters

| Type | Name |
|------|------|
| `string` | `agent` |
| `LSL_Types.Vector3` | `position` |
| `LSL_Types.Vector3` | `lookat` |

## Return Value

`void`

## Timing, Energy and Permissions

- **Threat Level:** Severe
- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osTeleportAgent](https://opensimulator.org/wiki/osTeleportAgent)
