---
name: "llLinkStopSound"
category: "function"
type: "function"
language: "LSL"
description: "Stops the attached sound(s) currently playing, if they were started by llLoopSound"
signature: "void llLinkStopSound(integer link)"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llLinkStopSound'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
---

Stops the attached sound(s) currently playing, if they were started by llLoopSound


## Signature

```lsl
void llLinkStopSound(integer link);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `integer (link)` | `link` | Link number (0: unlinked, 1: root prim, >1: child prims and seated avatars) or a LINK_* flag |


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llLinkStopSound)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llLinkStopSound) — scraped 2026-03-18_

## Caveats

- There is no way to stop a specific sound.
- In a linked set use llLinkStopSound to stop sound in a specific prim.

## Examples

```lsl
default
{
    state_entry()
    {
        llLoopSound("string soundname if in object inventory or UUID", 1.0);
    }
    touch_start(integer total_number)
    {
        llStopSound();//As if by magic the sound stops!!
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
- **llSound** — llPlaySound
- llPlaySound
- llPlaySoundSlave
- llLoopSound
- llLoopSoundMaster
- llLoopSoundSlave

<!-- /wiki-source -->
