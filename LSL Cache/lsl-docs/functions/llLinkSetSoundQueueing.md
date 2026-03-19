---
name: "llLinkSetSoundQueueing"
category: "function"
type: "function"
language: "LSL"
description: "Set whether attached sounds wait for the current sound to finish. If queue is TRUE, queuing is enabled, if FALSE queuing is disabled. Sound queuing is disabled by default."
signature: "void llLinkSetSoundQueueing(integer link, integer queue)"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llLinkSetSoundQueueing'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
---

Set whether attached sounds wait for the current sound to finish. If queue is TRUE, queuing is enabled, if FALSE queuing is disabled. Sound queuing is disabled by default.


## Signature

```lsl
void llLinkSetSoundQueueing(integer link, integer queue);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `integer (link)` | `link` | Link number (0: unlinked, 1: root prim, >1: child prims and seated avatars) or a LINK_* flag |
| `integer (boolean)` | `queue` | boolean, sound queuing: TRUE enables, FALSE (default) disables |


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llLinkSetSoundQueueing)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llLinkSetSoundQueueing) — scraped 2026-03-18_

## Caveats

- The sound queue is only 1 level deep - this means that beside the sound that is currently playing, there can only be 1 sound in reserve. The sound queue is first-come, first-serve.* SVC-4260
- Further to the above, the queue order is reversed when using llPlaySoundSlave - using the below example, the default behaviour would be to play SoundName1 and SoundName2, however when using the aforementioned function the order would be to play SoundName2 and SoundName3.
- Sound queuing is a property of the prim, not the script. It can be activated and deactivated by any script in the prim and survives script reset, re-rez and script removal.
- If used to make smooth transitions using slave/master sounds the sounds tend to go out of sync.
- Although sounds are queued, the volume of all sounds in the queue is set by the last item in the queue. If your application requires the use of differing volume values, you may wish to implement llAdjustSoundVolume alongside the sound queue
- There is a very small (but audible) gap of silence between sounds due to network latency and processing time.
- The queued sound must be fully loaded in the viewer, or else it will not play. llPreloadSound is not always reliable in doing its job.
- Queueing a sound that is identical to the one currently playing will fail. Use llLoopSound instead.
- While this function does not have a delay, enabling or disabling the sound queue is not instant. It seems to take approx ~0.1 seconds to set the queueing flag.

## Examples

```lsl
default
{
    state_entry()
    {
        llPreloadSound("SoundName1");//This loads the sounds into all in range viewers and cuts delay between sounds.
        llPreloadSound("SoundName2");//All sound parameters can be the name of a sound in the prim's inventory or a UUID of a sound");
        llPreloadSound("SoundName3"); //This sound will be skipped, as the queue is only 1 level deep.
    }
    touch_start(integer detected)
    {
        llSetSoundQueueing(TRUE);//Set to TRUE for queueing and SoundName2 plays after the SoundName1 has ended.
        //Set to FALSE only the second will be played since the prim has only one sound emitter and the second was called last.
        //Can be set anywhere within the script (if within an event it will activate when the event is triggered.
        llPlaySound("SoundName1", 1.0);
        llPlaySound("SoundName2", 1.0);
        llPlaySound("SoundName3", 1.0); //This sound isn't played as the queue is already full, so this is discarded.
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
- llLoopSound
- **llLoopSoundSlave** — Plays a looped sound attached, synced with the master.
- **llPlaySoundSlave** — Plays a sound once attached, synced with the master.
- **llAdjustSoundVolume** — Adjusts the volume of playing sound(s).

<!-- /wiki-source -->
