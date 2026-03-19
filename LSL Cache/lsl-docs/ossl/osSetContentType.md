---
name: "osSetContentType"
category: "function"
type: "function"
language: "OSSL"
description: "Sets the response type of a HTTP request or response"
signature: "void osSetContentType(key id, string type)"
return_type: "void"
threat_level: "Severe"
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osSetContentType"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Sets the response type of a HTTP request or response

## Syntax

```lsl
void osSetContentType(key id, string type)
```

## Parameters

| Type | Name |
|------|------|
| `key` | `id` |
| `string` | `type` |

## Return Value

`void`

## Timing, Energy and Permissions

- **Threat Level:** Severe
- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osSetContentType](https://opensimulator.org/wiki/osSetContentType)
