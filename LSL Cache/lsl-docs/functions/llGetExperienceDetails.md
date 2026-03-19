---
name: "llGetExperienceDetails"
category: "function"
type: "function"
language: "LSL"
description: 'Returns a list of details about the experience. This list has 6 components: [string experience_name, key owner_id, key experience_id, integer state, string state_message, key group_id]

If experience_id is NULL_KEY, then information about the script's experience is returned. In this situation, if th'
signature: "list llGetExperienceDetails(key experience_id)"
return_type: "list"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetExperienceDetails'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
flags: "experience-api"
patterns: ["llgetexperiencedetails"]
---

Returns a list of details about the experience. This list has 6 components: [string experience_name, key owner_id, key experience_id, integer state, string state_message, key group_id]

If experience_id is NULL_KEY, then information about the script's experience is returned. In this situation, if the script isn't associated with an experience, an empty list is returned.


## Signature

```lsl
list llGetExperienceDetails(key experience_id);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `key` | `experience_id` | The ID of the experience to query. |


## Return Value

Returns `list`.


## Caveats

- Energy cost: **10.0**.
- Requires an active **Experience** (Experience API function).


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetExperienceDetails)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetExperienceDetails) — scraped 2026-03-18_

Returns a list of details about the experience. This list has 6 components: [string experience_name, key owner_id, key experience_id, integer state, string state_message, key group_id]

## Examples

```lsl
default
   {
       touch_start(integer total_number)
       {
           key xp = "9170c22b-f445-ea5d-89fa-0f2f1e144f04";
           llOwnerSay(llDumpList2String(llGetExperienceDetails(xp), "\n"));
           // Prints:
           // Linden Realms
           // id
           // status msg

           llOwnerSay(llDumpList2String(llGetExperienceDetails(NULL_KEY), "\n"));
           // Print nothing if not associated with an XP or info about the associated experience
       }
   }
```

## Notes

#### Compiling

For a script to be associated with an Experience...

- It must be compiled with a client that is Experience aware,
- The "Use Experience" checkbox must be checked,
- And one of the users Experience keys selected.

|  | Important: Not all TPVs have this functionality. |
| --- | --- |

## See Also

### Functions

- llAgentInExperience

<!-- /wiki-source -->
