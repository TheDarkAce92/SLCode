---
name: "osReplaceRegionEnvironment"
category: "function"
type: "function"
language: "OSSL"
description: "Alters the region environment base parameters of a given settings item (asset UUID) with transition time."
signature: "integer osReplaceRegionEnvironment(integer transition, string daycycle, float daylen, float dayoffset, float altitude1, float altitude2, float altitude3)"
return_type: "integer"
threat_level: ""
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osReplaceRegionEnvironment"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Alters the region environment base parameters of a given settings item (asset UUID) with transition time.

## Syntax

```lsl
integer osReplaceRegionEnvironment(integer transition, string daycycle, float daylen, float dayoffset, float altitude1, float altitude2, float altitude3)
```

## Parameters

| Type | Name |
|------|------|
| `integer` | `transition` |
| `string` | `daycycle` |
| `float` | `daylen` |
| `float` | `dayoffset` |
| `float` | `altitude1` |
| `float` | `altitude2` |
| `float` | `altitude3` |

## Return Value

`integer`

## Timing, Energy and Permissions

- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osReplaceRegionEnvironment](https://opensimulator.org/wiki/osReplaceRegionEnvironment)
