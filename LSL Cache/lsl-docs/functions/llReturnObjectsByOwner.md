---
name: "llReturnObjectsByOwner"
category: "function"
type: "function"
language: "LSL"
description: 'If the script is owned by an agent, PERMISSION_RETURN_OBJECTS may be granted by the owner.  If the script is owned by a group, this permission may be granted by an agent belonging to the group's 'Owners' role.

Returns an integer that is the number of objects successfully returned to their owners or'
signature: "integer llReturnObjectsByOwner(key owner, integer scope)"
return_type: "integer"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llReturnObjectsByOwner'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llreturnobjectsbyowner"]
---

If the script is owned by an agent, PERMISSION_RETURN_OBJECTS may be granted by the owner.  If the script is owned by a group, this permission may be granted by an agent belonging to the group's "Owners" role.

Returns an integer that is the number of objects successfully returned to their owners or an ERR_* flag.

If the return value is negative, it represents an error flag.


## Signature

```lsl
integer llReturnObjectsByOwner(key owner, integer scope);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `key` | `owner` | avatar or group UUID |
| `integer` | `scope` | OBJECT_RETURN_* flag |


## Return Value

Returns `integer`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llReturnObjectsByOwner)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llReturnObjectsByOwner) — scraped 2026-03-18_

If the script is owned by an agent, PERMISSION_RETURN_OBJECTS may be granted by the owner. If the script is owned by a group, this permission may be granted by an agent belonging to the group's "Owners" role.Returns an integer that is the number of objects successfully returned to their owners or an ERR_* flag.

## Caveats

| Permissions |
| --- |
| - Do not depend upon the auto-grant status of permissions. **Always** use the run_time_permissions event. - If the script lacks the permission PERMISSION_RETURN_OBJECTS, the script will shout an error on DEBUG_CHANNEL and the operation fails (but the script continues to run). - Once the PERMISSION_RETURN_OBJECTS permission is granted there is no way to revoke it except from inside the script (for example, with a new llRequestPermissions call) or the script is reset or deleted. - While anyone may grant PERMISSION_RETURN_OBJECTS this function will only work properly if one of the following is true: - The land is owned by the prim owner and this permission has been granted by the land owner. - The land is group owned and this permission has been granted by a group member filling the group "Owners" role. |

- Parcel owner, estate owner and estate managers can not have their objects returned by this method.
- Objects which are owned by the group the land is set to will not be returned by this method.

  - Objects owned by other groups will be returned to their previous owner if the object is transferable. If not transferable they are deleted.

## Notes

For group-owned land you may want to explicitly code a group owner's key into the script as there is no way to determine if a user is a group owner.

## See Also

### Events

- **run_time_permissions** — Permission receiving event

### Functions

- **llGetPermissions** — Get the permissions granted
- **llGetPermissionsKey** — Get the agent who granted permissions
- **llRequestPermissions** — Request permissions
- llReturnObjectsByID
- llGetParcelPrimOwners
- llDie

### Articles

- Script permissions

<!-- /wiki-source -->
