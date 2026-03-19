---
name: "experience_permissions_denied"
category: "event"
type: "event"
language: "LSL"
description: "The agent has denied experience permission."
signature: "experience_permissions_denied(key agent_id, integer reason)"
wiki_url: 'https://wiki.secondlife.com/wiki/experience_permissions_denied'
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
deprecated: "false"
parameters: []
---

The agent has denied experience permission.


## Signature

```lsl
experience_permissions_denied(key agent_id, integer reason)
{
    // your code here
}
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `key` | `agent_id` | avatar UUID that is in the same region  |
| `integer (experience_error)` | `reason` | Reason for denial; one of the Experience Tools XP_ERROR_* errors flags. |


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/experience_permissions_denied)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/experience_permissions_denied) — scraped 2026-03-18_

## Examples

```lsl
// Simple experience watcher
string denied_region = "";
string experience_name = "";

default{
    state_entry(){
        llRequestExperiencePermissions(llGetOwner(), "");
        experience_name = llList2String(llGetExperienceDetails(NULL_KEY), 0);
    }

    experience_permissions(key agent){
        denied_region="";
        llOwnerSay("in "+ experience_name);
    }

    experience_permissions_denied(key agent, integer reason){
        denied_region = llGetRegionName( );
        llOwnerSay("out "+ experience_name);

    }

    changed(integer what){
        if(denied_region != "" && denied_region != llGetRegionName()){
           llRequestExperiencePermissions(llGetOwner(), "");
        }
    }
}
```

## See Also

### Events

experience permissions

### Functions

- llRequestExperiencePermissions
- llGetExperienceErrorMessage

<!-- /wiki-source -->
