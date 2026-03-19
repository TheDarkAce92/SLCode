---
name: "osGetNotecardLine"
category: "function"
type: "function"
language: "OSSL"
description: "Directly returns a given line of a notecard in the primitive inventory."
signature: "string osGetNotecardLine(string name, integer line)"
return_type: "string"
threat_level: "VeryHigh"
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osGetNotecardLine"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Directly returns a given line of a notecard in the primitive inventory.

## Syntax

```lsl
string osGetNotecardLine(string name, integer line)
```

## Parameters

| Type | Name |
|------|------|
| `string` | `name` |
| `integer` | `line` |

## Return Value

`string`

## Timing, Energy and Permissions

- **Threat Level:** VeryHigh
- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osGetNotecardLine](https://opensimulator.org/wiki/osGetNotecardLine)
