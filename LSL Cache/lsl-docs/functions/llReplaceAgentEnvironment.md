---
name: "llReplaceAgentEnvironment"
category: "function"
type: "function"
language: "LSL"
description: "The llReplaceAgentEnvironment function overrides the current region and parcel environment seen by an agent. The new environment persists until the agent crosses to a new region or this function is called with the NULL_KEY or empty string in the environment parameter for the particular agent, doing "
signature: "integer llReplaceAgentEnvironment(key agent_id, float transition, string environment)"
return_type: "integer"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llReplaceAgentEnvironment'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
flags: "experience-api"
---

The llReplaceAgentEnvironment function overrides the current region and parcel environment seen by an agent. The new environment persists until the agent crosses to a new region or this function is called with the NULL_KEY or empty string in the environment parameter for the particular agent, doing so will strip all environmental settings applied to this agent as part of the experience. This function must be executed as part of an experience.


## Signature

```lsl
integer llReplaceAgentEnvironment(key agent_id, float transition, string environment);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `key` | `agent_id` | The key for an agent in the region. The agent must be in the region and must be participating in the experience. |
| `float` | `transition` | The number of seconds over which to transition to the new settings. |
| `string` | `environment` | The name of an environmental setting in the object's inventory or the asset ID for an environment. |


## Return Value

Returns `integer`.


## Caveats

- Energy cost: **10.0**.
- Requires an active **Experience** (Experience API function).


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llReplaceAgentEnvironment)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llReplaceAgentEnvironment) — scraped 2026-03-18_

The llReplaceAgentEnvironment function overrides the current region and parcel environment seen by an agent. The new environment persists until the agent crosses to a new region or this function is called with the NULL_KEY or empty string in the environment parameter for the particular agent, doing so will strip all environmental settings applied to this agent as part of the experience. This function must be executed as part of an experience.Returns an Integer

## Caveats

- The agent's viewer may choose to ignore this command.
- An environment set locally on the viewer will override any environment set from this function.
- If a UUID is passed as the environment parameter and that UUID does not specify an environment setting, the viewer quietly ignores the instruction.

## Examples

```lsl
string gEnvironment = "A-12AM"; // Can be asset's name in object's inventory or the asset ID
float gTransitionTime = 3.0;

default
{
    touch_start(integer total_number)
    {
        key person = llDetectedKey(0);
        if (llGetAgentSize(person) != ZERO_VECTOR)
        {
            llRequestExperiencePermissions(person, "");
        }
        else
        {
            llInstantMessage(person, "You need to be in the same region to change environment");
        }
    }

    experience_permissions(key agent_id)
    {
        integer envTest = llReplaceAgentEnvironment(agent_id, gTransitionTime, gEnvironment);
        if (envTest == 1)
        {
            llRegionSayTo(agent_id, 0, "Applying environment for " + (string)agent_id);
        }
        else
        {
            llRegionSayTo(agent_id, 0, "Cannot apply environment for " + (string)agent_id + " due to reason id: " + (string)envTest);
        }
    }

    experience_permissions_denied(key agent_id, integer reason)
    {
        llRegionSayTo(agent_id, 0, "Denied experience permissions for " + (string)agent_id + " due to reason id: " + (string)reason);
    }
}
```

## See Also

### Functions

- llSetAgentEnvironment
- llGetEnvironment

<!-- /wiki-source -->
