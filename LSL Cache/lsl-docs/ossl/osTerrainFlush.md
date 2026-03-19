---
name: "osTerrainFlush"
category: "function"
type: "function"
language: "OSSL"
description: "Send terrain to all agents"
signature: "void osTerrainFlush()"
return_type: "void"
threat_level: "VeryLow"
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osTerrainFlush"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Send terrain to all agents

## Syntax

```lsl
void osTerrainFlush()
```

## Return Value

`void`

## Timing, Energy and Permissions

- **Threat Level:** VeryLow
- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osTerrainFlush](https://opensimulator.org/wiki/osTerrainFlush)
