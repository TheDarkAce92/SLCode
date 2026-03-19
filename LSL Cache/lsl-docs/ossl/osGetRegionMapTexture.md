---
name: "osGetRegionMapTexture"
category: "function"
type: "function"
language: "OSSL"
description: "Returns the asset UUID of the texture representing the region map tile of a given region name or UUID."
signature: "key osGetRegionMapTexture(string regionNameOrID)"
return_type: "key"
threat_level: "High"
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osGetRegionMapTexture"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Returns the asset UUID of the texture representing the region map tile of a given region name or UUID.

## Syntax

```lsl
key osGetRegionMapTexture(string regionNameOrID)
```

## Parameters

| Type | Name |
|------|------|
| `string` | `regionNameOrID` |

## Return Value

`key`

## Timing, Energy and Permissions

- **Threat Level:** High
- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osGetRegionMapTexture](https://opensimulator.org/wiki/osGetRegionMapTexture)
