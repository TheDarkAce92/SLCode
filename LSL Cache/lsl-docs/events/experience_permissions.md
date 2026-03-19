---
name: "experience_permissions"
category: "event"
type: "event"
language: "LSL"
description: "The agent has approved an experience permissions request.  This may be through interaction with the experience permission dialog or the experience profile, or automatically if the agent has previously approved the experience."
signature: "experience_permissions(key agent_id)"
wiki_url: 'https://wiki.secondlife.com/wiki/experience_permissions'
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
deprecated: "false"
parameters: []
---

The agent has approved an experience permissions request.  This may be through interaction with the experience permission dialog or the experience profile, or automatically if the agent has previously approved the experience.


## Signature

```lsl
experience_permissions(key agent_id)
{
    // your code here
}
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `key` | `agent_id` | avatar UUID that is in the same region  |


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/experience_permissions)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/experience_permissions) — scraped 2026-03-18_

## Examples

```lsl
default
{
    touch_start(integer total_number)
    {
        llRequestExperiencePermissions(llDetectedKey(0), "");
    }

    experience_permissions(key agent_id)
    {
        llSay(0, "Experience permissions granted for " + (string)agent_id);
    }

    experience_permissions_denied(key agent_id, integer reason)
    {
        llSay(0, "Experience permissions denied for " + (string)agent_id + " due to reason #" + (string)reason);
    }
}
```

## See Also

### Events

experience_permissions_denied

### Functions

llRequestExperiencePermissions

<!-- /wiki-source -->
