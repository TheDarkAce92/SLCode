---
name: "llLinkSitTarget"
category: "function"
type: "function"
language: "LSL"
description: 'Set the sit location for the linked prim(s). The sit location is relative to the prim's position and rotation.

If offset == <0.0, 0.0, 0.0> then the sit target is removed.'
signature: "void llLinkSitTarget(integer link, vector offset, rotation rot)"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llLinkSitTarget'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["lllinksittarget"]
---

Set the sit location for the linked prim(s). The sit location is relative to the prim's position and rotation.

If offset == <0.0, 0.0, 0.0> then the sit target is removed.


## Signature

```lsl
void llLinkSitTarget(integer link, vector offset, rotation rot);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `integer (link)` | `link` | Link number (0: unlinked, 1: root prim, >1: child prims and seated avatars) or a LINK_* flag |
| `vector` | `offset` | Additional position for the sit target in local prim coordinates. |
| `rotation` | `rot` | Additional rotation for the sit target relative to the prim rotation. |


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llLinkSitTarget)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llLinkSitTarget) — scraped 2026-03-18_

Set the sit location for the linked prim(s). The sit location is relative to the prim's position and rotation.

## Caveats

- link needs to be either an actual link number or a link constants that equate to a single prim, such as LINK_ROOT and LINK_THIS.

  - LINK_SET, LINK_ALL_CHILDREN and LINK_ALL_OTHERS will not work.
- link needs to be LINK_THIS for an unlinked prim. Specifying LINK_ROOT (integer value 1) will not work.
- Once a sit target is removed llAvatarOnLinkSitTarget will only return NULL_KEY.
- Removing or deactivating the script that sets the sit target will not remove the prim's sit target.

  - Sit target is a prim property and not dependent on a script for its continued existence.
- To remove sit target, use the following:

```lsl
llLinkSitTarget(linkNum, ZERO_VECTOR, ZERO_ROTATION);
```

- There is no way to remove the Sit option from the pie menu. It will appear to be removed if the llSetSitText is set to a space " " or similar transparent string.
- Attachments cannot be sat upon (see [SVC-6100](https://jira.secondlife.com/browse/SVC-6100) to vote for such a feature).
- rot affects the position of the sit-target in a buggy way. To correct for the *rot* bug, subtract <0.0, 0.0, 0.4> from the position when *rot* is zero. See example in llSitTarget. This offset is <0.0, 0.0, 0.418> on OpenSimulator 0.7.6 (it's 0.4 on version 0.8), but there is more to it than just this offset (opensim and SL remain incompatible). You can find the gory details and an example here.

  - llSetLinkPrimitiveParams is a more difficult workaround.
  - Animations are relative to the Agent Target, but the Agent Target isn't described by the animation.
- llSitTarget does not update position of an already seated avatar. See UpdateSitTarget for a way to do this.
- offset is limited to 300.0 meters on each axis. The x, y and z components must be in the range [-300, 300.0].

  - If they are outside the acceptable range they are rounded to the closest limit.
- If an object has multiple seats (each seat has a script that sets a sit target with llSitTarget, or the link set has a script that assigns several *llLinkSitTarget*s), the following method determines which sit target an avatar ends up at:

  - If the prim that is clicked on *has* a sit target and that sit target is not full, that sit target is used.
  - If the prim that is clicked on *has no sit target*, and one or more other linked prims have sit targets that are not full, the sit target of the prim with the lowest link number will be used.

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

### Events

- changed

### Functions

- **llGetLinkNumber** — prim
- llSitTarget
- llSetSitText
- llAvatarOnSitTarget
- llAvatarOnLinkSitTarget
- llUnSit

<!-- /wiki-source -->
