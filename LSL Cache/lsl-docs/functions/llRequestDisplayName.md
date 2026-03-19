---
name: "llRequestDisplayName"
category: "function"
type: "function"
language: "LSL"
description: 'Requests the Display Name of the agent identified by id. When the Display Name is available the dataserver event will be raised. The agent identified by id does not need to be in the same region or online at the time of the request.

Returns the handle (a key) that is used to identify the dataserver'
signature: "key llRequestDisplayName(key id)"
return_type: "key"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llRequestDisplayName'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llrequestdisplayname"]
---

Requests the Display Name of the agent identified by id. When the Display Name is available the dataserver event will be raised. The agent identified by id does not need to be in the same region or online at the time of the request.

Returns the handle (a key) that is used to identify the dataserver event when it is raised.


## Signature

```lsl
key llRequestDisplayName(key id);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `key` | `id` | avatar UUID |


## Return Value

Returns `key`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llRequestDisplayName)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llRequestDisplayName) — scraped 2026-03-18_

Requests the Display Name of the agent identified by id. When the Display Name is available the dataserver event will be raised. The agent identified by id does not need to be in the same region or online at the time of the request.Returns the handle (a key) that is used to identify the dataserver event when it is raised.

## Caveats

- If the request fails for any reason, there will be no error notice or dataserver event. You may use a timer to check for stale requests.
- If you merely wish to show the agent display name in the viewer window, it may be more straightforward to use Viewer URI Name Space and avoid a dataserver event, e.g.:

```lsl
llSay(0, "secondlife:///app/agent/" + (string)id + "/displayname");
```

## Examples

```lsl
key owner_key;
key owner_name_query;
string owner_display_name;

default
{
    state_entry()
    {
        owner_key = llGetOwner();
        owner_name_query = llRequestDisplayName(owner_key);
    }
    dataserver(key queryid, string data)
    {
        if ( owner_name_query == queryid )
        {
            owner_display_name = data;
            llSay(0, "The display name of the owner of this script : " + owner_display_name );
        }
    }
}
```

## See Also

### Events

- dataserver

### Functions

- llGetDisplayName
- llRequestUsername

<!-- /wiki-source -->
