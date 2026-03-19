---
name: "osEjectFromGroup"
category: "function"
type: "function"
language: "OSSL"
description: "Removes a given avatar from the group the object belongs to."
signature: "integer osEjectFromGroup(key agentId)"
return_type: "integer"
threat_level: "VeryLow"
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osEjectFromGroup"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Removes a given avatar from the group the object belongs to.

## Syntax

```lsl
integer osEjectFromGroup(key agentId)
```

## Parameters

| Type | Name |
|------|------|
| `key` | `agentId` |

## Return Value

`integer`

## Timing, Energy and Permissions

- **Threat Level:** VeryLow
- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osEjectFromGroup](https://opensimulator.org/wiki/osEjectFromGroup)
