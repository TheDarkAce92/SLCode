---
name: "osGetInertiaData"
category: "function"
type: "function"
language: "OSSL"
description: "Returns a list of the inertia data of the object containing the script."
signature: "list osGetInertiaData()"
return_type: "list"
threat_level: ""
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osGetInertiaData"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Returns a list of the inertia data of the object containing the script.

## Syntax

```lsl
list osGetInertiaData()
```

## Return Value

`list`

## Timing, Energy and Permissions

- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osGetInertiaData](https://opensimulator.org/wiki/osGetInertiaData)
