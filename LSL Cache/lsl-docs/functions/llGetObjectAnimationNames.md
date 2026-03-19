---
name: "llGetObjectAnimationNames"
category: "function"
type: "function"
language: "LSL"
description: "Returns a list of names of animations playing in the current object"
signature: "list llGetObjectAnimationNames()"
return_type: "list"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetObjectAnimationNames'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
---

Returns a list of names of animations playing in the current object


## Signature

```lsl
list llGetObjectAnimationNames();
```


## Return Value

Returns `list`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetObjectAnimationNames)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetObjectAnimationNames) — scraped 2026-03-18_

Returns a list of names of animations playing in the current object

## Examples

```lsl
stop_all_animations()
{
    list curr_anims = llGetObjectAnimationNames();
    llSay(0,"stopping all, curr_anims are " + (string) curr_anims);
    integer length = llGetListLength(curr_anims);
    integer index = 0;
    while (index < length)
    {
        string anim = llList2String(curr_anims, index);
        llSay(0, "Stopping " + anim);
        llStopObjectAnimation(anim);
        // This check isn't really needed, just included to demonstrate is_animation_running()
        if (is_animation_running(anim))
        {
            llSay(0, "ERROR - failed to stop " + anim + "!");
        }
        ++index;
    }
}

integer is_animation_running(string anim)
{
    list curr_anims = llGetObjectAnimationNames();
    return ~llListFindList(curr_anims, (list)anim);
}

default
{
    state_entry()
    {
        llSay(0, "Hello, Avatar!");
    }

    touch_start(integer total_number)
    {
        // Assumes there is an animation with this name in the current object.
        string anim_name = "MyFancyWalk";
        llSay(0, "Touched.");
        llStartObjectAnimation(anim_name);
        if (is_animation_running(anim_name))
        {
            llSay(0,anim_name + " is playing, which is good");
        }
        llSleep(5.0);
        stop_all_animations();
        if (is_animation_running(anim_name))
        {
            llSay(0,anim_name + " is playing, which is an error!");
        }
    }
}
```

## Notes

The typical uses for this function are to stop all currently playing animations, or to check whether a particular animation is currently playing.

This function allows you to see all currently playing animations in this object. Normally the returned values will be the names of animations within the object's inventory. In the unusual case that the animation can't be found, the key for the animation will be returned instead (as a string). In either case, the result can be sent to llStopObjectAnimation

Animated objects work by associating a skeleton with a linkset containing one or more rigged mesh primitives. When animations are played by a script in any of the prims in the linkset, the skeleton will animate and any rigged meshes in the linkset will move accordingly. A script running in any prim of the linkset can start, stop or query animations using the new commands. The typical usage of these functions is to do all object animation scripting in the root prim of the linkset; in this scenario, the animations and scripts would all be part of the inventory of this prim, and so of the object as a whole. However, if scripts and animations are present in multiple prims of a linkset, it is important to understand that animations are started, stopped and tracked independently in each prim.

## See Also

### Functions

- **llStartObjectAnimation** — Start playing an animation in the current object
- **llStopObjectAnimation** — Stop playing an animation in the current object

<!-- /wiki-source -->
