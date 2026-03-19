---
name: "osSetPenColor"
category: "function"
type: "function"
language: "OSSL"
description: "This sets the drawing color to either a named .NET color, a 32-bit color value (formatted as eight hexadecimal digits in the format aarrggbb, representing the eight-bit alpha, red, green and blue channels) or a LSL vector color and alpha float value."
signature: "string osSetPenColor(string drawList, LSL_Types.Vector3 color, float alpha)"
return_type: "string"
threat_level: ""
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osSetPenColor"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

This sets the drawing color to either a named .NET color, a 32-bit color value (formatted as eight hexadecimal digits in the format aarrggbb, representing the eight-bit alpha, red, green and blue channels) or a LSL vector color and alpha float value.

## Syntax

```lsl
string osSetPenColor(string drawList, LSL_Types.Vector3 color, float alpha)
```

## Parameters

| Type | Name |
|------|------|
| `string` | `drawList` |
| `LSL_Types.Vector3` | `color` |
| `float` | `alpha` |

## Return Value

`string`

## Timing, Energy and Permissions

- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osSetPenColor](https://opensimulator.org/wiki/osSetPenColor)
