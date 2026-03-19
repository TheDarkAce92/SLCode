---
name: "osMatchString"
category: "function"
type: "function"
language: "OSSL"
description: "Returns a list of matches from a given string from a given start."
signature: "list osMatchString(string src, string pattern, integer start)"
return_type: "list"
threat_level: "VeryLow"
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osMatchString"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Returns a list of matches from a given string from a given start.

## Syntax

```lsl
list osMatchString(string src, string pattern, integer start)
```

## Parameters

| Type | Name |
|------|------|
| `string` | `src` |
| `string` | `pattern` |
| `integer` | `start` |

## Return Value

`list`

## Timing, Energy and Permissions

- **Threat Level:** VeryLow
- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osMatchString](https://opensimulator.org/wiki/osMatchString)
