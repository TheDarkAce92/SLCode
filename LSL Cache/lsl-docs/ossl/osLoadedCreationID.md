---
name: "osLoadedCreationID"
category: "function"
type: "function"
language: "OSSL"
description: "Returns the original region UUID of the loaded region scene data."
signature: "string osLoadedCreationID()"
return_type: "string"
threat_level: "Low"
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osLoadedCreationID"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Returns the original region UUID of the loaded region scene data.

## Syntax

```lsl
string osLoadedCreationID()
```

## Return Value

`string`

## Timing, Energy and Permissions

- **Threat Level:** Low
- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osLoadedCreationID](https://opensimulator.org/wiki/osLoadedCreationID)
