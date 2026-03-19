---
name: "llRequestPermissions"
category: "function"
type: "function"
language: "LSL"
description: 'Ask agent for permissions to run certain classes of functions.

Script execution continues without waiting for a response. When a response is given, a run_time_permissions event is put in the event queue.'
signature: "void llRequestPermissions(key agent, integer perm)"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llRequestPermissions'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llrequestpermissions"]
---

Ask agent for permissions to run certain classes of functions.

Script execution continues without waiting for a response. When a response is given, a run_time_permissions event is put in the event queue.


## Signature

```lsl
void llRequestPermissions(key agent, integer perm);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `key` | `agent` | avatar UUID that is in the same region |
| `integer (permission)` | `permissions` | Permission mask (bitfield containing the permissions to request). |


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llRequestPermissions)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llRequestPermissions) — scraped 2026-03-18_

Ask agent for permissions to run certain classes of functions.

## Caveats

- A dialog is presented to the agent to grant these permissions except when granted automatically as shown in the table above.
- If object is attached to agent, "automatic" permissions are granted without notification upon request.
- Permissions persist across state changes.
- Regardless of whether granting is automatic, you should always use the run_time_permissions event.  Granting permissions takes time, and you shouldn't assume it's completed until the run_time_permissions handler gets invoked.
- The menu-option "Stop Animating Me" will release certain permissions (PERMISSION_TRIGGER_ANIMATION and PERMISSION_OVERRIDE_ANIMATIONS), if the script which holds these permissions is in the same region as the agent, and the script is not attached to the permission granter.
- Permissions do not accumulate.

  - If a permission was requested with a previous call to this function and granted, then in subsequent call was not requested, that permission is released (lost).
  - To request two or more permissions at the same time, use the bitwise OR (|) operator, e.g.:

```lsl
llRequestPermissions(AvatarID, PERMISSION_TAKE_CONTROLS | PERMISSION_TRIGGER_ANIMATION)
```

- Permissions are requested and granted separately for each script, even if they are located in the same object.
- It is currently not possible to request no permissions at all (see Issues below); as a workaround llResetScript can be used.
- Scripts may hold permissions for only one agent at a time. To hold permissions for multiple agents you must use more than one script.
- The result of granting permissions affects the return of llGetPermissions and llGetPermissionsKey immediately, despite the run_time_permissions event being queued, or dropped if the object's event queue is full.
- Permission request dialogs never time out.
- If a script makes two permission requests, whichever response is last is considered the granted permissions.
- The viewer limits permission requests from any agent to any other agent to 5 dialogs in 10 seconds.
- Permission requests and changing state ...

  - Requesting a permission in one state, then changing state before the agent response, will cause run_time_permissions to be fired in the new state once the agent responds.
  - Requesting only auto-granted permissions in one state, then immediately changing state, will never fire run_time_permissions.

## Examples

Request permission to animate an avatar

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

To request two (or more) permissions at the same time, use the bitwise OR (|) operator.

```lsl
llRequestPermissions(AvatarID, PERMISSION_TAKE_CONTROLS | PERMISSION_TRIGGER_ANIMATION);
```

- or -

```lsl
integer perms = PERMISSION_TAKE_CONTROLS | PERMISSION_TRIGGER_ANIMATION;
llRequestPermissions(AvatarID, perms);
```

## Notes

When an agent grants a script non-automatic permissions they will receive a notification (in chat) of

- The **name** of the object that contains the script that has been granted perms,
- The name of the owner of the object,
- The location of the object in the order Region name at **position**, and
- A statement of what permissions were granted.

If the script that holds the permissions is in a child prim the **name** will be that of the child prim (not the object (root)) and **position** will be its local position (relative to its root).

## See Also

### Events

- **run_time_permissions** — Permission receiver event

### Functions

- **llGetPermissions** — Get the permissions granted
- **llGetPermissionsKey** — Get the avatar who granted permissions.

### Articles

- Script permissions

<!-- /wiki-source -->
