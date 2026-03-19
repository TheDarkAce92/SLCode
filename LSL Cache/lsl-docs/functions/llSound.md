---
name: "llSound"
category: "function"
type: "function"
language: "LSL"
description: "Plays sound at volume and whether it should loop or not."
signature: "void llSound(string sound, float volume, integer queue, integer loop)"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llSound'
deprecated: "true"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
---

Plays sound at volume and whether it should loop or not.


## Signature

```lsl
void llSound(string sound, float volume, integer queue, integer loop);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `string` | `sound` | a sound in the inventory of the prim this script is in or a UUID of a sound |
| `float` | `volume` | between 0.0 (silent) and 1.0 (loud) (0.0 <= volume <= 1.0) |
| `integer` | `queue` | boolean, whether or not to queue the song (TRUE) or interrupt the playing song (FALSE). |
| `integer` | `loop` | boolean, whether or not to loop the song. |


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llSound)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llSound) — scraped 2026-03-18_

Plays sound at volume and whether it should loop or not.

## Caveats

- This function has been deprecated, please use llPlaySound instead.
- If sound is missing from the prim's inventory  and it is not a UUID or it is not a sound then an error is shouted on DEBUG_CHANNEL.
- If sound is a UUID then there are no new asset permissions consequences for the object.

  - The resulting object develops no new usage restrictions that might have occurred if the asset had been placed in the prims inventory.

## Examples

```lsl
default
{
    state_entry()
    {
        llSound("sound",1.0,TRUE,FALSE);
        //Plays the sound once.
    }
}
```

<!-- /wiki-source -->
