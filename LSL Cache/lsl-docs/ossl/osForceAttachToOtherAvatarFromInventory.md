---
name: "osForceAttachToOtherAvatarFromInventory"
category: "function"
type: "function"
language: "OSSL"
description: "Forcefully attaches an object from the inventory of the object containing this script to a given attachment point of a given avatar bypassing attach permissions."
signature: "void osForceAttachToOtherAvatarFromInventory(string rawAvatarId, string itemName, integer attachmentPoint)"
return_type: "void"
threat_level: "VeryHigh"
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osForceAttachToOtherAvatarFromInventory"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Forcefully attaches an object from the inventory of the object containing this script to a given attachment point of a given avatar bypassing attach permissions.

## Syntax

```lsl
void osForceAttachToOtherAvatarFromInventory(string rawAvatarId, string itemName, integer attachmentPoint)
```

## Parameters

| Type | Name |
|------|------|
| `string` | `rawAvatarId` |
| `string` | `itemName` |
| `integer` | `attachmentPoint` |

## Return Value

`void`

## Timing, Energy and Permissions

- **Threat Level:** VeryHigh
- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osForceAttachToOtherAvatarFromInventory](https://opensimulator.org/wiki/osForceAttachToOtherAvatarFromInventory)
