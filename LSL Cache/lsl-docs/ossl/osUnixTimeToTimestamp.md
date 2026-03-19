---
name: "osUnixTimeToTimestamp"
category: "function"
type: "function"
language: "OSSL"
description: "Returns the timestamp string for a given unix epoch (seconds)."
signature: "string osUnixTimeToTimestamp(integer time)"
return_type: "string"
threat_level: ""
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osUnixTimeToTimestamp"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Returns the timestamp string for a given unix epoch (seconds).

## Syntax

```lsl
string osUnixTimeToTimestamp(integer time)
```

## Parameters

| Type | Name |
|------|------|
| `integer` | `time` |

## Return Value

`string`

## Timing, Energy and Permissions

- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osUnixTimeToTimestamp](https://opensimulator.org/wiki/osUnixTimeToTimestamp)
