---
name: "run_time_permissions"
category: "event"
type: "event"
language: "LSL"
description: "Fires when an avatar grants or denies permissions requested by llRequestPermissions"
wiki_url: "https://wiki.secondlife.com/wiki/Run_time_permissions"
first_fetched: "2026-03-09"
last_updated: "2026-03-09"
signature: "run_time_permissions(integer perm)"
parameters:
  - name: "perm"
    type: "integer"
    description: "Bitmask of PERMISSION_* flags that were granted; 0 if all denied"
deprecated: "false"
---

# run_time_permissions

```lsl
run_time_permissions(integer perm)
{
    if (perm & PERMISSION_TRIGGER_ANIMATION)
    {
        llStartAnimation("wave");
    }
}
```

Fires after an avatar responds to a permissions dialog from `llRequestPermissions`. `perm` is a bitmask of granted permissions.

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `perm` | integer | Bitmask of granted PERMISSION_* flags (0 if all denied) |

## PERMISSION_* Constants

| Constant | Value | Description | Who Grants |
|----------|-------|-------------|-----------|
| `PERMISSION_DEBIT` | 0x2 | Debit owner's account (L$) | Owner only |
| `PERMISSION_TAKE_CONTROLS` | 0x4 | Override avatar movement controls | Anyone |
| `PERMISSION_TRIGGER_ANIMATION` | 0x10 | Play animations on avatar | Anyone |
| `PERMISSION_ATTACH` | 0x20 | Attach/detach from avatar | Owner or anyone |
| `PERMISSION_CHANGE_LINKS` | 0x80 | Link/unlink prims | Owner only |
| `PERMISSION_TRACK_CAMERA` | 0x400 | Read camera position/rotation | Anyone |
| `PERMISSION_CONTROL_CAMERA` | 0x800 | Override camera position | Anyone |
| `PERMISSION_TELEPORT` | 0x1000 | Teleport the avatar | Anyone |
| `PERMISSION_SILENT_ESTATE_MANAGEMENT` | 0x4000 | Manage estate access silently | Owner only |
| `PERMISSION_OVERRIDE_ANIMATIONS` | 0x8000 | Override default animations | Anyone |
| `PERMISSION_RETURN_OBJECTS` | 0x10000 | Return objects from parcels | Owner/group owner |
| `PERMISSION_PRIVILEGED_LAND_ACCESS` | 0x80000 | Privileged parcel access | Owner only |

Auto-granted (no dialog shown) when avatar is seated or object is attached.

## Caveats

- `perm` of 0 means the user denied all permissions.
- Test with bitwise `&`, not `==`.
- `PERMISSION_TELEPORT` cannot be held by temporary attachments.
- Some permissions auto-granted on attach/sit (no `run_time_permissions` event fires in that case — check with `llGetPermissions`).

## Example

```lsl
default
{
    state_entry()
    {
        llRequestPermissions(llGetOwner(), PERMISSION_TRIGGER_ANIMATION);
    }

    run_time_permissions(integer perm)
    {
        if (perm & PERMISSION_TRIGGER_ANIMATION)
        {
            llStartAnimation("wave");
        }
        else
        {
            llOwnerSay("Animation permission denied");
        }
    }
}
```

## See Also

- `llRequestPermissions` — request permissions from avatar
- `llGetPermissions` — check currently held permissions
- `llGetPermissionsKey` — UUID of avatar who granted permissions
- `PERMISSION_*` constants


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/run_time_permissions) — scraped 2026-03-18_

## Examples

Plays an animation

```lsl
default
{
    state_entry()
    {
        llRequestPermissions(llGetOwner(), PERMISSION_TRIGGER_ANIMATION);
    }
    run_time_permissions(integer perm)
    {
        if(PERMISSION_TRIGGER_ANIMATION & perm)
        {
            llStartAnimation("nyanya");
        }
    }
}
```

## Notes

The argument **perm** is the bit combination of all permissions granted when this event is triggered. To determine if an exact permission is granted you will need to perform a bitwise AND comparison between **perm** and the permission constant you are looking for. The example above demonstrates this. Perm will be 0 if the user has refused to grant any permissions.

<!-- /wiki-source -->
