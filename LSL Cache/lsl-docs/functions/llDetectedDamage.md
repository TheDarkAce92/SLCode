---
name: "llDetectedDamage"
category: "function"
type: "function"
language: "LSL"
description: "Returns damage information for a detected object at the given index, used with damage-related events."
signature: "list llDetectedDamage(integer index)"
return_type: "list"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llDetectedDamage'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
flags: "experimental"
---


## Signature

```lsl
list llDetectedDamage(integer index);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `integer` | `number` | Index of detection information  |


## Return Value

Returns `list`.


## Caveats

- Energy cost: **10.0**.
- **Experimental** — behaviour may change.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llDetectedDamage)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llDetectedDamage) — scraped 2026-03-18_

Returns a list containing pending damage information.

## See Also

### Events

- on_damage

### Functions

- llAdjustDamage

<!-- /wiki-source -->
