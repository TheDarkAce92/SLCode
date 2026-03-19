---
name: "llSitOnLink"
category: "function"
type: "function"
language: "LSL"
description: 'The avatar specified by agent_id is forced to sit on the sit target of the prim indicated by the link parameter. If the specified link is already occupied, the simulator searches down the chain of prims in the link set looking for an available sit target.

If successful, this method returns 1.

If t'
signature: "integer llSitOnLink(key agent_id, integer link)"
return_type: "integer"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llSitOnLink'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
flags: "experience-api"
patterns: ["llsitonlink"]
---

The avatar specified by agent_id is forced to sit on the sit target of the prim indicated by the link parameter. If the specified link is already occupied, the simulator searches down the chain of prims in the link set looking for an available sit target.

If successful, this method returns 1.

If the function fails, it returns a negative number constant.

Link constants that indicate a single prim may be used for the link parameter. These are LINK_ROOT and LINK_THIS. Other constants such as LINK_SET, LINK_CHILDREN, LINK_ALL_OTHERS will return an INVALID_LINK error.

This method must be called from an experience enabled script running on land that has enabled the experience key. If these conditions are not met this method returns a NOT_EXPERIENCE error.

The targeted avatar must also have accepted the experience. If the user is not participating in the experience this method returns NO_EXPERIENCE_PERMISSION. If the avatar id can not be found or is not over land that has enabled the experience this method returns INVALID_AGENT.

If there are no valid sit targets remaining in the linkset this method returns NO_SIT_TARGET and no action is taken with the avatar.

If the avatar does not have access to the parcel containing the prim running this script, this call fails.


## Signature

```lsl
integer llSitOnLink(key agent_id, integer link);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `key` | `agent_id` | UUID of the avatar being forced to sit |
| `integer` | `link` | Link number for the prim containing the desired sit target |


## Return Value

Returns `integer`.


## Caveats

- Energy cost: **10.0**.
- Requires an active **Experience** (Experience API function).


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llSitOnLink)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llSitOnLink) — scraped 2026-03-18_

The avatar specified by agent_id is forced to sit on the sit target of the prim indicated by the link parameter. If the specified link is already occupied, the simulator searches down the chain of prims in the link set looking for an available sit target.Returns an Integer

## Examples

```lsl
integer gLinkId = LINK_THIS;

default
{
    touch_start(integer total_number)
    {
        llRequestExperiencePermissions(llDetectedKey(0), "");
    }

    experience_permissions(key agent_id)
    {
        integer sitTest = llSitOnLink(agent_id, gLinkId);
        if (sitTest != 1)
        {
            llInstantMessage(agent_id, "Cannot force agent " + (string)agent_id + " to sit due to reason id: " + (string)sitTest);
        }
    }

    experience_permissions_denied(key agent_id, integer reason)
    {
        llInstantMessage(agent_id, "Denied experience permissions for " + (string)agent_id + " due to reason id: " + (string)reason);
    }
}
```

## Notes

This function was introduced in conjunction with new primitive parameter constants: PRIM_ALLOW_UNSIT, PRIM_SCRIPTED_SITS_ONLY, and PRIM_SIT_TARGET.

## See Also

### Functions

- llLinkSitTarget
- llSitTarget
- llSetSitText
- llAvatarOnLinkSitTarget
- llAvatarOnSitTarget
- llUnSit

### Constants

- PRIM_ALLOW_UNSIT
- PRIM_SCRIPTED_SIT_ONLY
- PRIM_SIT_TARGET

<!-- /wiki-source -->
