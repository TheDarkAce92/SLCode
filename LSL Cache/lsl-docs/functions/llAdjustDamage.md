---
name: "llAdjustDamage"
category: "function"
type: "function"
language: "LSL"
description: "The llAdjustDamage modifies the amount of damage that will be applied by the current on_damage event after it has completed processing. "
signature: "void llAdjustDamage(integer index, float damage)"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llAdjustDamage'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
flags: "experimental"
---

The llAdjustDamage modifies the amount of damage that will be applied by the current on_damage event after it has completed processing. 


## Signature

```lsl
void llAdjustDamage(integer index, float damage);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `integer` | `number` | The index of the damage event to be modified. |
| `float` | `new_damage` | A new damage value to be applied or distributed after on_damage processing. |


## Caveats

- Energy cost: **10.0**.
- **Experimental** — behaviour may change.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llAdjustDamage)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llAdjustDamage) — scraped 2026-03-18_

The llAdjustDamage modifies the amount of damage that will be applied by the current on_damage event after it has completed processing.

## Caveats

- Calling this function from any event handler other than on_damage results in an error message being shouted to the debug channel.

  - Requires the region to allow damage adjustment for the on_damage event to run
- Negative indexes are not supported.
- Indexes that are out of range will silently fail.

## See Also

### Events

- on_damage

### Functions

- llDetectedDamage

<!-- /wiki-source -->
