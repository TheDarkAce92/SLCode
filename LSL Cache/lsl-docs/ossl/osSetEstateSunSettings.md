---
name: "osSetEstateSunSettings"
category: "function"
type: "function"
language: "OSSL"
description: "Set sun type (fixed, daycycle) and time offset for the estate sun."
signature: "void osSetEstateSunSettings(integer sunFixed, float sunHour)"
return_type: "void"
threat_level: "High"
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osSetEstateSunSettings"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Set sun type (fixed, daycycle) and time offset for the estate sun.

## Syntax

```lsl
void osSetEstateSunSettings(integer sunFixed, float sunHour)
```

## Parameters

| Type | Name |
|------|------|
| `integer` | `sunFixed` |
| `float` | `sunHour` |

## Return Value

`void`

## Timing, Energy and Permissions

- **Threat Level:** High
- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osSetEstateSunSettings](https://opensimulator.org/wiki/osSetEstateSunSettings)
