---
name: "osMessageObject"
category: "function"
type: "function"
language: "OSSL"
description: "Directly send a message as dataserver event to a given object by its key."
signature: "void osMessageObject(key objectUUID, string message)"
return_type: "void"
threat_level: "Low"
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osMessageObject"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Directly send a message as dataserver event to a given object by its key.

## Syntax

```lsl
void osMessageObject(key objectUUID, string message)
```

## Parameters

| Type | Name |
|------|------|
| `key` | `objectUUID` |
| `string` | `message` |

## Return Value

`void`

## Timing, Energy and Permissions

- **Threat Level:** Low
- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osMessageObject](https://opensimulator.org/wiki/osMessageObject)
