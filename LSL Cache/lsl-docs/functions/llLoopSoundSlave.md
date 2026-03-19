---
name: "llLoopSoundSlave"
category: "function"
type: "function"
language: "LSL"
description: "Plays attached sound looping at volume, synced to most audible sync master declared by llLoopSoundMaster."
signature: "void llLoopSoundSlave(string sound, float volume)"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llLoopSoundSlave'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llloopsoundslave"]
---

Plays attached sound looping at volume, synced to most audible sync master declared by llLoopSoundMaster.


## Signature

```lsl
void llLoopSoundSlave(string sound, float volume);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `string` | `sound` | a sound in the inventory of the prim this script is in or a UUID of a sound |
| `float` | `volume` | between 0.0 (silent) and 1.0 (loud) (0.0 <= volume <= 1.0) |


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llLoopSoundSlave)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llLoopSoundSlave) — scraped 2026-03-18_

Plays attached sound looping at volume, synced to most audible sync master declared by llLoopSoundMaster.

## Caveats

- If sound is missing from the prim's inventory  and it is not a UUID or it is not a sound then an error is shouted on DEBUG_CHANNEL.
- If sound is a UUID then there are no new asset permissions consequences for the object.

  - The resulting object develops no new usage restrictions that might have occurred if the asset had been placed in the prims inventory.
- As an object can only have a single active sound, llLoopSoundSlave() should be called from a different prim than the one that defined a sync master, otherwise it will remove the master sound, and no sound will be available to sync-to.

## Examples

```lsl
default
{
   state_entry()
   {
      llLoopSoundSlave("sound name",.05);
   }
}
```

## See Also

### Functions

- **llPlaySound** — Plays a sound attached once.
- llPlaySoundSlave
- **llLoopSound** — Plays a sound attached indefinitely.
- llLoopSoundMaster
- **llTriggerSound** — Plays a sound unattached.
- llTriggerSoundLimited

<!-- /wiki-source -->
