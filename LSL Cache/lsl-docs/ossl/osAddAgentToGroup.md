---
name: "osAddAgentToGroup"
category: "function"
type: "function"
language: "OSSL"
description: "Adds an agent to a named group and optionally assigns a requested role."
signature: "integer osAddAgentToGroup(key AgentID, string GroupName, string RequestedRole)"
return_type: "integer"
energy_cost: ""
sleep_time: ""
wiki_url: "https://opensimulator.org/wiki/osAddAgentToGroup"
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-19"
---

Adds an agent to a named group and optionally assigns a requested role.

## Syntax

```lsl
integer osAddAgentToGroup(key AgentID, string GroupName, string RequestedRole)
```

## Parameters

| Type | Name |
|------|------|
| `key` | `AgentID` |
| `string` | `GroupName` |
| `string` | `RequestedRole` |

## Return Value

`integer`

## Notes

- OSSL function — requires appropriate threat level in the region's OpenSim configuration.
- See: [https://opensimulator.org/wiki/osAddAgentToGroup](https://opensimulator.org/wiki/osAddAgentToGroup)
