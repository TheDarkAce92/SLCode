---
name: "osGetGender"
category: "function"
type: "function"
language: "OSSL"
description: "Returns the gender of a given avatar as string."
signature: "string osGetGender(key rawAvatarId)"
return_type: "string"
threat_level: "None"
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osGetGender"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Returns the gender of a given avatar as string.

## Syntax

```lsl
string osGetGender(key rawAvatarId)
```

## Parameters

| Type | Name |
|------|------|
| `key` | `rawAvatarId` |

## Return Value

`string`

## Timing, Energy and Permissions

- **Threat Level:** None
- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osGetGender](https://opensimulator.org/wiki/osGetGender)
