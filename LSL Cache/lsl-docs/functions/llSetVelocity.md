---
name: "llSetVelocity"
category: "function"
type: "function"
language: "LSL"
description: 'Applies velocity to object

Instantaneous velocity not dependent on object energy or mass.'
signature: "void llSetVelocity(vector velocity, integer local)"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llSetVelocity'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llsetvelocity"]
---

Applies velocity to object

Instantaneous velocity not dependent on object energy or mass.


## Signature

```lsl
void llSetVelocity(vector velocity, integer local);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `vector` | `velocity` |  |
| `integer (boolean)` | `local` |  |


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llSetVelocity)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llSetVelocity) — scraped 2026-03-18_

Applies velocity to object

## Caveats

- Only works in  physics-enabled objects.

## See Also

### Functions

- llSetAngularVelocity
- llApplyImpulse

<!-- /wiki-source -->
