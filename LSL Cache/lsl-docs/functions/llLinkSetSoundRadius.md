---
name: "llLinkSetSoundRadius"
category: "function"
type: "function"
language: "LSL"
description: "Establishes a hard cut-off radius for audibility of scripted sounds (both attached and triggered)."
signature: "void llLinkSetSoundRadius(integer link, float radius)"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llLinkSetSoundRadius'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
---

Establishes a hard cut-off radius for audibility of scripted sounds (both attached and triggered).


## Signature

```lsl
void llLinkSetSoundRadius(integer link, float radius);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `integer (link)` | `link` | Link number (0: unlinked, 1: root prim, >1: child prims and seated avatars) or a LINK_* flag |
| `float` | `radius` | in meters |


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llLinkSetSoundRadius)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llLinkSetSoundRadius) — scraped 2026-03-18_

## Caveats

- This function is a prim property, thus will survive script resets.
- Has no effect on llTriggerSound or llLinkPlaySound in triggered mode. Sounds will play regardless of camera position.

  - llTriggerSoundLimited can be used instead for a similar effect but the function depends on **avatar** position, not camera position.
- When used with llPlaySound or llLinkPlaySound in non-looped mode, the sound will be played from the beginning only once, when the observer's camera enters the radius for the first time. This can happen significantly later than a one-off sound was actually played.
- With llLoopSound or llLinkPlaySound in looped mode, the sound will be played from the beginning every time the observer's camera enters the radius.

## Examples

Enable sound cutoff at 4 meters.

```lsl
llSetSoundRadius(4); //Enable sound cutoff at 4 meters.
```

Disable sound cutoff.

```lsl
llSetSoundRadius(0); //Disable sound cutoff.
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
Pass 0 to this function to disable it.

## See Also

### Functions

- **llGetLinkNumber** — prim
- **llGetLinkNumberOfSides** — Returns the number of faces of the linked prim.
- llTriggerSoundLimited

<!-- /wiki-source -->
