---
name: "osRound"
category: "function"
type: "function"
language: "OSSL"
description: "Rounds a given value to a specified amount of digits."
signature: "float osRound(float value, integer digits)"
return_type: "float"
threat_level: ""
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osRound"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Rounds a given value to a specified amount of digits.

## Syntax

```lsl
float osRound(float value, integer digits)
```

## Parameters

| Type | Name |
|------|------|
| `float` | `value` |
| `integer` | `digits` |

## Return Value

`float`

## Timing, Energy and Permissions

- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osRound](https://opensimulator.org/wiki/osRound)
