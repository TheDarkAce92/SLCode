---
name: "osGetApparentTime"
category: "function"
type: "function"
language: "OSSL"
description: "Returns the virtual seconds since environment midnight."
signature: "float osGetApparentTime()"
return_type: "float"
threat_level: ""
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osGetApparentTime"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Returns the virtual seconds since environment midnight.

## Syntax

```lsl
float osGetApparentTime()
```

## Return Value

`float`

## Timing, Energy and Permissions

- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osGetApparentTime](https://opensimulator.org/wiki/osGetApparentTime)
