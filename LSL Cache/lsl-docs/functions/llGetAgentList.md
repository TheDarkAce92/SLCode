---
name: "llGetAgentList"
category: "function"
type: "function"
language: "LSL"
description: 'Requests a list of agents currently in the region, limited by the scope parameter.

Returns a list [key id0, key id1, ..., key idn] or [string error_msg] - returns avatar keys for all agents in the region limited to the area(s) specified by scope'
signature: "list llGetAgentList(integer scope, list options)"
return_type: "list"
sleep_time: ""
energy_cost: ""
wiki_url: 'https://wiki.secondlife.com/wiki/llGetAgentList'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgetagentlist"]
---

Requests a list of agents currently in the region, limited by the scope parameter.

Returns a list [key id0, key id1, ..., key idn] or [string error_msg] - returns avatar keys for all agents in the region limited to the area(s) specified by scope


## Signature

```lsl
list llGetAgentList(integer scope, list options);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `integer` | `scope` | AGENT_LIST_* flag specifies the selection scope
* AGENT_LIST_PARCEL - returns only agents on the same parcel where the script is running.
* AGENT_LIST_PARCEL_OWNER - returns only agents on any parcel in the region where the parcel owner is the same as the owner of the parcel under the scripted object.
* AGENT_LIST_REGION - returns any/all agents in the region. |
| `list (instructions)` | `options` | Unused. |


## Return Value

Returns `list`.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetAgentList)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetAgentList) — scraped 2026-03-18_

Requests a list of agents currently in the region, limited by the scope parameter.Returns a list [key id0, key id1, ..., key idn] or [string error_msg] - returns avatar keys for all agents in the region limited to the area(s) specified by scope

## Caveats

- There is no guaranteed understandable order or randomness to the list returned.
- Will only return up to 100 agents.
- Ghosts, agents that leave behind a corrupted presence and agents in God Mode depending on the level will have NULL_KEY returned instead of their real key with llGetAgentList(). There is also an issue with a certain type of ghosted agent still returning a key too. Perhaps check each key against llGetAgentSize() to verify if they're really in the sim or not; none of the above anomalies affect llGetAgentSize().

## Examples

|  | Important: To check if an avatar is in the same sim, please check whether llGetAgentSize does NOT return ZERO_VECTOR. It's much faster and easier than calling llGetAgentList and running through the list to compare a given key with each list item. |
| --- | --- |

|  | Important: As of now, this function does not have a delimiter for its option list. This means, the function MIGHT return up to a hundred avatar keys. You'll need a lot of free memory to be able to store those keys, be warned of possible STACK_HEAP_COLLISION_ERRORs. |
| --- | --- |

```lsl
//Displays up to 100 avatar key: name pairs detected in the entire region

default
{
    touch_start(integer total_number)
    {
        list avatarsInRegion = llGetAgentList(AGENT_LIST_REGION, []);
        integer numOfAvatars = llGetListLength(avatarsInRegion);

        // if no avatars, abort avatar listing process and give a short notice
        if (!numOfAvatars)
        {
            llOwnerSay("No avatars found within the region!");
            return;
        }

        integer index;
        while (index < numOfAvatars)
        {
            key id = llList2Key(avatarsInRegion, index);
            string name = llKey2Name(id);

            llOwnerSay(name + " [ " + (string)id + " ]");
            ++index;
        }
    }
}
```

```lsl
//  Orders new list based on distance
//  and returns names and distances on touch

default
{
    touch_start(integer num_detected)
    {
        list keys = llGetAgentList(AGENT_LIST_REGION, []);
        integer numberOfKeys = llGetListLength(keys);

        vector currentPos = llGetPos();
        list newkeys;
        key thisAvKey;

        integer i;
        for (i = 0; i < numberOfKeys; ++i) {
            thisAvKey = llList2Key(keys,i);
            newkeys += [llRound(llVecDist(currentPos,
                            llList2Vector(llGetObjectDetails(thisAvKey, [OBJECT_POS]), 0))),
                        thisAvKey];
        }

        newkeys = llListSort(newkeys, 2, FALSE);     //  sort strided list by descending distance

        for (i = 0; i < (numberOfKeys * 2); i += 2) {
            llOwnerSay(llGetDisplayName(llList2Key(newkeys, i+1))
                +" ["+ (string) llList2Integer(newkeys, i) + "m]");
        }
    }
}
```

## See Also

### Functions

- llGetRegionAgentCount

<!-- /wiki-source -->
