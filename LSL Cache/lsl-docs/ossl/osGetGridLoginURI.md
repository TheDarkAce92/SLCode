---
name: "osGetGridLoginURI"
category: "function"
type: "function"
language: "OSSL"
description: "Returns the login URI of the current grid."
signature: "string osGetGridLoginURI()"
return_type: "string"
threat_level: "Moderate"
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osGetGridLoginURI"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Returns the login URI of the current grid.

## Syntax

```lsl
string osGetGridLoginURI()
```

## Return Value

`string`

## Timing, Energy and Permissions

- **Threat Level:** Moderate
- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osGetGridLoginURI](https://opensimulator.org/wiki/osGetGridLoginURI)
