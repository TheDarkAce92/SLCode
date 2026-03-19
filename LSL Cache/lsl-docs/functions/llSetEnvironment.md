---
name: "llSetEnvironment"
category: "function"
type: "function"
language: "LSL"
description: 'This function overrides the environmental settings for a region or a parcel. The owner of the script must have permission to modify the environment on the parcel or be an estate manager to change the entire region.

An override for a given parameter can be set at the region scope or parcel scope. It'
signature: "integer llSetEnvironment(vector position, list params)"
return_type: "integer"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llSetEnvironment'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
---

This function overrides the environmental settings for a region or a parcel. The owner of the script must have permission to modify the environment on the parcel or be an estate manager to change the entire region.

An override for a given parameter can be set at the region scope or parcel scope. It can also be set for a single sky track, all sky tracks, or both. If an override of a given parameter is specified for both an individual track and all tracks, the individual track's override takes priority.

Note that the list of valid parameters differs from those available for llGetEnvironment.


## Signature

```lsl
integer llSetEnvironment(vector position, list params);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| ` vector` | ` position` | The location on the region of the parcel to be changed. Use <-1, -1, z> for the entire region. The z-component specifies which sky track to change, based on elevation. Use z=-1 to set an override on the special 'all tracks' slot. |
| ` list` | ` params` | A list of parameters to change for the parcel or region. Passing an empty list will remove any modifications from previous calls to llSetEnvironment. |


## Return Value

Returns `integer`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llSetEnvironment)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llSetEnvironment) — scraped 2026-03-18_

This function overrides the environmental settings for a region or a parcel. The owner of the script must have permission to modify the environment on the parcel or be an estate manager to change the entire region.

## Caveats

- An environment set locally on the viewer will override any environment set from this function.
- When changing a parcel's environment it must first have had an environment set.
- If the parcel is group-owned, the script must either be deeded to the group, or the script owner must have "Modify environment settings and day cycle" group ability **and** have an active agent in the sim.

## See Also

### Functions

- llReplaceAgentEnvironment
- llGetEnvironment

<!-- /wiki-source -->
