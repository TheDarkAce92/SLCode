---
name: "osCheckODE"
category: "function"
type: "function"
language: "OSSL"
description: "Returns whether the simulator is using the ODE physics engine."
signature: "integer osCheckODE()"
return_type: "integer"
threat_level: ""
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osCheckODE"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Returns whether the simulator is using the ODE physics engine.

## Syntax

```lsl
integer osCheckODE()
```

## Return Value

`integer`

## Timing, Energy and Permissions

- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osCheckODE](https://opensimulator.org/wiki/osCheckODE)
