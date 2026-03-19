---
name: "osListAsInteger"
category: "function"
type: "function"
language: "OSSL"
description: "Returns a integer that is at index(>=0) in src or 0 if that is not a integer"
signature: "integer osListAsInteger(list src, integer index)"
return_type: "integer"
threat_level: ""
energy_cost: ""
sleep_time: ""
wiki_url: "https://opensimulator.org/wiki/osListAsInteger"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-18"
last_updated: "2026-03-19"
---

Returns a integer that is at index(>=0) in src or 0 if that is not a integer

## Syntax

```lsl
integer osListAsInteger(list src, integer index)
```

## Parameters

| Type | Name |
|------|------|
| `list` | `src` |
| `integer` | `index` |

## Return Value

`integer`

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osListAsInteger](https://opensimulator.org/wiki/osListAsInteger)
