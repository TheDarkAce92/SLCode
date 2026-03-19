---
name: "llSoundPreload"
category: "function"
type: "function"
language: "LSL"
description: "Preloads sound on viewers within range."
signature: "void llSoundPreload(string sound)"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llSoundPreload'
deprecated: "true"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
---

Preloads sound on viewers within range.


## Signature

```lsl
void llSoundPreload(string sound);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `string` | `sound` | a sound in the inventory of the prim this script is in or a UUID of a sound |


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llSoundPreload)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llSoundPreload) — scraped 2026-03-18_

Preloads sound on viewers within range.

## Caveats

- This function has been deprecated, please use llPreloadSound instead.
- If sound is missing from the prim's inventory  and it is not a UUID or it is not a sound then an error is shouted on DEBUG_CHANNEL.
- If sound is a UUID then there are no new asset permissions consequences for the object.

  - The resulting object develops no new usage restrictions that might have occurred if the asset had been placed in the prims inventory.

<!-- /wiki-source -->
