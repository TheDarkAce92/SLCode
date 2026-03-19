---
name: "llReplaceEnvironment"
category: "function"
type: "function"
language: "LSL"
description: "The llReplaceEnvironment function replaces the environment in a parcel or a region. Either for a single elevation track or the entire environment. The owner of the script must have permission to edit the environment on the destination parcel, or be an estate manage in the case of an entire region. I"
signature: "integer llReplaceEnvironment(vector position, string environment, integer track_no, integer day_length, integer day_offset)"
return_type: "integer"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llReplaceEnvironment'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
---

The llReplaceEnvironment function replaces the environment in a parcel or a region. Either for a single elevation track or the entire environment. The owner of the script must have permission to edit the environment on the destination parcel, or be an estate manage in the case of an entire region. In most cases errors are reported as a return value from the function (see table below). However, issues with the environment assets may be reported in the debug chat.


## Signature

```lsl
integer llReplaceEnvironment(vector position, string environment, integer track_no, integer day_length, integer day_offset);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `vector` | `position` | The position in the region of the parcel that will receive the new environment. To change the entire region use <-1, -1, -1>. The z component of the vector is ignored. |
| `string` | `environment` | The name of an environmental setting in the object's inventory or the asset ID for an environment. NULL_KEY or empty string to remove the environment. |
| `integer` | `track_no` | The elevation zone to change. 0 for water, 1 for ground level, 2 for sky 1000m, 3 for sky 2000m, 4 for sky 3000m. -1 to change all tracks. |
| `integer` | `day_length` | The length in seconds for the day cycle. -1 to leave unchanged. |
| `integer` | `day_offset` | The offset in seconds from UTC. -1 to leave unchanged. |


## Return Value

Returns `integer`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llReplaceEnvironment)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llReplaceEnvironment) — scraped 2026-03-18_

The llReplaceEnvironment function replaces the environment in a parcel or a region. Either for a single elevation track or the entire environment. The owner of the script must have permission to edit the environment on the destination parcel, or be an estate manage in the case of an entire region. In most cases errors are reported as a return value from the function (see table below). However, issues with the environment assets may be reported in the debug chat.Returns an Integer

## Caveats

- An environment set locally on the viewer will override any environment set from this function.
- A parameter override set by llSetEnvironment will be preserved after the environment is replaced by this function.  Call llSetEnvironment with an empty list parameter to clear any straggling overrides.
- The environment specified by this function is applied asynchronously, as the simulator must download the environment asset before applying it. This means that llGetEnvironment will not immediately reflect the new environment's parameters, although the delay is typically quite small.
- If a UUID is passed as the environment parameter and that UUID does not specify an environment setting or one can not be constructed, the function will return success (1) but will post a message to the debug channel.
- If the parcel is group-owned, the script must either be deeded to the group, or the script owner must have "Modify environment settings and day cycle" group ability **and** have an active agent in the sim.

## Examples

```lsl
//  Will set the entire region to the "Tropicalia" EEP from the Linden inventory when touched.
//  It will set all the tracks to the same EEP with 24 hour day and a -8 hour Day Offset.
//  The "Tropicalia" must be in the prims inventory with the script.
//
//  Limited to Estate Managers or Region owners.
//  Madi Perth - 4/17/2023

default
{

    touch_start(integer total_number)
    {
        llReplaceEnvironment(<-1, -1, -1>, "Tropicalia", -1, 86400, (86400-28800));
    }
}
```

## See Also

### Functions

- llSetAgentEnvironment
- llGetEnvironment
- llSetEnvironment

<!-- /wiki-source -->
