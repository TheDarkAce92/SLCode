---
name: "osGetGridGatekeeperURI"
category: "function"
type: "function"
language: "OSSL"
description: "Returns the gatekeeper URI of the current grid."
signature: "string osGetGridGatekeeperURI()"
return_type: "string"
threat_level: "Moderate"
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osGetGridGatekeeperURI"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Returns the gatekeeper URI of the current grid.

## Syntax

```lsl
string osGetGridGatekeeperURI()
```

## Return Value

`string`

## Timing, Energy and Permissions

- **Threat Level:** Moderate
- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osGetGridGatekeeperURI](https://opensimulator.org/wiki/osGetGridGatekeeperURI)
