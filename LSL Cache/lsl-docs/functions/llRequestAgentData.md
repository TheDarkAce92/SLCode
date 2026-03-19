---
name: "llRequestAgentData"
category: "function"
type: "function"
language: "LSL"
description: 'Requests data about agent id. When data is available the dataserver event will be raised

Returns the handle (a key) for the dataserver event when it is raised.'
signature: "key llRequestAgentData(key id, integer data)"
return_type: "key"
sleep_time: "0.1"
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llRequestAgentData'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llrequestagentdata"]
---

Requests data about agent id. When data is available the dataserver event will be raised

Returns the handle (a key) for the dataserver event when it is raised.


## Signature

```lsl
key llRequestAgentData(key id, integer data);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `key` | `id` | avatar UUID |
| `integer` | `data` | DATA_* flag |


## Return Value

Returns `key`.


## Caveats

- Forced delay: **0.1 seconds** — the script sleeps after each call.
- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llRequestAgentData)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llRequestAgentData) — scraped 2026-03-18_

Requests data about agent id. When data is available the dataserver event will be raisedReturns the handle (a key) for the dataserver event when it is raised.

## Caveats

- This function causes the script to sleep for 0.1 seconds.
- DATA_BORN is not UTC. It is Pacific Time based.
- It's worth restating: if the requested data does not exist - or if the key given is not for an agent - then dataserver will **not** be raised.

## Examples

**DATA_NAME**

```lsl
key owner_key;
key owner_name_query;
string owner_name;

default
{
    state_entry()
    {
        owner_key = llGetOwner();
        owner_name_query = llRequestAgentData(owner_key, DATA_NAME);
    }
    dataserver(key queryid, string data)
    {
        if ( owner_name_query == queryid )
        {
            owner_name = data;
            llSay(0, "The owner of this script is called : " + owner_name );
        }
    }
}//Anylyn Hax 06:19, 23 July 2007 (PDT)
```

**DATA_ONLINE**

```lsl
/*
    Server friendly online status example by Daemonika Nightfire.

    It is not a big load for the server to check every 2 minutes if there is an avatar in the region.
    But it is nonsense to trigger a dataserver event for online status when nobody is in the region.
    For this purpose, the script checks the number of avatars in the region on each pass.
*/

key owner;
float repeat = 120.0; // 60 - 120 sec. Recommended, faster than 60 seconds and LL will kick your XXX.

key status_request;
Status()
{
    integer agent_count = llGetRegionAgentCount();
    if(agent_count > 0) // skip the request if nobody is in the region
    {
        status_request = llRequestAgentData(owner, DATA_ONLINE);
    }
}

default
{
    state_entry()
    {
        owner = llGetOwner();
        llSetTimerEvent(repeat);
        Status();
    }

    timer()
    {
        Status();
    }

    dataserver(key queryid, string data)
    {
        if(queryid == status_request)
        {
            // requested data contains the string "0" or "1" for DATA_ONLINE
            // i convert it to an integer and use the boolean as index

            //list index = [   0,       1,     2(0+2), 3(1+2)  ]
            list status = ["OFFLINE","ONLINE",<1,0,0>,<0,1,0>];

            string text = llList2String(status,(integer)data);    // boolean/index = 0   or 1
            vector color = llList2Vector(status,(integer)data+2); // boolean/index = 0+2 or 1+2

            llSetText(text, color, 1.0);
        }
    }

    on_rez(integer Dae)
    {
        llResetScript();
    }
}
```

## See Also

### Events

- dataserver

### Functions

- llGetAgentInfo

<!-- /wiki-source -->
