---
name: "llAdjustSoundVolume"
category: "function"
type: "function"
language: "LSL"
description: "Adjusts volume of attached sound."
signature: "void llAdjustSoundVolume(float volume)"
return_type: "void"
sleep_time: "0.1"
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llAdjustSoundVolume'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["lladjustsoundvolume"]
---

Adjusts volume of attached sound.


## Signature

```lsl
void llAdjustSoundVolume(float volume);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `float` | `volume` | Volume level, 0.0 (silent) to 1.0 (loudest) |


## Caveats

- Forced delay: **0.1 seconds** — the script sleeps after each call.
- Energy cost: **10.0**.
- Does not affect sounds played with `llTriggerSound` or `llCollisionSound`.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llAdjustSoundVolume)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llAdjustSoundVolume) — scraped 2026-03-18_

## Caveats

Not work llTriggerSound and llCollisionSound

## Examples

```lsl
default
{
    state_entry()
    {
        llListen(42, "", llGetOwner(), "");
    }

    listen(integer chan, string name, key id, string msg)
    {
        float value = (float)msg;
        llAdjustSoundVolume(value);
        llOwnerSay("Volume set to: " + (string)value + " of 1.0");
    }
}
```

```lsl
default
{
    collision_start(integer p)
    {
        llPlaySound("5df2e97f-d3ab-9a80-7063-69007470a182", 1.0);
        llAdjustSoundVolume(1.0);
        llSetTimerEvent(0.2); //In 0.2 seconds, will reduce the volume of the currently playing audio.
    }
    timer(){
        llAdjustSoundVolume(0.1);
        llSetTimerEvent(0.0);
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
- llLinkPlaySound
- llLinkSetSoundQueueing
- llLinkSetSoundRadius
- llLinkStopSound
- llLoopSound
- llLoopSoundMaster
- llLoopSoundSlave
- llPlaySound
- llPlaySoundSlave
- llPreloadSound
- llSetSoundQueueing
- llSetSoundRadius
- llSound
- llSoundPreload
- llStopSound
- llTriggerSound
- llTriggerSoundLimited

<!-- /wiki-source -->
