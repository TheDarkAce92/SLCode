---
name: "osReplaceString"
category: "function"
type: "function"
language: "OSSL"
description: "Returns a string with replaced substrings given a match pattern from a given start for a given number of matches."
signature: "string osReplaceString(string src, string pattern, string replace, integer count, integer start)"
return_type: "string"
threat_level: "VeryLow"
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osReplaceString"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Returns a string with replaced substrings given a match pattern from a given start for a given number of matches.

## Syntax

```lsl
string osReplaceString(string src, string pattern, string replace, integer count, integer start)
```

## Parameters

| Type | Name |
|------|------|
| `string` | `src` |
| `string` | `pattern` |
| `string` | `replace` |
| `integer` | `count` |
| `integer` | `start` |

## Return Value

`string`

## Timing, Energy and Permissions

- **Threat Level:** VeryLow
- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osReplaceString](https://opensimulator.org/wiki/osReplaceString)
