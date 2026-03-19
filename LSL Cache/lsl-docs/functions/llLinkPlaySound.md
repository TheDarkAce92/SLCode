---
name: "llLinkPlaySound"
category: "function"
type: "function"
language: "LSL"
description: "Plays attached sound once at volume"
signature: "void llLinkPlaySound(integer link, string sound, float volume, integer flags)"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llLinkPlaySound'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
---

Plays attached sound once at volume


## Signature

```lsl
void llLinkPlaySound(integer link, string sound, float volume, integer flags);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `integer (link)` | `link` | Link number (0: unlinked, 1: root prim, >1: child prims and seated avatars) or a LINK_* flag |
| `string` | `sound` | a sound in the inventory of the prim this script is in or a UUID of a sound |
| `float` | `volume` | between 0.0 (silent) and 1.0 (loud) (0.0 <= volume <= 1.0) |
| `integer` | `flags` | Bit flags used to control how the sound is played. |


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llLinkPlaySound)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llLinkPlaySound) — scraped 2026-03-18_

Plays attached sound once at volume

## Caveats

- If sound is missing from the prim's inventory  and it is not a UUID or it is not a sound then an error is shouted on DEBUG_CHANNEL.
- If sound is a UUID then there are no new asset permissions consequences for the object.

  - The resulting object develops no new usage restrictions that might have occurred if the asset had been placed in the prims inventory.
- A call to llPlaySound replaces any other sound (so that only one sound can be played at the same time from the same prim), except sounds started with the deprecated llSound which always plays sound files till the end.
- Sound files must be 30 seconds or shorter.
- Sounds are always sampled at 44.1KHz, 16-bit, mono (stereo files will have one channel dropped--merged (as in combined)--when uploading).
- If the object playing the sound is a HUD, the sound is only heard by the user the HUD is attached to.

  - To play a sound inworld from a HUD use llTriggerSound.
- It is impossible to play two (or more) sounds at the same time and have them start playing at exactly the same time ~ [VWR-15663](https://jira.secondlife.com/browse/VWR-15663)

  - If multiple sound emitters play the same exact sound within range of the viewer at the same time, they are usually not in sync due to latency between the server/client and script execution & communication delays. This can produce echos, odd resonance, and other strange effects that you (probably) do not want.
- When used in conjunction with llSetSoundQueueing, sounds may incorrectly [play more than once.](https://community.secondlife.com/forums/topic/443645-llplaysound-plays-the-sound-twice-or-more/) This can be fixed by disabling the sound queue if only a single sound sample is to be played.
- Use llLinkStopSound to stop a looped sound started in a link with SOUND_LOOP.
- Playing sounds is throttled. If the average number of played sounds per second exceeds the limit (22 sounds/s), all sounds from the object are suppressed until the average falls sufficiently. The throttle is per object, not per link or per script, so multiple links cannot be used to overcome the throttle.

  - Once the throttle is hit, the following error will be shown in debug channel: "Too many sound requests.  Throttled until average falls."

## Examples

```lsl
default
 {
     state_entry()
     {
          llLinkPlaySound(LINK_ROOT, "some_sound", 1.0, SOUND_PLAY);
     }
 }
```

## Notes

### Link Numbers

Each prim that makes up an object has an address, a link number. To access a specific prim in the object, the prim's link number must be known. In addition to prims having link numbers, avatars seated upon the object do as well.

- If an object consists of only one prim, and there are no avatars seated upon it, the (root) prim's link number is zero.
- However, if the object is made up of multiple prims or there is an avatar seated upon the object, the root prim's link number is one.

When an avatar sits on an object, it is added to the end of the link set and will have the largest link number. In addition to this, while an avatar is seated upon an object, the object is unable to link or unlink prims without unseating all avatars first.

#### Counting Prims & Avatars

There are two functions of interest when trying to find the number of prims and avatars on an object.

- `llGetNumberOfPrims()` - Returns the number of prims and seated avatars.
- `llGetObjectPrimCount(llGetKey())` - Returns only the number of prims in the object but will return zero for attachments.

```lsl
integer GetPrimCount() { //always returns only the number of prims
    if(llGetAttached())//Is it attached?
        return llGetNumberOfPrims();//returns avatars and prims but attachments can't be sat on.
    return llGetObjectPrimCount(llGetKey());//returns only prims but won't work on attachments.
}
```

See llGetNumberOfPrims for more about counting prims and avatars.

#### Errata

If a script located in a child prim erroneously attempts to access link 0, it will get or set the property of the linkset's root prim.  This bug ([BUG-5049](https://jira.secondlife.com/browse/BUG-5049)) is preserved for broken legacy scripts.

## See Also

### Functions

- **llGetLinkNumber** — prim
- **llGetLinkNumberOfSides** — Returns the number of faces of the linked prim.
- **llGetLinkNumberOfSides** — Returns the number of faces of the linked prim.
- **llTriggerSound** — Plays a sound unattached.
- llTriggerSoundLimited
- **llLoopSound** — Plays a sound attached.
- llLoopSoundMaster
- llLoopSoundSlave
- llPlaySoundSlave
- **llSetSoundQueueing** — Sets a prim property which allows sounds to be queued, instead of overwriting eachother.
- llStopSound
- llLinkStopSound
- **llPreloadSound** — Preloads sound on viewers within range.
- **llLinkAdjustSoundVolume** — Adjusts volume of attached sound.

<!-- /wiki-source -->
