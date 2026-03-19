---
name: "osKickAvatar"
category: "function"
type: "function"
language: "OSSL"
description: "Disconnects an avatar from the simulator by first and last name or avatar key."
signature: "void osKickAvatar(key agentId, string alert)"
return_type: "void"
threat_level: "Severe"
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osKickAvatar"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Disconnects an avatar from the simulator by first and last name or avatar key.

## Syntax

```lsl
void osKickAvatar(key agentId, string alert)
```

## Parameters

| Type | Name |
|------|------|
| `key` | `agentId` |
| `string` | `alert` |

## Return Value

`void`

## Timing, Energy and Permissions

- **Threat Level:** Severe
- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osKickAvatar](https://opensimulator.org/wiki/osKickAvatar)
