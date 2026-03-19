---
name: "llSitTarget"
category: "function"
type: "function"
language: "LSL"
description: 'Set the sit location for the prim. The sit location is relative to the prim's position and rotation.

If offset == <0.0, 0.0, 0.0> then the sit target is removed.'
signature: "void llSitTarget(vector offset, rotation rot)"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llSitTarget'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llsittarget"]
---

Set the sit location for the prim. The sit location is relative to the prim's position and rotation.

If offset == <0.0, 0.0, 0.0> then the sit target is removed.


## Signature

```lsl
void llSitTarget(vector offset, rotation rot);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `vector` | `offset` | Additional position for the sit target in local prim coordinates. |
| `rotation` | `rot` | Additional rotation for the sit target relative to the prim rotation. |


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llSitTarget)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llSitTarget) — scraped 2026-03-18_

Set the sit location for the prim. The sit location is relative to the prim's position and rotation.

## Caveats

- Once a sit target is removed llAvatarOnSitTarget will only return NULL_KEY.
- Removing or deactivating the script that sets the sit target will not remove the prim's sit target.

  - Sit target is a prim property and not dependent on a script for its continued existence.
- To remove sit target, use the following:

```lsl
llSitTarget(ZERO_VECTOR, ZERO_ROTATION);
```

- Shift-copying a prim with a sit target, without a script that will set the sit target again, will not keep the sit target on the copy. (The copy is in the original location when shift-copying.)
- There is no way to remove the Sit option from the menu.

  - It will appear to be removed if the llSetSitText is set to a space " " or similar transparent string.
- Attachments cannot be sat upon (see [SVC-6100](https://jira.secondlife.com/browse/SVC-6100) to vote for such a feature).
- rot affects the position of the sit target in a buggy way.

  - To correct for the *rot* bug, simply subtract <0,0,0.4> from the position when *rot* is zero. See example below.
  - llSetLinkPrimitiveParams is a more difficult work-around.
  - Animations are relative to the Agent Target, but the Agent Target isn't described by the animation.
- llSitTarget does not update position of an already seated avatar.

  - UpdateSitTarget described below works around this problem. It works by converting the sit target information into a link position that is passed along to llSetLinkPrimitiveParams.
- offset is limited to 300.0 meters on each axis. The *x*, *y* and *z* components must be in the range [-300, 300.0].

  - If they are outside the acceptable range they are rounded to the closest limit.
- If an object has multiple seats (each seat has a script that sets a sit target, or the linkset has a script that assigns several llLinkSitTargets), the following method determines which sit target an avatar ends up at:

  - If the prim that is clicked on *has* a sit target and that sit target is not full, that sit target is used.
  - If the prim that is clicked on *has no sit target*, and one or more other linked prims have sit targets that are not full, the sit target of the prim with the lowest link number will be used.

## Examples

```lsl
default
{
    state_entry()
    {
        llSitTarget(<0.0, 0.0, 1.0>, ZERO_ROTATION); //The vector's components must not all be set to 0 for effect to take place.
    }
}
```

```lsl
default     //example with work-around for llSetTarget rot bug
{           //place in any prim large enough to sit on at any angle
            //click once to choose a place to sit, a second time to sit there
    touch_start(integer num)
    {
        vector pos   = llDetectedTouchPos(0);        //use touch to set sit target
        vector lft   = llDetectedTouchBinormal(0);   //use normals to rotate avatar to
        vector up    = llDetectedTouchNormal(0);     //sit upright
        rotation rot = llAxes2Rot(lft % up, lft, up) / llGetRot();  //rotate avatar to stand there
        vector siz   = llGetAgentSize(llDetectedKey(0));
        pos += 0.65 * siz.z * up;       //this places MY avatars feet close to the surface
        pos = (pos - llGetPos()) / llGetRot();  //llSetTarget expects local co-ordinates
        if (rot != ZERO_ROTATION) pos -=<0.0, 0.0, 0.4>;  //here is the workaround
        llSitTarget(pos, rot);
        llSetClickAction(CLICK_ACTION_SIT);   //switch to sit for second click
    }
    changed(integer change)
    {
        if (llAvatarOnSitTarget() == NULL_KEY)      //if they unsit,
            llSetClickAction(CLICK_ACTION_TOUCH);   //go back to click mode
    }
}
```

## See Also

### Events

- changed

### Functions

- llLinkSitTarget
- llSetSitText
- llAvatarOnSitTarget
- llAvatarOnLinkSitTarget
- llUnSit

<!-- /wiki-source -->
