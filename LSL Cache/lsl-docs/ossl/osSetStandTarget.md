---
name: "osSetStandTarget"
category: "function"
type: "function"
language: "OSSL"
description: "Sets the stand offset from the position of the object containing the script."
signature: "void osSetStandTarget(vector v)"
return_type: "void"
threat_level: ""
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osSetStandTarget"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Sets the stand offset from the position of the object containing the script.

## Syntax

```lsl
void osSetStandTarget(vector v)
```

## Parameters

| Type | Name |
|------|------|
| `vector` | `v` |

## Return Value

`void`

## Timing, Energy and Permissions

- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osSetStandTarget](https://opensimulator.org/wiki/osSetStandTarget)
