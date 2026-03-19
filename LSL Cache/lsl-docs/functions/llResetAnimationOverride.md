---
name: "llResetAnimationOverride"
category: "function"
type: "function"
language: "LSL"
description: 'Resets the animation override of the specified animation state (anim_state) to the corresponding default value.

To run this function the script must request the PERMISSION_OVERRIDE_ANIMATIONS permission with llRequestPermissions.
If anim_state equals 'ALL', all animation states are reset.'
signature: "void llResetAnimationOverride(string anim_state)"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llResetAnimationOverride'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llresetanimationoverride"]
---

Resets the animation override of the specified animation state (anim_state) to the corresponding default value.

To run this function the script must request the PERMISSION_OVERRIDE_ANIMATIONS permission with llRequestPermissions.
If anim_state equals "ALL", all animation states are reset.


## Signature

```lsl
void llResetAnimationOverride(string anim_state);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `string` | `anim_state` | animation state to be reset |


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llResetAnimationOverride)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llResetAnimationOverride) — scraped 2026-03-18_

Resets the animation override of the specified animation state (anim_state) to the corresponding default value.

## Caveats

| Permissions |
| --- |
| - Do not depend upon the auto-grant status of permissions. **Always** use the run_time_permissions event. - If the script lacks the permission PERMISSION_OVERRIDE_ANIMATIONS, the script will shout an error on DEBUG_CHANNEL and the operation fails (but the script continues to run). - Once the PERMISSION_OVERRIDE_ANIMATIONS permission is granted there may be no way to revoke it except from inside the script (for example, with a new llRequestPermissions call) or if the script is reset. Furthermore even if the script loses the permission (or is derezzed), it will not reset/revert the overridable animations. - *For Viewer 3.6.7 and up:* If the object is *not* attached to the permission granter but *is* in the same region, then **Me>Movement>Stop Animating Me** will revoke both PERMISSION_TRIGGER_ANIMATION and PERMISSION_OVERRIDE_ANIMATIONS (other permissions will remain). In this case, overrides *are* reset. |

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
