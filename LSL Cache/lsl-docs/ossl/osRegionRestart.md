---
name: "osRegionRestart"
category: "function"
type: "function"
language: "OSSL"
description: "Schedule a region restart with broadcast message seconds in the future."
signature: "integer osRegionRestart(float seconds, string msg)"
return_type: "integer"
threat_level: "High"
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osRegionRestart"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Schedule a region restart with broadcast message seconds in the future.

## Syntax

```lsl
integer osRegionRestart(float seconds, string msg)
```

## Parameters

| Type | Name |
|------|------|
| `float` | `seconds` |
| `string` | `msg` |

## Return Value

`integer`

## Timing, Energy and Permissions

- **Threat Level:** High
- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osRegionRestart](https://opensimulator.org/wiki/osRegionRestart)
