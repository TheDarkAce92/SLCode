---
name: "osGetSimulatorVersion"
category: "function"
type: "function"
language: "OSSL"
description: "Returns the version information of the current simulator."
signature: "string osGetSimulatorVersion()"
return_type: "string"
threat_level: "High"
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osGetSimulatorVersion"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Returns the version information of the current simulator.

## Syntax

```lsl
string osGetSimulatorVersion()
```

## Return Value

`string`

## Timing, Energy and Permissions

- **Threat Level:** High
- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osGetSimulatorVersion](https://opensimulator.org/wiki/osGetSimulatorVersion)
