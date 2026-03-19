---
name: "osStringStartsWith"
category: "function"
type: "function"
language: "OSSL"
description: "Returns an integer whether a string starts with another string."
signature: "integer osStringStartsWith(string src, string value, integer ignorecase)"
return_type: "integer"
threat_level: ""
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osStringStartsWith"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Returns an integer whether a string starts with another string.

## Syntax

```lsl
integer osStringStartsWith(string src, string value, integer ignorecase)
```

## Parameters

| Type | Name |
|------|------|
| `string` | `src` |
| `string` | `value` |
| `integer` | `ignorecase` |

## Return Value

`integer`

## Timing, Energy and Permissions

- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osStringStartsWith](https://opensimulator.org/wiki/osStringStartsWith)
