---
name: "osGetAvatarHomeURI"
category: "function"
type: "function"
language: "OSSL"
description: "Tries to determine the home grid URI of an avatar."
signature: "string osGetAvatarHomeURI(string uuid)"
return_type: "string"
threat_level: "Low"
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osGetAvatarHomeURI"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Tries to determine the home grid URI of an avatar.

## Syntax

```lsl
string osGetAvatarHomeURI(string uuid)
```

## Parameters

| Type | Name |
|------|------|
| `string` | `uuid` |

## Return Value

`string`

## Timing, Energy and Permissions

- **Threat Level:** Low
- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osGetAvatarHomeURI](https://opensimulator.org/wiki/osGetAvatarHomeURI)
