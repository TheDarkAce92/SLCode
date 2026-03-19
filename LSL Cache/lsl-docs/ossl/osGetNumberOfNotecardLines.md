---
name: "osGetNumberOfNotecardLines"
category: "function"
type: "function"
language: "OSSL"
description: "Returns the number of lines of a given notecard."
signature: "integer osGetNumberOfNotecardLines(string name)"
return_type: "integer"
threat_level: "VeryHigh"
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osGetNumberOfNotecardLines"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Returns the number of lines of a given notecard.

## Syntax

```lsl
integer osGetNumberOfNotecardLines(string name)
```

## Parameters

| Type | Name |
|------|------|
| `string` | `name` |

## Return Value

`integer`

## Timing, Energy and Permissions

- **Threat Level:** VeryHigh
- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osGetNumberOfNotecardLines](https://opensimulator.org/wiki/osGetNumberOfNotecardLines)
