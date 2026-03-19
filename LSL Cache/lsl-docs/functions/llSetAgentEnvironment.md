---
name: "llSetAgentEnvironment"
category: "function"
type: "function"
language: "LSL"
description: "This function sets environment values for an individual agent in an experience. The changes to the environment persist until the agent moves to a new region or llSetAgentEnvironment is called for an agent with an empty list. Passing an empty list in params will strip all environmental settings appli"
signature: "integer llSetAgentEnvironment(key agent_id, float transition, list params)"
return_type: "integer"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llSetAgentEnvironment'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
flags: "experience-api"
---

This function sets environment values for an individual agent in an experience. The changes to the environment persist until the agent moves to a new region or llSetAgentEnvironment is called for an agent with an empty list. Passing an empty list in params will strip all environmental settings applied to this agent as part of the experience


## Signature

```lsl
integer llSetAgentEnvironment(key agent_id, float transition, list params);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| ` key` | ` agent_id` | The key for an agent in the region. The agent must be in the region and must be participating in the experience. |
| ` float` | ` transition` | The number of seconds over which to transition to the new settings. |
| ` list` | ` params` | A list of parameters to retrieve from the current environment. |


## Return Value

Returns `integer`.


## Caveats

- Energy cost: **10.0**.
- Requires an active **Experience** (Experience API function).


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llSetAgentEnvironment)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llSetAgentEnvironment) — scraped 2026-03-18_

This function sets environment values for an individual agent in an experience. The changes to the environment persist until the agent moves to a new region or llSetAgentEnvironment is called for an agent with an empty list. Passing an empty list in params will strip all environmental settings applied to this agent as part of the experienceReturns an integer

## Caveats

- The list of valid parameters differs from those available for llGetEnvironment.
- The agent's viewer may choose to ignore this command.
- An environment set locally on the viewer will override any environment set from this function.

## Examples

```lsl
float gTransitionTime = 3.0;
list gListEnvironmentParams = [
    SKY_CLOUD_TEXTURE, TEXTURE_PLYWOOD,
    SKY_GAMMA, 10.0,
    WATER_NORMAL_SCALE, <5.0, 5.0, 5.0>
];

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
        integer envTest = llSetAgentEnvironment(agent_id, gTransitionTime, gListEnvironmentParams);
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

- llReplaceAgentEnvironment
- llGetEnvironment

<!-- /wiki-source -->
