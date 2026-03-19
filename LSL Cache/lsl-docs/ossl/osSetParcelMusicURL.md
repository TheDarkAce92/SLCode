---
name: "osSetParcelMusicURL"
category: "function"
type: "function"
language: "OSSL"
description: "Sets the current parcel music URL."
signature: "void osSetParcelMusicURL(string url)"
return_type: "void"
threat_level: "VeryLow"
energy_cost: "10.0"
sleep_time: "0.0"
wiki_url: "https://opensimulator.org/wiki/osSetParcelMusicURL"
source: "opensim/opensim GitHub (IOSSL_Api.cs)"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Sets the current parcel music URL.

## Syntax

```lsl
void osSetParcelMusicURL(string url)
```

## Parameters

| Type | Name |
|------|------|
| `string` | `url` |

## Return Value

`void`

## Timing, Energy and Permissions

- **Threat Level:** VeryLow
- **Forced Delay:** 0.0 seconds
- **Energy:** 10.0

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- Reference: [https://opensimulator.org/wiki/osSetParcelMusicURL](https://opensimulator.org/wiki/osSetParcelMusicURL)
