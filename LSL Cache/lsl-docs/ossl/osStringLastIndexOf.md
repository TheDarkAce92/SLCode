---
name: "osStringLastIndexOf"
category: "function"
type: "function"
language: "OSSL"
description: "Returns the index of the last substring of a given string starting from an index and match count."
signature: "integer osStringLastIndexOf(string src, string value, integer start, integer count, integer ignorecase)"
return_type: "integer"
threat_level: ""
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osStringLastIndexOf"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Returns the index of the last substring of a given string starting from an index and match count.

## Syntax

```lsl
integer osStringLastIndexOf(string src, string value, integer start, integer count, integer ignorecase)
```

## Parameters

| Type | Name |
|------|------|
| `string` | `src` |
| `string` | `value` |
| `integer` | `start` |
| `integer` | `count` |
| `integer` | `ignorecase` |

## Return Value

`integer`

## Timing, Energy and Permissions

- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osStringLastIndexOf](https://opensimulator.org/wiki/osStringLastIndexOf)
