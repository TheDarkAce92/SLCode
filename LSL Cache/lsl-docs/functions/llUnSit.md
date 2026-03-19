---
name: "llUnSit"
category: "function"
type: "function"
language: "LSL"
description: 'The agent identified by id is forced to stand up if any of the following apply:
# The agent is sitting on the scripted object
# The agent is over land owned by the scripted object's owner and/or a group the owner has land rights for.'
signature: "void llUnSit(key id)"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llUnSit'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llunsit"]
---

The agent identified by id is forced to stand up if any of the following apply:
# The agent is sitting on the scripted object
# The agent is over land owned by the scripted object's owner and/or a group the owner has land rights for.


## Signature

```lsl
void llUnSit(key id);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `key` | `id` | avatar UUID that is in the same region |


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llUnSit)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llUnSit) — scraped 2026-03-18_

The agent identified by id is forced to stand up if any of the following apply:

## Examples

```lsl
// UnSit on Sit, Using a sit target
default
{
    state_entry()
    {
        llSitTarget(<0.0, 0.0, 0.1>, ZERO_ROTATION); // Needed for llAvatarOnSitTarget to work. The vectors components must not all be set to 0.0
    }
    changed(integer change) // Triggered when various changes are sensed.
    {
        if(change & CHANGED_LINK) // When an agent sits on an object they become a new link.
        {
            key user = llAvatarOnSitTarget(); // Store the UUID of any agent sitting on the sit target.
            if(user) // An avatar is on the sit target.
                llUnSit(user); // Un-Sit the avatar.
        }
    }
}
```

```lsl
// UnSit on Sit, NOT using a sit target

default
{
    changed(integer change) // Triggered when various changes are sensed.
    {
        if(change & CHANGED_LINK) // When an agent sits on an object they become a new link.
        {
            integer links = 0; // Create an integer type variable.
            if(llGetObjectPrimCount(llGetKey()) < (links = llGetNumberOfPrims())) // During the check store the number of links.
            // If the number of prims is fewer than the number of links, the last must be an avatar.
                llUnSit(llGetLinkKey(links)); // Use the key of the last link to be added (the avatar) to call llUnSit().
            else
                llOwnerSay("Some kind of linking or unlinking has changed me but, I am not being sat on.");
            // llUnSit() triggers the changed event too (the number of links is reduced by 1).
        }
    }
}
```

```lsl
unsit_all_avatars()
{
    integer objectPrimCount = llGetObjectPrimCount(llGetKey());
    integer currentLinkNumber = llGetNumberOfPrims();

    for (; objectPrimCount < currentLinkNumber; --currentLinkNumber)
        llUnSit(llGetLinkKey(currentLinkNumber));
}

default
{
    touch_start(integer num_detected)
    {
        unsit_all_avatars();
    }
}
```

## See Also

### Events

- changed

### Functions

- llAvatarOnSitTarget
- llSitTarget

<!-- /wiki-source -->
