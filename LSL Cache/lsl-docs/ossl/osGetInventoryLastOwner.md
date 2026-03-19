---
name: "osGetInventoryLastOwner"
category: "function"
type: "function"
language: "OSSL"
description: "Returns the last owner (key) of a given inventory item (name or key) of the object containing the script."
signature: "key osGetInventoryLastOwner(string itemNameOrId)"
return_type: "key"
threat_level: ""
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osGetInventoryLastOwner"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Returns the last owner (key) of a given inventory item (name or key) of the object containing the script.

## Syntax

```lsl
key osGetInventoryLastOwner(string itemNameOrId)
```

## Parameters

| Type | Name |
|------|------|
| `string` | `itemNameOrId` |

## Return Value

`key`

## Timing, Energy and Permissions

- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osGetInventoryLastOwner](https://opensimulator.org/wiki/osGetInventoryLastOwner)
