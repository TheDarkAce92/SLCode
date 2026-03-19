---
name: "osAvatarName2Key"
category: "function"
type: "function"
language: "OSSL"
description: "Returns the avatar key, based on their first and last name."
signature: "string osAvatarName2Key(string firstname, string lastname)"
return_type: "string"
threat_level: "Low"
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osAvatarName2Key"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Returns the avatar key, based on their first and last name.

## Syntax

```lsl
string osAvatarName2Key(string firstname, string lastname)
```

## Parameters

| Type | Name |
|------|------|
| `string` | `firstname` |
| `string` | `lastname` |

## Return Value

`string`

## Timing, Energy and Permissions

- **Threat Level:** Low
- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osAvatarName2Key](https://opensimulator.org/wiki/osAvatarName2Key)
