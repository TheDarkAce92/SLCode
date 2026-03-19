---
name: "osGetNumberOfAttachments"
category: "function"
type: "function"
language: "OSSL"
description: "Returns the number of attachments attached to a list of attachment points of a given avatar."
signature: "list osGetNumberOfAttachments(key avatar, list attachmentPoints)"
return_type: "list"
threat_level: "Moderate"
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osGetNumberOfAttachments"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Returns the number of attachments attached to a list of attachment points of a given avatar.

## Syntax

```lsl
list osGetNumberOfAttachments(key avatar, list attachmentPoints)
```

## Parameters

| Type | Name |
|------|------|
| `key` | `avatar` |
| `list` | `attachmentPoints` |

## Return Value

`list`

## Timing, Energy and Permissions

- **Threat Level:** Moderate
- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osGetNumberOfAttachments](https://opensimulator.org/wiki/osGetNumberOfAttachments)
