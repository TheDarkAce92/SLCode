---
name: "osMessageAttachments"
category: "function"
type: "function"
language: "OSSL"
description: "Sends a message as dataserver event to a given attachment based on the avatar key and attachment point. Can be constrained further with options."
signature: "void osMessageAttachments(key avatar, string message, list attachmentPoints, integer flags)"
return_type: "void"
threat_level: "Moderate"
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osMessageAttachments"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Sends a message as dataserver event to a given attachment based on the avatar key and attachment point. Can be constrained further with options.

## Syntax

```lsl
void osMessageAttachments(key avatar, string message, list attachmentPoints, integer flags)
```

## Parameters

| Type | Name |
|------|------|
| `key` | `avatar` |
| `string` | `message` |
| `list` | `attachmentPoints` |
| `integer` | `flags` |

## Return Value

`void`

## Timing, Energy and Permissions

- **Threat Level:** Moderate
- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osMessageAttachments](https://opensimulator.org/wiki/osMessageAttachments)
