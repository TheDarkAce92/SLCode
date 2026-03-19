---
name: "llAgentInExperience"
category: "function"
type: "function"
language: "LSL"
description: 'Determines whether or not the specified agent is in the script's experience.

Returns a boolean (an integer) that is TRUE if the agent is in the experience and the experience can run in the current region.'
signature: "integer llAgentInExperience(key agent)"
return_type: "integer"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llAgentInExperience'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
flags: "experience-api"
patterns: ["llagentinexperience"]
---

Determines whether or not the specified agent is in the script's experience.

Returns a boolean (an integer) that is TRUE if the agent is in the experience and the experience can run in the current region.


## Signature

```lsl
integer llAgentInExperience(key agent);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `key` | `agent` | avatar UUID that is in the same region to query. |


## Return Value

Returns `integer`.


## Caveats

- Energy cost: **10.0**.
- Requires an active **Experience** (Experience API function).


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llAgentInExperience)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llAgentInExperience) — scraped 2026-03-18_

Determines whether or not the specified agent is in the script's experience.Returns a boolean (an integer) that is TRUE if the agent is in the experience and the experience can run in the current region.

## Caveats

- Agent must be over a parcel that has the Experience allowed or FALSE is returned with Land Scope Experience compiled scripts.

## Examples

```lsl
default
{
  touch_start(integer total_number)
  {
    if(llAgentInExperience(llDetectedKey(0)))
    {
      llOwnerSay(llDetectedName(0)+ " is in my experience");
    }
    else
    {
      llOwnerSay(llDetectedName(0)+ " is not in my experience");
    }
  }
}
```

## See Also

### Functions

- llGetExperienceDetails

<!-- /wiki-source -->
