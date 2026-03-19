---
name: "osDrawFilledRectangle"
category: "function"
type: "function"
language: "OSSL"
description: "Appends a filled rectangle drawing command to the string provided in drawList and returns the result.\nThe rectangle is drawn with the current pen size and color on the x,y point pairs that comes from LSL list."
signature: "string osDrawFilledRectangle(string drawList, integer width, integer height)"
return_type: "string"
threat_level: ""
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osDrawFilledRectangle"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Appends a filled rectangle drawing command to the string provided in drawList and returns the result.\nThe rectangle is drawn with the current pen size and color on the x,y point pairs that comes from LSL list.

## Syntax

```lsl
string osDrawFilledRectangle(string drawList, integer width, integer height)
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
- Reference: [https://opensimulator.org/wiki/osDrawFilledRectangle](https://opensimulator.org/wiki/osDrawFilledRectangle)
