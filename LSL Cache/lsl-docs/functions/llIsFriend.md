---
name: "llIsFriend"
category: "function"
type: "function"
language: "LSL"
description: "Returns an integer that is TRUE if agent_id and the owner of the prim the script is in are friends, otherwise FALSE."
signature: "integer llIsFriend(key agent)"
return_type: "integer"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llIsFriend'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
---

Returns an integer that is TRUE if agent_id and the owner of the prim the script is in are friends, otherwise FALSE.


## Signature

```lsl
integer llIsFriend(key agent);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `key` | `agent_id` |  |


## Return Value

Returns `integer`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llIsFriend)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llIsFriend) — scraped 2026-03-18_

Returns a boolean (an integer) that is TRUE if agent_id and the owner of the prim the script is in are friends, otherwise FALSE.

## Caveats

- You are not your own friend.

## Examples

```lsl
default
{
    state_entry()
    {
        llSensorRepeat("", NULL_KEY, AGENT, 95, PI, 10);
    }

    sensor(integer count)
    {
        integer index;
        for (index = 0; index < count; ++index)
        {
            string is_is_not = " is NOT ";
            if (llIsFriend(llDetectedKey(index)))
            {
                is_is_not = " is ";
            }
            llSay(0, llDetectedName(index) + is_is_not + "a friend.");
        }
    }
}
```

## See Also

### Functions

- llDetectedGroup
- llSameGroup

<!-- /wiki-source -->
