---
name: "osDetectedCountry"
category: "function"
type: "function"
language: "OSSL"
description: "Detected params return of triggered user event of their set country."
signature: "string osDetectedCountry(integer number)"
return_type: "string"
threat_level: "Moderate"
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osDetectedCountry"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Detected params return of triggered user event of their set country.

## Syntax

```lsl
string osDetectedCountry(integer number)
```

## Parameters

| Type | Name |
|------|------|
| `integer` | `number` |

## Return Value

`string`

## Timing, Energy and Permissions

- **Threat Level:** Moderate
- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osDetectedCountry](https://opensimulator.org/wiki/osDetectedCountry)
