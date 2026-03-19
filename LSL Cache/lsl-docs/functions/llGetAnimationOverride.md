---
name: "llGetAnimationOverride"
category: "function"
type: "function"
language: "LSL"
description: "Returns a string that is the name of the animation that is being used for the specified animation state (anim_state)."
signature: "string llGetAnimationOverride(string anim_state)"
return_type: "string"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetAnimationOverride'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgetanimationoverride"]
---

Returns a string that is the name of the animation that is being used for the specified animation state (anim_state).


## Signature

```lsl
string llGetAnimationOverride(string anim_state);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `string` | `anim_state` | animation state |


## Return Value

Returns `string`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetAnimationOverride)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetAnimationOverride) — scraped 2026-03-18_

Returns a string that is the name of the animation that is being used for the specified animation state (anim_state).

## Caveats

| Permissions |
| --- |
| - Do not depend upon the auto-grant status of permissions. **Always** use the run_time_permissions event. - If the script lacks both the permissions PERMISSION_OVERRIDE_ANIMATIONS and PERMISSION_TRIGGER_ANIMATION, the script will shout an error on DEBUG_CHANNEL and the operation fails (but the script continues to run). - Once the PERMISSION_OVERRIDE_ANIMATIONS permission is granted there may be no way to revoke it except from inside the script (for example, with a new llRequestPermissions call) or if the script is reset. Furthermore even if the script loses the permission (or is derezzed), it will not reset/revert the overridable animations. - *For Viewer 3.6.7 and up:* If the object is *not* attached to the permission granter but *is* in the same region, then **Me>Movement>Stop Animating Me** will revoke both PERMISSION_TRIGGER_ANIMATION and PERMISSION_OVERRIDE_ANIMATIONS (other permissions will remain). In this case, overrides *are* reset. - Once the PERMISSION_TRIGGER_ANIMATION permission is granted there may be no way to revoke it except from inside the script (for example, with a new llRequestPermissions call) or if the script is reset. - *For Viewer 3.6.7 and up:* If the object is *not* attached to the permission granter but *is* in the same region, then **Me>Movement>Stop Animating Me** will revoke both PERMISSION_TRIGGER_ANIMATION and PERMISSION_OVERRIDE_ANIMATIONS (other permissions will remain). |

## Examples

```lsl
//    llGetAnimationOverride Example
//    A Script to check the animation Stats on
//  all available overridable animations.
//    By Kanashio Koroshi and Pedro Oval

default
{
    state_entry()
    {
        llRequestPermissions(llGetOwner(),
            PERMISSION_OVERRIDE_ANIMATIONS);
    }

    run_time_permissions(integer permissions)
    {
        if (permissions & PERMISSION_OVERRIDE_ANIMATIONS)
        {
            llOwnerSay("Listing Overridden Animations");
            llOwnerSay("Crouching: " + llGetAnimationOverride("Crouching"));
            llOwnerSay("CrouchWalking: " + llGetAnimationOverride("CrouchWalking"));
            llOwnerSay("Falling Down: " + llGetAnimationOverride("Falling Down"));
            llOwnerSay("Flying: " + llGetAnimationOverride("Flying"));
            llOwnerSay("FlyingSlow: " + llGetAnimationOverride("FlyingSlow"));
            llOwnerSay("Hovering: " + llGetAnimationOverride("Hovering"));
            llOwnerSay("Hovering Down: " + llGetAnimationOverride("Hovering Down"));
            llOwnerSay("Hovering Up: " + llGetAnimationOverride("Hovering Up"));
            llOwnerSay("Jumping: " + llGetAnimationOverride("Jumping"));
            llOwnerSay("Landing: " + llGetAnimationOverride("Landing"));
            llOwnerSay("PreJumping: " + llGetAnimationOverride("PreJumping"));
            llOwnerSay("Running: " + llGetAnimationOverride("Running"));
            llOwnerSay("Sitting: " + llGetAnimationOverride("Sitting"));
            llOwnerSay("Sitting on Ground: " + llGetAnimationOverride("Sitting on Ground"));
            llOwnerSay("Standing: " + llGetAnimationOverride("Standing"));
            llOwnerSay("Standing Up: " + llGetAnimationOverride("Standing Up"));
            llOwnerSay("Striding: " + llGetAnimationOverride("Striding"));
            llOwnerSay("Soft Landing: " + llGetAnimationOverride("Soft Landing"));
            llOwnerSay("Taking Off: " + llGetAnimationOverride("Taking Off"));
            llOwnerSay("Turning Left: " + llGetAnimationOverride("Turning Left"));
            llOwnerSay("Turning Right: " + llGetAnimationOverride("Turning Right"));
            llOwnerSay("Walking: " + llGetAnimationOverride("Walking"));
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
- llSetAnimationOverride
- llResetAnimationOverride

### Articles

- Script permissions
- **Internal_Animations** — lists internal Animations always available

<!-- /wiki-source -->
