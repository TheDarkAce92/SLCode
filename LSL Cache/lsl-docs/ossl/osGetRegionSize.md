---
name: "osGetRegionSize"
category: "function"
type: "function"
language: "OSSL"
description: "Returns the x and y size of the region as vector. z is unused."
signature: "vector osGetRegionSize()"
return_type: "vector"
threat_level: ""
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osGetRegionSize"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Returns the x and y size of the region as vector. z is unused.

## Syntax

```lsl
vector osGetRegionSize()
```

## Return Value

`vector`

## Timing, Energy and Permissions

- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osGetRegionSize](https://opensimulator.org/wiki/osGetRegionSize)
