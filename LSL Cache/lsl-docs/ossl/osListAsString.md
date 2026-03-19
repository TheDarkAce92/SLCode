---
name: "osListAsString"
category: "function"
type: "function"
language: "OSSL"
description: "Returns a string that is at index(>=0) in src or empty string if that is not a string"
signature: "string osListAsString(list src, integer index)"
return_type: "string"
threat_level: ""
energy_cost: ""
sleep_time: ""
wiki_url: "https://opensimulator.org/wiki/osListAsString"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-18"
last_updated: "2026-03-19"
---

Returns a string that is at index(>=0) in src or empty string if that is not a string

## Syntax

```lsl
string osListAsString(list src, integer index)
```

## Parameters

| Type | Name |
|------|------|
| `list` | `src` |
| `integer` | `index` |

## Return Value

`string`

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osListAsString](https://opensimulator.org/wiki/osListAsString)
