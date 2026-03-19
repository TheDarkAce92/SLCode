---
name: "osStringRemove"
category: "function"
type: "function"
language: "OSSL"
description: "Returns the remainder of a given string with characters from start index and count removed."
signature: "string osStringRemove(string src, integer start, integer count)"
return_type: "string"
threat_level: ""
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osStringRemove"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Returns the remainder of a given string with characters from start index and count removed.

## Syntax

```lsl
string osStringRemove(string src, integer start, integer count)
```

## Parameters

| Type | Name |
|------|------|
| `string` | `src` |
| `integer` | `start` |
| `integer` | `count` |

## Return Value

`string`

## Timing, Energy and Permissions

- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osStringRemove](https://opensimulator.org/wiki/osStringRemove)
