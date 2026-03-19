---
name: "osListAsVector"
category: "function"
type: "function"
language: "OSSL"
description: "Returns a vector that is at index(>=0) in src or Zero vector if that is not a vector"
signature: "vector osListAsVector(list src, integer index)"
return_type: "vector"
threat_level: ""
energy_cost: ""
sleep_time: ""
wiki_url: "https://opensimulator.org/wiki/osListAsVector"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-18"
last_updated: "2026-03-19"
---

Returns a vector that is at index(>=0) in src or Zero vector if that is not a vector

## Syntax

```lsl
vector osListAsVector(list src, integer index)
```

## Parameters

| Type | Name |
|------|------|
| `list` | `src` |
| `integer` | `index` |

## Return Value

`vector`

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osListAsVector](https://opensimulator.org/wiki/osListAsVector)
