---
name: "llStartAnimation"
category: "function"
type: "function"
language: "LSL"
description: 'Start animation anim for agent that granted PERMISSION_TRIGGER_ANIMATION if the permission has not been revoked.

To run this function the script must request the PERMISSION_TRIGGER_ANIMATION permission with llRequestPermissions.'
signature: "void llStartAnimation(string anim)"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llStartAnimation'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llstartanimation"]
---

Start animation anim for agent that granted PERMISSION_TRIGGER_ANIMATION if the permission has not been revoked.

To run this function the script must request the PERMISSION_TRIGGER_ANIMATION permission with llRequestPermissions.


## Signature

```lsl
void llStartAnimation(string anim);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `string` | `anim` | an item in the inventory of the prim this script is in or built-in animation |


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llStartAnimation)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llStartAnimation) — scraped 2026-03-18_

Start animation anim for agent that granted PERMISSION_TRIGGER_ANIMATION if the permission has not been revoked.

## Caveats

| Permissions |
| --- |
| - Do not depend upon the auto-grant status of permissions. **Always** use the run_time_permissions event. - If the script lacks the permission PERMISSION_TRIGGER_ANIMATION, the script will shout an error on DEBUG_CHANNEL and the operation fails (but the script continues to run). - Once the PERMISSION_TRIGGER_ANIMATION permission is granted there may be no way to revoke it except from inside the script (for example, with a new llRequestPermissions call) or if the script is reset. - *For Viewer 3.6.7 and up:* If the object is *not* attached to the permission granter but *is* in the same region, then **Me>Movement>Stop Animating Me** will revoke both PERMISSION_TRIGGER_ANIMATION and PERMISSION_OVERRIDE_ANIMATIONS (other permissions will remain). |

- If anim is missing from the prim's inventory    then an error is shouted on DEBUG_CHANNEL.
- Only 30 animations can be played at a time.  (Prior to 1.25.4 the limit was 15 and prior to 1.25.3 there was no limit at all.)

## Examples

```lsl
default
{
    touch_start(integer detected)
    {
        llRequestPermissions(llDetectedKey(0), PERMISSION_TRIGGER_ANIMATION);
    }
    run_time_permissions(integer perm)
    {
        if (perm & PERMISSION_TRIGGER_ANIMATION)
        {
            llStartAnimation("sit");
            llOwnerSay("animation will end in 5 seconds");
            llSetTimerEvent(5.0);
        }
    }
    timer()
    {
        llSetTimerEvent(0.0);
        llStopAnimation("sit");
    }
}
```

Add an animation or pose inside the same object as this script:

```lsl
string animation; // the first animation in inventory will automatically be used
  // the animation name must be stored globally to be able to stop the animation when standing up

default
{
    state_entry()
    {
        // set sit target, otherwise this will not work
        llSitTarget(<0.0, 0.0, 0.1>, ZERO_ROTATION);
    }

    changed(integer change)
    {
        if (change & CHANGED_LINK)
        {
            key av = llAvatarOnSitTarget();
            if (av) //evaluated as true if not NULL_KEY or invalid
                llRequestPermissions(av, PERMISSION_TRIGGER_ANIMATION);
            else // avatar is standing up
            {
                if (animation)
                    llStopAnimation(animation); // stop the started animation
                llResetScript(); // release the avatar animation permissions
            }
        }
    }

    run_time_permissions(integer perm)
    {
        if (perm & PERMISSION_TRIGGER_ANIMATION)
        {
            animation = llGetInventoryName(INVENTORY_ANIMATION,0); // get the first animation from inventory
            if (animation)
            {
                llStopAnimation("sit"); // stop the default sit animation
                llStartAnimation(animation);
            }
        }
    }
}
```

Common script to play some kind of a "holding animation" while an object is attached to an avatar:

```lsl
string animation_name = "hold";

default
{
    // Whenever this object is attached or detached...
    attach(key id)
    {
        if (id)
        {   // If it was just attached, request permission to animate.
            llRequestPermissions(llGetOwner(), PERMISSION_TRIGGER_ANIMATION);
        }
        else
        {   // It's being detached...
            if (llGetPermissions() & PERMISSION_TRIGGER_ANIMATION)
            {   // If we have permission to animate, stop the animation.
                llStopAnimation(animation_name);
            }
        }
    }

    // Whenever permissions change...
    run_time_permissions(integer permissions)
    {
        if (permissions & PERMISSION_TRIGGER_ANIMATION)
        {   // If permission to animate was granted, start the animation.
            llStartAnimation(animation_name);
        }
    }
}
```

## See Also

### Events

- **run_time_permissions** — Permission receiving event

### Functions

- **llGetPermissions** — Get the permissions granted
- **llGetPermissionsKey** — Get the agent who granted permissions
- **llRequestPermissions** — Request permissions
- llStopAnimation

### Articles

- Script permissions
- **Internal_Animations** — lists internal Animations always available

<!-- /wiki-source -->
