---
name: "osGetGridName"
category: "function"
type: "function"
language: "OSSL"
description: "Returns the grid name of the current grid."
signature: "string osGetGridName()"
return_type: "string"
threat_level: ""
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osGetGridName"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Returns the grid name of the current grid.

## Syntax

```lsl
string osGetGridName()
```

## Return Value

`string`

## Timing, Energy and Permissions

- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osGetGridName](https://opensimulator.org/wiki/osGetGridName)
