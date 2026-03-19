---
name: "osGetLinkNumber"
category: "function"
type: "function"
language: "OSSL"
description: "Return the link number of a given primitive in the linkset by name."
signature: "integer osGetLinkNumber(string name)"
return_type: "integer"
threat_level: ""
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osGetLinkNumber"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Return the link number of a given primitive in the linkset by name.

## Syntax

```lsl
integer osGetLinkNumber(string name)
```

## Parameters

| Type | Name |
|------|------|
| `string` | `name` |

## Return Value

`integer`

## Timing, Energy and Permissions

- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osGetLinkNumber](https://opensimulator.org/wiki/osGetLinkNumber)
