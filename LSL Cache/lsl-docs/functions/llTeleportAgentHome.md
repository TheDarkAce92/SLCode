---
name: "llTeleportAgentHome"
category: "function"
type: "function"
language: "LSL"
description: 'Teleports avatar on owner's land to their home location without any warning, similar to a God Summons or dying.

Generally, the object owner must also be the land owner but there is an exception for land deeded to a group for group members with the 'Eject and freeze Residents on parcels' ability. Se'
signature: "void llTeleportAgentHome(key id)"
return_type: "void"
sleep_time: "5.0"
energy_cost: "100.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llTeleportAgentHome'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llteleportagenthome"]
---

Teleports avatar on owner's land to their home location without any warning, similar to a God Summons or dying.

Generally, the object owner must also be the land owner but there is an exception for land deeded to a group for group members with the "Eject and freeze Residents on parcels" ability. See #Ownership Limitations for details.


## Signature

```lsl
void llTeleportAgentHome(key id);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `key` | `avatar` | avatar UUID that is in the same region |


## Caveats

- Forced delay: **5.0 seconds** — the script sleeps after each call.
- Energy cost: **100.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llTeleportAgentHome)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llTeleportAgentHome) — scraped 2026-03-18_

Teleports avatar on owner's land to their home location without any warning, similar to a God Summons or dying.

## Caveats

- This function causes the script to sleep for 5.0 seconds.

## Examples

```lsl
default
{
    state_entry()
    {
        // floattext is red and opaque
        llSetText("Don't touch me!", <1.0, 0.0, 0.0>, 1.0);
    }

    touch_start(integer num_detected)
    {
        key id = llDetectedKey(0);

        llTeleportAgentHome(id);
    }
}
```

## See Also

### Functions

- llEjectFromLand
- llTeleportAgent
- llTeleportAgentGlobalCoords

<!-- /wiki-source -->
