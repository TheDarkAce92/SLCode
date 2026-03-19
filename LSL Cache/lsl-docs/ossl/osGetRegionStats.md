---
name: "osGetRegionStats"
category: "function"
type: "function"
language: "OSSL"
description: "Returns a list of statistics regarding the region and simulator from the stats reporter module."
signature: "list osGetRegionStats()"
return_type: "list"
threat_level: "Moderate"
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osGetRegionStats"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Returns a list of statistics regarding the region and simulator from the stats reporter module.

## Syntax

```lsl
list osGetRegionStats()
```

## Return Value

`list`

## Timing, Energy and Permissions

- **Threat Level:** Moderate
- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osGetRegionStats](https://opensimulator.org/wiki/osGetRegionStats)
