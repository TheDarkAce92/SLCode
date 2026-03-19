---
name: "osDrawText"
category: "function"
type: "function"
language: "OSSL"
description: "Draws a given string as text at the current drawing position. Text extends right and downwards."
signature: "string osDrawText(string drawList, string text)"
return_type: "string"
threat_level: ""
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osDrawText"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Draws a given string as text at the current drawing position. Text extends right and downwards.

## Syntax

```lsl
string osDrawText(string drawList, string text)
```

## Parameters

| Type | Name |
|------|------|
| `string` | `drawList` |
| `string` | `text` |

## Return Value

`string`

## Timing, Energy and Permissions

- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osDrawText](https://opensimulator.org/wiki/osDrawText)
