---
name: "llPlaySound"
category: "function"
type: "function"
language: "LSL"
description: "Plays attached sound once at volume"
signature: "void llPlaySound(string sound, float volume)"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llPlaySound'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llplaysound"]
---

Plays attached sound once at volume


## Signature

```lsl
void llPlaySound(string sound, float volume);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `string` | `sound` | a sound in the inventory of the prim this script is in or a UUID of a sound |
| `float` | `volume` | between 0.0 (silent) and 1.0 (loud) (0.0 <= volume <= 1.0) |


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llPlaySound)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llPlaySound) — scraped 2026-03-18_

Plays attached sound once at volume

## Caveats

- If sound is missing from the prim's inventory  and it is not a UUID or it is not a sound then an error is shouted on DEBUG_CHANNEL.
- If sound is a UUID then there are no new asset permissions consequences for the object.

  - The resulting object develops no new usage restrictions that might have occurred if the asset had been placed in the prims inventory.
- A call to llPlaySound replaces any other sound (so that only one sound can be played at the same time from the same prim), except sounds started with the deprecated llSound which always plays sound files till the end.
- Sound files must be 30 seconds or shorter.
- Sounds are always sampled at 44.1KHz, 16-bit (unsigned), mono (stereo files will have one channel dropped — merged (as in combined) — when uploading).
- If the object playing the sound is a HUD, the sound is only heard by the user the HUD is attached to.

  - To play a sound inworld from a HUD use llTriggerSound.
- It is impossible to play two (or more) sounds at the same time and have them start playing at exactly the same time ~ [VWR-15663](https://jira.secondlife.com/browse/VWR-15663)

  - If multiple sound emitters play the same exact sound within range of the viewer at the same time, they are usually not in sync due to latency between the server/client and script execution & communication delays. This can produce echoes, odd resonance, and other strange effects that you (probably) do not want.
- When used in conjunction with llSetSoundQueueing, sounds may incorrectly. [play more than once.](https://community.secondlife.com/forums/topic/443645-llplaysound-plays-the-sound-twice-or-more/) This can be fixed by disabling the sound queue if only a single sound sample is to be played.
- Playing sounds is throttled. If the average number of played sounds per second exceeds the limit (22 sounds/s), all sounds from the object are suppressed until the average falls sufficiently. The throttle is per object, not per link or per script, so multiple links cannot be used to overcome the throttle.

  - Once the throttle is hit, the following error will be shown in debug channel: "Too many sound requests.  Throttled until average falls."

## Examples

```lsl
default
 {
     state_entry()
     {
          llPlaySound("some_sound",1.0);
     }
 }
```

## See Also

### Functions

- **llTriggerSound** — Plays a sound unattached.
- llTriggerSoundLimited
- **llLoopSound** — Plays a sound attached.
- llLoopSoundMaster
- llLoopSoundSlave
- llPlaySoundSlave
- **llSetSoundQueueing** — Sets a prim property which allows sounds to be queued, instead of overwriting each other.
- llStopSound
- **llLinkPlaySound** — Plays a sound from a prim in the linkset, with flexible options.
- **llPreloadSound** — Preloads sound on viewers in range.
- **llAdjustSoundVolume** — Adjusts volume of attached sound.

### Articles

| • Sound Clips |  | – | Specifications for uploading sounds. |  |
| --- | --- | --- | --- | --- |

<!-- /wiki-source -->
