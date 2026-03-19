---
name: "llAvatarOnLinkSitTarget"
category: "function"
type: "function"
language: "LSL"
description: 'Returns a key that is the UUID of the user seated on the prim.

If the prim lacks a sit target or there is no avatar sitting on the prim, then NULL_KEY is returned.'
signature: "key llAvatarOnLinkSitTarget(integer link)"
return_type: "key"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llAvatarOnLinkSitTarget'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llavataronlinksittarget"]
---

Returns a key that is the UUID of the user seated on the prim.

If the prim lacks a sit target or there is no avatar sitting on the prim, then NULL_KEY is returned.


## Signature

```lsl
key llAvatarOnLinkSitTarget(integer link);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `integer (link)` | `link` | Link number (1: root prim, >1: child prims and seated avatars) or a LINK_* flag |


## Return Value

Returns `key`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llAvatarOnLinkSitTarget)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llAvatarOnLinkSitTarget) — scraped 2026-03-18_

Returns a key that is the UUID of the user seated on the prim.

## Caveats

- link needs to be either an actual link number or a link constants that equate to a single prim, such as LINK_ROOT and LINK_THIS.

  - LINK_SET, LINK_ALL_CHILDREN and LINK_ALL_OTHERS will not work.
- A prim does not have a sit target unless llSitTarget/llLinkSitTarget has been called with a **nonzero** vector as the first argument.
- The root link number changes from zero to one when someone sits on an unlinked prim.

  - So `(llAvatarOnLinkSitTarget( 0) == NULL_KEY)` is always true. Nobody ever sits on link number 0

## Examples

```lsl
// Unseat a second avatar on this object

string one_sitter_message = "Hey!  I don't take passengers.";

default
{
    state_entry()
    {
        // Sit target 1 is your sit target on the root prim
        llLinkSitTarget(1,<0.0,0.0,0.5>,ZERO_ROTATION);
        // Sit target 2 is the target on child prim 2, a small transparent prim inside the object
        llLinkSitTarget(2, <0.0,0.0,0.1>,ZERO_ROTATION);
    }

    changed(integer change)
    {
        if (change & CHANGED_LINK)
        {
            // An avatar on child prim 2, whether seated by choice or by redirection after sit target 1 is occupied, will be unseated.
            if (llAvatarOnLinkSitTarget(2))
            {
                llRegionSayTo(llAvatarOnLinkSitTarget(2),PUBLIC_CHANNEL, one_sitter_message);
                llUnSit(llAvatarOnLinkSitTarget(2));
            }
            // Now pay attention to the avatar on the root prim.
            key agent = llAvatarOnLinkSitTarget(1);
            if (agent)
            {
                llRegionSayTo(agent,PUBLIC_CHANNEL,"Hello!");
            }
        }
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
The position of an avatar on a sit target can be determined with the use of llGetObjectDetails (see llSitTarget for an example).

If an object has multiple seats (each seat has a script that sets a sit target with llSitTarget, or the linkset has a script that assigns several *llLinkSitTarget*s), the following method determines which sit target an avatar ends up at:

- If the prim that is clicked on *has* a sit target and that sit target is not full, that sit target is used.
- If the prim that is clicked on *has no sit target*, and one or more other linked prims have sit targets that are not full, the sit target of the prim with the lowest link number will be used.

## See Also

### Events

- changed

### Functions

- **llGetLinkNumber** — prim
- llAvatarOnSitTarget
- llLinkSitTarget
- llGetLinkKey

### Articles

- CHANGED_LINK

<!-- /wiki-source -->
