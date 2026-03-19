---
name: "osRegexIsMatch"
category: "function"
type: "function"
language: "OSSL"
description: "Returns an integer whether the input string matches a regex pattern."
signature: "integer osRegexIsMatch(string input, string pattern)"
return_type: "integer"
threat_level: "Low"
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osRegexIsMatch"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Returns an integer whether the input string matches a regex pattern.

## Syntax

```lsl
integer osRegexIsMatch(string input, string pattern)
```

## Parameters

| Type | Name |
|------|------|
| `string` | `input` |
| `string` | `pattern` |

## Return Value

`integer`

## Timing, Energy and Permissions

- **Threat Level:** Low
- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osRegexIsMatch](https://opensimulator.org/wiki/osRegexIsMatch)
