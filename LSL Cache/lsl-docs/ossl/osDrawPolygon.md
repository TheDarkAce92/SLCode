---
name: "osDrawPolygon"
category: "function"
type: "function"
language: "OSSL"
description: "Appends a polygon drawing command to the string provided in drawList and returns the result.\nThe polygon is drawn with the current pen size and color on the x,y point pairs that comes from LSL list."
signature: "string osDrawPolygon(string drawList, list x, list y)"
return_type: "string"
threat_level: ""
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osDrawPolygon"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Appends a polygon drawing command to the string provided in drawList and returns the result.\nThe polygon is drawn with the current pen size and color on the x,y point pairs that comes from LSL list.

## Syntax

```lsl
string osDrawPolygon(string drawList, list x, list y)
```

## Parameters

| Type | Name |
|------|------|
| `string` | `drawList` |
| `list` | `x` |
| `list` | `y` |

## Return Value

`string`

## Timing, Energy and Permissions

- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osDrawPolygon](https://opensimulator.org/wiki/osDrawPolygon)
