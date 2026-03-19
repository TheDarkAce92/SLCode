---
name: "llReturnObjectsByID"
category: "function"
type: "function"
language: "LSL"
description: 'If the script is owned by an agent, PERMISSION_RETURN_OBJECTS may be granted by the owner.  If the script is owned by a group, this permission may be granted by an agent belonging to the group's 'Owners' role.

Returns an integer that is the number of objects successfully returned to their owners or'
signature: "integer llReturnObjectsByID(list objects)"
return_type: "integer"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llReturnObjectsByID'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llreturnobjectsbyid"]
---

If the script is owned by an agent, PERMISSION_RETURN_OBJECTS may be granted by the owner.  If the script is owned by a group, this permission may be granted by an agent belonging to the group's "Owners" role.

Returns an integer that is the number of objects successfully returned to their owners or an ERR_* flag.

If the return value is negative, it represents an error flag.


## Signature

```lsl
integer llReturnObjectsByID(list objects);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `list` | `objects` | list of object uuids (keys) |


## Return Value

Returns `integer`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llReturnObjectsByID)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llReturnObjectsByID) — scraped 2026-03-18_

If the script is owned by an agent, PERMISSION_RETURN_OBJECTS may be granted by the owner. If the script is owned by a group, this permission may be granted by an agent belonging to the group's "Owners" role.Returns an integer that is the number of objects successfully returned to their owners or an ERR_* flag.

## Caveats

| Permissions |
| --- |
| - Do not depend upon the auto-grant status of permissions. **Always** use the run_time_permissions event. - If the script lacks the permission PERMISSION_RETURN_OBJECTS, the script will shout an error on DEBUG_CHANNEL and the operation fails (but the script continues to run). - Once the PERMISSION_RETURN_OBJECTS permission is granted there is no way to revoke it except from inside the script (for example, with a new llRequestPermissions call) or the script is reset or deleted. - While anyone may grant PERMISSION_RETURN_OBJECTS this function will only work properly if one of the following is true: - The land is owned by the prim owner and this permission has been granted by the land owner. - The land is group owned and this permission has been granted by a group member filling the group "Owners" role. |

- Objects owned by other groups will be returned to their previous owner if the object is transferable, deleted otherwise.

## See Also

### Events

- **run_time_permissions** — Permission receiving event

### Functions

- **llGetPermissions** — Get the permissions granted
- **llGetPermissionsKey** — Get the agent who granted permissions
- **llRequestPermissions** — Request permissions
- llReturnObjectsByOwner
- llGetParcelPrimOwners
- llDie

### Articles

- Script permissions

<!-- /wiki-source -->
