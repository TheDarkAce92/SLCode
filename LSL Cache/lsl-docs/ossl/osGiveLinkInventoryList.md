---
name: "osGiveLinkInventoryList"
category: "function"
type: "function"
language: "OSSL"
description: "Send a list of inventory items (key) in a given link to a given destination avatar (key) creating a new named folder."
signature: "void osGiveLinkInventoryList(integer linkNumber, key destination, string folderName, list inventory)"
return_type: "void"
threat_level: ""
energy_cost: ""
sleep_time: ""
wiki_url: "https://opensimulator.org/wiki/osGiveLinkInventoryList"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-18"
last_updated: "2026-03-19"
---

Send a list of inventory items (key) in a given link to a given destination avatar (key) creating a new named folder.

## Syntax

```lsl
void osGiveLinkInventoryList(integer linkNumber, key destination, string folderName, list inventory)
```

## Parameters

| Type | Name |
|------|------|
| `integer` | `linkNumber` |
| `key` | `destination` |
| `string` | `folderName` |
| `list` | `inventory` |

## Return Value

`void`

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osGiveLinkInventoryList](https://opensimulator.org/wiki/osGiveLinkInventoryList)
