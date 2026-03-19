---
name: "llStopObjectAnimation"
category: "function"
type: "function"
language: "LSL"
description: "Stop an animation for the current object."
signature: "void llStopObjectAnimation(string anim)"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llStopObjectAnimation'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
---

Stop an animation for the current object.


## Signature

```lsl
void llStopObjectAnimation(string anim);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `string` | `anim` | name of an animation in the inventory of the current object, or an animation uuid |


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llStopObjectAnimation)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llStopObjectAnimation) — scraped 2026-03-18_

Stop an animation for the current object.

## Examples

```lsl
default
{
    state_entry()
    {
    }

    // This assumes that an animation called "MyFancyWalk" is present in the inventory of the current object.
    touch_start(integer total_number)
    {
        llSay(0, "Starting animation");
        llStartObjectAnimation("MyFancyWalk");
    }

    touch_end(integer total_number)
    {
        llSay(0, "Stopping animation");
        llStopObjectAnimation("MyFancyWalk");
    }
}
```

## Notes

Animated objects work by associating a skeleton with a linkset containing one or more rigged mesh primitives. When animations are played by a script in any of the prims in the linkset, the skeleton will animate and any rigged meshes in the linkset will move accordingly. A script running in any prim of the linkset can start, stop or query animations using the new commands. The typical usage of these functions is to do all object animation scripting in the root prim of the linkset; in this scenario, the animations and scripts would all be part of the inventory of this prim, and so of the object as a whole. However, if scripts and animations are present in multiple prims of a linkset, it is important to understand that animations are started, stopped and tracked independently in each prim.

## See Also

### Functions

- **llStartObjectAnimation** — Start playing an animation in the current object
- **llGetObjectAnimationNames** — List currently playing animations in the current object

<!-- /wiki-source -->
