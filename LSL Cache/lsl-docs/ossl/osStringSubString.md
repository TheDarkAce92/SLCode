---
name: "osStringSubString"
category: "function"
type: "function"
language: "OSSL"
description: "Returns a substring from start index and length."
signature: "string osStringSubString(string src, integer start, integer length)"
return_type: "string"
threat_level: ""
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osStringSubString"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Returns a substring from start index and length.

## Syntax

```lsl
string osStringSubString(string src, integer start, integer length)
```

## Parameters

| Type | Name |
|------|------|
| `string` | `src` |
| `integer` | `start` |
| `integer` | `length` |

## Return Value

`string`

## Timing, Energy and Permissions

- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osStringSubString](https://opensimulator.org/wiki/osStringSubString)
