---
name: "llStopAnimation"
category: "function"
type: "function"
language: "LSL"
description: 'Stop animation anim for agent that granted PERMISSION_TRIGGER_ANIMATION if the permission has not been revoked.

To run this function the script must request the PERMISSION_TRIGGER_ANIMATION permission with llRequestPermissions.'
signature: "void llStopAnimation(string anim)"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llStopAnimation'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llstopanimation"]
---

Stop animation anim for agent that granted PERMISSION_TRIGGER_ANIMATION if the permission has not been revoked.

To run this function the script must request the PERMISSION_TRIGGER_ANIMATION permission with llRequestPermissions.


## Signature

```lsl
void llStopAnimation(string anim);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `string` | `anim` | an animation in the inventory of the prim this script is in or a UUID of an animation or built in animation name |


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llStopAnimation)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llStopAnimation) — scraped 2026-03-18_

Stop animation anim for agent that granted PERMISSION_TRIGGER_ANIMATION if the permission has not been revoked.

## Caveats

| Permissions |
| --- |
| - Do not depend upon the auto-grant status of permissions. **Always** use the run_time_permissions event. - If the script lacks the permission PERMISSION_TRIGGER_ANIMATION, the script will shout an error on DEBUG_CHANNEL and the operation fails (but the script continues to run). - Once the PERMISSION_TRIGGER_ANIMATION permission is granted there may be no way to revoke it except from inside the script (for example, with a new llRequestPermissions call) or if the script is reset. - *For Viewer 3.6.7 and up:* If the object is *not* attached to the permission granter but *is* in the same region, then **Me>Movement>Stop Animating Me** will revoke both PERMISSION_TRIGGER_ANIMATION and PERMISSION_OVERRIDE_ANIMATIONS (other permissions will remain). |

- If anim is missing from the prim's inventory  and it is not a UUID or it is not an animation then an error is shouted on DEBUG_CHANNEL.
- If anim is a UUID then there are no new asset permissions consequences for the object.

  - The resulting object develops no new usage restrictions that might have occurred if the asset had been placed in the prims inventory.
- If the animation to be stopped is the only playing animation (as found via llGetAnimationList), it will continue to play to its end (if looped it will continue indefinitely)

  - if you must stop a looped animation, playing a single frame non-looped one immediately after stopping it, at low priority, will clear the list.

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

## Notes

```lsl
llStopAnimation(llGetAnimationOverride("Sitting"))
```

## See Also

### Events

- **run_time_permissions** — Permission receiving event

### Functions

- **llGetPermissions** — Get the permissions granted
- **llGetPermissionsKey** — Get the agent who granted permissions
- **llRequestPermissions** — Request permissions
- **llGetAnimationList** — Gets a list of playing animations
- **llStartAnimation** — Starts playing an animation

### Articles

- Script permissions

<!-- /wiki-source -->
