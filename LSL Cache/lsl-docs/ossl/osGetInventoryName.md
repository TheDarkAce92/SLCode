---
name: "osGetInventoryName"
category: "function"
type: "function"
language: "OSSL"
description: "Returns the name of a given inventory item key in the object containing the script."
signature: "string osGetInventoryName(key itemId)"
return_type: "string"
threat_level: ""
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osGetInventoryName"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Returns the name of a given inventory item key in the object containing the script.

## Syntax

```lsl
string osGetInventoryName(key itemId)
```

## Parameters

| Type | Name |
|------|------|
| `key` | `itemId` |

## Return Value

`string`

## Timing, Energy and Permissions

- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osGetInventoryName](https://opensimulator.org/wiki/osGetInventoryName)
