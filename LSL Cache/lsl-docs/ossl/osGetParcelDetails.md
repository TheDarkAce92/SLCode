---
name: "osGetParcelDetails"
category: "function"
type: "function"
language: "OSSL"
description: "Returns a list with the requested parcel details."
signature: "list osGetParcelDetails(key id, list details)"
return_type: "list"
threat_level: ""
energy_cost: ""
sleep_time: ""
wiki_url: "https://opensimulator.org/wiki/osGetParcelDetails"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-18"
last_updated: "2026-03-19"
---

Returns a list with the requested parcel details.

## Syntax

```lsl
list osGetParcelDetails(key id, list details)
```

## Parameters

| Type | Name |
|------|------|
| `key` | `id` |
| `list` | `details` |

## Return Value

`list`

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osGetParcelDetails](https://opensimulator.org/wiki/osGetParcelDetails)
