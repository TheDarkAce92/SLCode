---
name: "llTriggerSound"
category: "function"
type: "function"
language: "LSL"
description: 'Plays sound at volume, centered at but not attached to object.

If the object moves the sound does not move with it.
Use llPlaySound to play a sound attached to the object.'
signature: "void llTriggerSound(string sound, float volume)"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llTriggerSound'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["lltriggersound"]
---

Plays sound at volume, centered at but not attached to object.

If the object moves the sound does not move with it.
Use llPlaySound to play a sound attached to the object.


## Signature

```lsl
void llTriggerSound(string sound, float volume);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `string` | `sound` | a sound in the inventory of the prim this script is in or a UUID of a sound |
| `float` | `volume` | between 0.0 (silent) and 1.0 (loud) (0.0 <= volume <= 1.0) |


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llTriggerSound)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llTriggerSound) — scraped 2026-03-18_

Plays sound at volume, centered at but not attached to object.

## Caveats

- If sound is missing from the prim's inventory  and it is not a UUID or it is not a sound then an error is shouted on DEBUG_CHANNEL.
- If sound is a UUID then there are no new asset permissions consequences for the object.

  - The resulting object develops no new usage restrictions that might have occurred if the asset had been placed in the prims inventory.
- Sounds played from a HUD using llTriggerSound are audible inworld. To make sounds from a HUD audible only to the wearer, use llPlaySound.
- Playing sounds is throttled. If the average number of played sounds per second exceeds the limit (22 sounds/s), all sounds from the object are suppressed until the average falls sufficiently. The throttle is per object, not per link or per script, so multiple links cannot be used to overcome the throttle.

  - Once the throttle is hit, the following error will be shown in debug channel: "Too many sound requests.  Throttled until average falls."

## Examples

```lsl
//When touched, object containing this script will trigger the sound entered.
//This function allows object to trigger sound even if attached to an avatar (AGENT)
//Creator: TonyH Wrangler

string sound = "ed124764-705d-d497-167a-182cd9fa2e6c"; //uuid or name of item in inventory

default
{
    touch_start(integer total_num)
    {
        llTriggerSound(sound, 1.0);
    }
}
```

## See Also

### Functions

- llPlaySound
- llTriggerSoundLimited
- **llLinkPlaySound** — Can be used to trigger sounds in other prims in the linkset.

<!-- /wiki-source -->
