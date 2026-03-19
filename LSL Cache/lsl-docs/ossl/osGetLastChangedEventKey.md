---
name: "osGetLastChangedEventKey"
category: "function"
type: "function"
language: "OSSL"
description: "Returns the key of the last event setting detected params."
signature: "key osGetLastChangedEventKey()"
return_type: "key"
threat_level: ""
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osGetLastChangedEventKey"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Returns the key of the last event setting detected params.

## Syntax

```lsl
key osGetLastChangedEventKey()
```

## Return Value

`key`

## Timing, Energy and Permissions

- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osGetLastChangedEventKey](https://opensimulator.org/wiki/osGetLastChangedEventKey)
