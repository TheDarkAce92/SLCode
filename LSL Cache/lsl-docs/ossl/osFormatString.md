---
name: "osFormatString"
category: "function"
type: "function"
language: "OSSL"
description: "Fills a given strings placeholders {%d} with the entries of the given list."
signature: "string osFormatString(string str, list strings)"
return_type: "string"
threat_level: "VeryLow"
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osFormatString"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Fills a given strings placeholders {%d} with the entries of the given list.

## Syntax

```lsl
string osFormatString(string str, list strings)
```

## Parameters

| Type | Name |
|------|------|
| `string` | `str` |
| `list` | `strings` |

## Return Value

`string`

## Timing, Energy and Permissions

- **Threat Level:** VeryLow
- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osFormatString](https://opensimulator.org/wiki/osFormatString)
