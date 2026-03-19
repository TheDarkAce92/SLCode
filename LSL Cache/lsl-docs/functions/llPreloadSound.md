---
name: "llPreloadSound"
category: "function"
type: "function"
language: "LSL"
description: "Preloads sound on viewers within range"
signature: "void llPreloadSound(string sound)"
return_type: "void"
sleep_time: "1.0"
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llPreloadSound'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llpreloadsound"]
---

Preloads sound on viewers within range


## Signature

```lsl
void llPreloadSound(string sound);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `string` | `sound` | a sound in the inventory of the prim this script is in or a UUID of a sound |


## Caveats

- Forced delay: **1.0 seconds** — the script sleeps after each call.
- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llPreloadSound)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llPreloadSound) — scraped 2026-03-18_

Preloads sound on viewers within range

## Caveats

- This function causes the script to sleep for 1.0 seconds.
- If sound is missing from the prim's inventory  and it is not a UUID or it is not a sound then an error is shouted on DEBUG_CHANNEL.
- If sound is a UUID then there are no new asset permissions consequences for the object.

  - The resulting object develops no new usage restrictions that might have occurred if the asset had been placed in the prims inventory.

## Examples

```lsl
//Will preload a sound when rezzed, then play it when 'touched'.
string sound = "name or uuid";//sound in inventory or UUID of a sound.

default
{
    on_rez(integer start_param)
    {
        llSetText("Preloading....",<1,0,0>,1);
        llPreloadSound(sound);
        llSetText("Touch To Play",<1,1,1>,1);
    }
    touch_start(integer num_detected)
    {
        llPlaySound(sound, 1.0);
    }
}
```

<!-- /wiki-source -->
