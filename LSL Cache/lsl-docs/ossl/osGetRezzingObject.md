---
name: "osGetRezzingObject"
category: "function"
type: "function"
language: "OSSL"
description: "Returns the key of the object that rezzed the object the script is in."
signature: "key osGetRezzingObject()"
return_type: "key"
threat_level: "None"
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osGetRezzingObject"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Returns the key of the object that rezzed the object the script is in.

## Syntax

```lsl
key osGetRezzingObject()
```

## Return Value

`key`

## Timing, Energy and Permissions

- **Threat Level:** None
- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osGetRezzingObject](https://opensimulator.org/wiki/osGetRezzingObject)
