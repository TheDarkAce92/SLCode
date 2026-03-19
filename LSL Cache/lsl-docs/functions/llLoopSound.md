---
name: "llLoopSound"
category: "function"
type: "function"
language: "LSL"
description: "Plays attached sound looping indefinitely at volume"
signature: "void llLoopSound(string sound, float volume)"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llLoopSound'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llloopsound"]
---

Plays attached sound looping indefinitely at volume


## Signature

```lsl
void llLoopSound(string sound, float volume);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `string` | `sound` | a sound in the inventory of the prim this script is in or a UUID of a sound |
| `float` | `volume` | between 0.0 (silent) and 1.0 (loud) (0.0 <= volume <= 1.0) |


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llLoopSound)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llLoopSound) — scraped 2026-03-18_

Plays attached sound looping indefinitely at volume

## Caveats

- If sound is missing from the prim's inventory  and it is not a UUID or it is not a sound then an error is shouted on DEBUG_CHANNEL.
- If sound is a UUID then there are no new asset permissions consequences for the object.

  - The resulting object develops no new usage restrictions that might have occurred if the asset had been placed in the prims inventory.
- A call to llLoopSound replaces any other sound (so that only one sound can be played at the same time from the same prim, except sounds started with the deprecated llSound which always plays sound files till the end. An object can play 2 sounds with llLoopSound if the function is called from different prims
- If a second call to loop the same sound at a different volume is made from within the same script NO volume change is made.

  - llStopSound set just previous to the second call for a new volume allows the volume change with no discernible pause.
- When call made from HUD attachment sound is only heard by agent the task is attached to.

## Examples

```lsl
llLoopSound("ambient.wav", 0.5);
```

## See Also

### Functions

- **llLoopSoundMaster** — Plays a sound attached indefinitely.
- llLoopSoundSlave
- **llStopSound** — Stops playing a looped sound.
- **llPlaySound** — Plays a sound attached once.
- **llTriggerSound** — Plays a sound unattached.
- llTriggerSoundLimited

<!-- /wiki-source -->
