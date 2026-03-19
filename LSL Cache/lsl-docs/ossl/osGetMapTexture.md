---
name: "osGetMapTexture"
category: "function"
type: "function"
language: "OSSL"
description: "Returns the asset UUID of the texture representing the region map tile of the current region."
signature: "key osGetMapTexture()"
return_type: "key"
threat_level: ""
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osGetMapTexture"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Returns the asset UUID of the texture representing the region map tile of the current region.

## Syntax

```lsl
key osGetMapTexture()
```

## Return Value

`key`

## Timing, Energy and Permissions

- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osGetMapTexture](https://opensimulator.org/wiki/osGetMapTexture)
