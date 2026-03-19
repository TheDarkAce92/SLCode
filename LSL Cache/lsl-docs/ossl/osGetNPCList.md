---
name: "osGetNPCList"
category: "function"
type: "function"
language: "OSSL"
description: "Returns a strided list (key, position, name) of all NPCs in the region."
signature: "list osGetNPCList()"
return_type: "list"
threat_level: "None"
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osGetNPCList"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Returns a strided list (key, position, name) of all NPCs in the region.

## Syntax

```lsl
list osGetNPCList()
```

## Return Value

`list`

## Timing, Energy and Permissions

- **Threat Level:** None
- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osGetNPCList](https://opensimulator.org/wiki/osGetNPCList)
