---
name: "llGetAgentInfo"
category: "function"
type: "function"
language: "LSL"
description: "Returns a bit field (an integer) containing the agent information about id."
signature: "integer llGetAgentInfo(key id)"
return_type: "integer"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetAgentInfo'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgetagentinfo"]
---

Returns a bit field (an integer) containing the agent information about id.


## Signature

```lsl
integer llGetAgentInfo(key id);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `key` | `id` | avatar UUID that is in the same region |


## Return Value

Returns `integer`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetAgentInfo)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetAgentInfo) — scraped 2026-03-18_

Returns a bit field (an integer) containing the agent information about id.

## Caveats

- AGENT_BUSY indicates that the "busy" internal animation is playing, even if the user is not truly in busy mode.
- **On server 1.40 and below**, AGENT_TYPING indicated that the "type" internal animation is playing, it would not be set if the user disabled PlayTypingAnim. **On server 1.42 and up**, it reflects typing start/stop messages from the client and does not depend on the  animation. If the old behavior is desired, use llGetAnimationList and look for "c541c47f-e0c0-058b-ad1a-d6ae3a4584d9" — [SVC-787](https://jira.secondlife.com/browse/SVC-787)
- `AGENT_ALWAYS_RUN | AGENT_WALKING` indicates that the user requested to run using standard viewer controls. Use llGetAnimation to also detect running caused by physics.
- This function does not return reliable information immediately after a border crossing. Use llGetAnimation instead, if you can. — [SVC-3177](https://jira.secondlife.com/browse/SVC-3177)
- AGENT_AUTOMATED may unexpectedly be enabled, see its caveats for more detail.

## Examples

```lsl
default
{
    touch_start(integer buf)
    {
        buf = llGetAgentInfo(llDetectedKey(0));
        string out;
        if(buf & AGENT_FLYING)
            out += "The agent is flying.\n";
        else
            out += "The agent is not flying.\n";

        if(buf & AGENT_ATTACHMENTS)
        {
            if(buf & AGENT_SCRIPTED)
                out += "The agent has scripted attachments.\n";
            else
                out += "The agent's attachments are unscripted.\n";
        }
        else
            out += "The agent does not have attachments.\n";

        if(buf & AGENT_MOUSELOOK)
            out += "the agent is in mouselook.";
        else
            out += "the agent is in normal camera mode.";
        llWhisper(0, out);
    }
}
```

## Notes

This is not a good way of testing if an avatar is in the region, use llGetAgentSize instead.

## See Also

### Functions

- llRequestAgentData
- llGetAnimation
- llGetAnimationList

<!-- /wiki-source -->
