---
name: "llDamage"
category: "function"
type: "function"
language: "LSL"
description: "This function delivers damage to tasks and agent in the same region."
signature: "void llDamage(key id, float damage, integer damage_type)"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llDamage'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
flags: "experimental"
---

This function delivers damage to tasks and agent in the same region.


## Signature

```lsl
void llDamage(key id, float damage, integer damage_type);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `key` | `target` | The key for the task or avatar that will receive damage. |
| `float` | `damage` | The amount of damage to deliver to the targeted task or avatar. |
| `integer` | `damage_type` | The type of damage to deliver to the targeted task or avatar. |


## Caveats

- Energy cost: **10.0**.
- **Experimental** — behaviour may change.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llDamage)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llDamage) — scraped 2026-03-18_

This function delivers damage to tasks and agent in the same region.

## Caveats

- Calls are throttled to a rate of ≤10/30sec per recipient. Exceptions are:

  - Recipient is avatar of the attachment.
  - Recipient is sitting on the object.
- Triggering the damage throttle will shout an error to the debug channel and the script will continue running.
- The prim containing the script and the prim receiving the damage must both be in damage enable parcels.
- Targeting a seated avatar will redirect damage to the object the avatar is sitting on.



The on_damage event will NOT be triggered if the source of the damage is either:

- An attachment on the avatar.
- An object or vehicle that the avatar is sitting on.

final_damage will be triggered as normal.



The damage throttle is skipped if:

- Damage is negative.
- The source is an attachment on the avatar.
- The source is an object that the avatar is sitting on.
- The source is an object owned by a parcel owner or land group.

## See Also

### Events

- on_damage
- final_damage

### Functions

- llDetectedDamage
- llAdjustDamage

<!-- /wiki-source -->
