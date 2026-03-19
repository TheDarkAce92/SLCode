---
name: "llSetAnimationOverride"
category: "function"
type: "function"
language: "LSL"
description: 'Set the animation (anim) that will play for the given animation state (anim_state).

To run this function the script must request the PERMISSION_OVERRIDE_ANIMATIONS permission with llRequestPermissions.
Note: Animation overrides survive everything, except relog.'
signature: "void llSetAnimationOverride(string anim_state, string anim)"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llSetAnimationOverride'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llsetanimationoverride"]
---

Set the animation (anim) that will play for the given animation state (anim_state).

To run this function the script must request the PERMISSION_OVERRIDE_ANIMATIONS permission with llRequestPermissions.
Note: Animation overrides survive everything, except relog.


## Signature

```lsl
void llSetAnimationOverride(string anim_state, string anim);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `string` | `anim_state` | animation state to be overriden |
| `string` | `anim` | an animation in the inventory of the prim this script is in or the name of a built-in animation |


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llSetAnimationOverride)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llSetAnimationOverride) — scraped 2026-03-18_

Set the animation (anim) that will play for the given animation state (anim_state).

## Caveats

| Permissions |
| --- |
| - Do not depend upon the auto-grant status of permissions. **Always** use the run_time_permissions event. - If the script lacks the permission PERMISSION_OVERRIDE_ANIMATIONS, the script will shout an error on DEBUG_CHANNEL and the operation fails (but the script continues to run). - Once the PERMISSION_OVERRIDE_ANIMATIONS permission is granted there may be no way to revoke it except from inside the script (for example, with a new llRequestPermissions call) or if the script is reset. Furthermore even if the script loses the permission (or is derezzed), it will not reset/revert the overridable animations. - *For Viewer 3.6.7 and up:* If the object is *not* attached to the permission granter but *is* in the same region, then **Me>Movement>Stop Animating Me** will revoke both PERMISSION_TRIGGER_ANIMATION and PERMISSION_OVERRIDE_ANIMATIONS (other permissions will remain). In this case, overrides *are* reset. |

- If anim is missing from the prim's inventory   or it is not an animation then an error is shouted on DEBUG_CHANNEL.
- Animation overrides survive script reset, script removal, attachment removal, crossing into another region and teleporting, but not relog.
- State "Sit on Ground" will play the default animation in addition to any override set. This is required for correct viewer behavior.
- Some states are transitional and have undefined behavior if set to continuously looping animations. These states are "PreJumping", "Landing", "Soft Landing" and "Standing Up".

  - Usually this means your avatar will become frozen in place unless you run "Stop Animating My Avatar" from the viewer, so avoid using looping animations for these states.
- Permissions aren't auto granted if you sit on an object asking for PERMISSION_OVERRIDE_ANIMATIONS.
- Starting a default animation ("sit" "walk" "fly") with llStartAnimation will not start the Override Animation.
- When this function is used to override the Walking animation, the avatar can no longer walk backward - attempting to do so causes the avatar to turn around. Presumably this is because there's no way to specify a "walking backwards" animation, so actually moving backwards while your legs are moving forward would look wrong.

## Examples

```lsl
// Override the Sit, Stand and Walk animations
// 1. place this script and your animations in a prim
// 2. edit the animation names in the script to your animation's names
// 3. attach the prim to your avatar

string gMySit = "chop_sit";
string gMyStand = "FStand _02";
string gMyWalk = "Kort gang F v4.1";

default
{
    attach(key id)
    {
        if ( id ) llRequestPermissions(id , PERMISSION_OVERRIDE_ANIMATIONS);
        else if ( llGetPermissions() & PERMISSION_OVERRIDE_ANIMATIONS ) llResetAnimationOverride("ALL");
    }
    run_time_permissions(integer perms)
    {
        if ( perms & PERMISSION_OVERRIDE_ANIMATIONS )
        {
            llSetAnimationOverride( "Sitting", gMySit);
            llSetAnimationOverride( "Standing", gMyStand);
            llSetAnimationOverride( "Walking", gMyWalk);
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
- llGetAnimationOverride
- llResetAnimationOverride

### Articles

- Script permissions
- **Internal_Animations** — lists internal Animations always available

<!-- /wiki-source -->
