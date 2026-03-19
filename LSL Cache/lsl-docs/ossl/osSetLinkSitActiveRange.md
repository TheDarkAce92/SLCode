---
name: "osSetLinkSitActiveRange"
category: "function"
type: "function"
language: "OSSL"
description: "Sets the max distance for allowing avatars to sit on a given link.."
signature: "void osSetLinkSitActiveRange(integer linkNumber, float v)"
return_type: "void"
threat_level: ""
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osSetLinkSitActiveRange"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Sets the max distance for allowing avatars to sit on a given link..

## Syntax

```lsl
void osSetLinkSitActiveRange(integer linkNumber, float v)
```

## Parameters

| Type | Name |
|------|------|
| `integer` | `linkNumber` |
| `float` | `v` |

## Return Value

`void`

## Timing, Energy and Permissions

- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osSetLinkSitActiveRange](https://opensimulator.org/wiki/osSetLinkSitActiveRange)
