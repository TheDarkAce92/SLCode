---
name: "osDrawEllipse"
category: "function"
type: "function"
language: "OSSL"
description: "Appends an ellipse drawing command to the string provided in drawList and returns the result.\nThe ellipse is drawn with the current pen size and color on the x,y point pairs that comes from LSL list."
signature: "string osDrawEllipse(string drawList, integer width, integer height)"
return_type: "string"
threat_level: ""
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osDrawEllipse"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Appends an ellipse drawing command to the string provided in drawList and returns the result.\nThe ellipse is drawn with the current pen size and color on the x,y point pairs that comes from LSL list.

## Syntax

```lsl
string osDrawEllipse(string drawList, integer width, integer height)
```

## Parameters

| Type | Name |
|------|------|
| `string` | `drawList` |
| `integer` | `width` |
| `integer` | `height` |

## Return Value

`string`

## Timing, Energy and Permissions

- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osDrawEllipse](https://opensimulator.org/wiki/osDrawEllipse)
