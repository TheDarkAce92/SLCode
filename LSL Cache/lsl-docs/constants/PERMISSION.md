---
name: "PERMISSION constants"
category: "constant"
type: "constant"
language: "LSL"
description: "Bitmask constants for runtime permissions requested via llRequestPermissions and received in run_time_permissions"
wiki_url: "https://wiki.secondlife.com/wiki/PERMISSION_TRIGGER_ANIMATION"
first_fetched: "2026-03-09"
last_updated: "2026-03-09"
---

# PERMISSION_* Constants

Used with `llRequestPermissions`, `llGetPermissions`, and tested in `run_time_permissions`. Test with bitwise `&`.

## Constants

| Constant | Value | Description | Who Grants | Auto-Granted When |
|----------|-------|-------------|-----------|-------------------|
| `PERMISSION_DEBIT` | 0x2 | Debit L$ from owner's account | Owner only | — |
| `PERMISSION_TAKE_CONTROLS` | 0x4 | Override avatar movement controls | Anyone | Seated, attached |
| `PERMISSION_TRIGGER_ANIMATION` | 0x10 | Play/stop animations on avatar | Anyone | Seated, attached |
| `PERMISSION_ATTACH` | 0x20 | Attach/detach object to/from avatar | Owner or anyone | Already attached |
| `PERMISSION_CHANGE_LINKS` | 0x80 | Link or unlink prims | Owner only | — |
| `PERMISSION_TRACK_CAMERA` | 0x400 | Read camera position and rotation | Anyone | Seated, attached |
| `PERMISSION_CONTROL_CAMERA` | 0x800 | Override camera (auto-revoked on stand/detach) | Anyone | Seated, attached |
| `PERMISSION_TELEPORT` | 0x1000 | Teleport avatar via `llTeleportAgent` | Anyone | — |
| `PERMISSION_SILENT_ESTATE_MANAGEMENT` | 0x4000 | Manage estate access without notifications | Owner only | — |
| `PERMISSION_OVERRIDE_ANIMATIONS` | 0x8000 | Override default animations (`llSetAnimationOverride`) | Anyone | Attached |
| `PERMISSION_RETURN_OBJECTS` | 0x10000 | Return objects from parcels | Owner/group owner | — |
| `PERMISSION_PRIVILEGED_LAND_ACCESS` | 0x80000 | Privileged parcel access | Owner only | — |

## Usage

```lsl
// Request single permission
default
{
    state_entry()
    {
        llRequestPermissions(llGetOwner(), PERMISSION_TRIGGER_ANIMATION);
    }

    run_time_permissions(integer perm)
    {
        if (perm & PERMISSION_TRIGGER_ANIMATION)
            llStartAnimation("wave");
    }
}
```

```lsl
// Request multiple permissions
llRequestPermissions(llGetOwner(),
    PERMISSION_TRIGGER_ANIMATION | PERMISSION_TAKE_CONTROLS);

run_time_permissions(integer perm)
{
    if (perm & PERMISSION_TRIGGER_ANIMATION)
        llStartAnimation("wave");
    if (perm & PERMISSION_TAKE_CONTROLS)
        llTakeControls(CONTROL_FWD | CONTROL_BACK, TRUE, FALSE);
}
```

## See Also

- `llRequestPermissions` — request permissions from avatar
- `llGetPermissions` — get currently held permissions (bitmask)
- `llGetPermissionsKey` — UUID of avatar who granted permissions
- `run_time_permissions` event
