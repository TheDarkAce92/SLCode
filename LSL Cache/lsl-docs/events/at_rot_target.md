---
name: "at_rot_target"
category: "event"
type: "event"
language: "LSL"
description: "Result of llRotTarget library function call"
signature: "at_rot_target(integer handle, rotation targetrot, rotation ourrot)"
wiki_url: 'https://wiki.secondlife.com/wiki/at_rot_target'
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
deprecated: "false"
parameters: []
---

Result of llRotTarget library function call


## Signature

```lsl
at_rot_target(integer handle, rotation targetrot, rotation ourrot)
{
    // your code here
}
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `integer` | `handle` | llRotTarget return |
| `rotation` | `targetrot` | llRotTarget rot parameter |
| `rotation` | `ourrot` | current rotation (similar to llGetRot) |


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/at_rot_target)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/at_rot_target) — scraped 2026-03-18_

## Examples

For an example, see llRotTarget

## See Also

### Events

- not_at_rot_target
- at_target
- not_at_target

### Functions

- **llTarget** — Setup a target position
- **llTargetRemove** — Stop a target position
- **llRotTarget** — Setup a target rotation
- **llRotTargetRemove** — Stop a target rotation

<!-- /wiki-source -->
