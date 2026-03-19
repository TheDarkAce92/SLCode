---
name: "llSetDamage"
category: "function"
type: "function"
language: "LSL"
description: "Sets the amount of damage that will be done when this object hits an avatar."
signature: "void llSetDamage(float damage)"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llSetDamage'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llsetdamage"]
---

Sets the amount of damage that will be done when this object hits an avatar.


## Signature

```lsl
void llSetDamage(float damage);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `float` | `damage` | Damage amount. Negative values heal the avatar. Values ≥ 100.0 instantly kill a fully healthy avatar. No upper bound enforced. |


## Caveats

- Energy cost: **10.0**.
- `damage` is a prim property — persists even if the script is not running.
- Values ≥ 100.0 instantly kill even a fully healthy avatar; no upper cap is enforced.
- Negative values heal the avatar by the specified amount.
- If a damage-enabled object hits a physical object with seated avatars, damage is distributed to all seated avatars.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llSetDamage)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llSetDamage) — scraped 2026-03-18_

Sets the amount of damage that will be done when this object hits an avatar.

## Caveats

- damage is a Prim Property, and may be applied even if there is no running script.
- If damage is 100.0 or greater, the object will instantly kill even a fully healthy avatar.
- If damage is less than zero, the avatar will he healed for the indicated amount.
- If a damage enabled object hits a physics enabled object that one or more avatars are sitting on, damage will be distributed to all seated avatars.

## Examples

```lsl
//Simple autokiller bullet:
// This will instantly "kill" on collision if contact is made with avatar on damage enabled land.

default
{
    on_rez(integer param) // Becomes active when rezzed.
    {
        llSetDamage(100.0); // Set the damage to maximum.
        llSensor("", "", AGENT, 96.0, PI); // Sweep a 96 meter sphere searching for agents.
    }
    sensor(integer num) // If an agent is detected...
    {
        llSetStatus(STATUS_PHYSICS, TRUE); // Enable physics to allow physical movement.
        llSetTimerEvent(10.0); // Set a 10 second timer.
        llMoveToTarget(llDetectedPos(0), 0.5); // Move to the detected position.
    }
    no_sensor() // If no agents are detected...
    {
        llDie(); // Auto destruct.
    }
    timer() // If we missed our target...
    {
        llDie(); // Auto destruct.
    }
}
```

## See Also

### Articles

- **Damage** — How damage works in Second Life
- **Death** — The concept of death in Second Life
- **Combat** — Combat in Second Life
- **Weapon** — Weapons in Second Life

<!-- /wiki-source -->
