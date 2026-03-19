---
name: "llRequestUsername"
category: "function"
type: "function"
language: "LSL"
description: "Requests the Username of the agent identified by id. When the Username is available the dataserver event will be raised. The agent identified by id does not need to be in the same region or online at the time of the request.Returns a handle (a key) that is used to identify the dataserver event when "
signature: "key llRequestUsername(key id)"
return_type: "key"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llRequestUsername'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llrequestusername"]
---

Requests the Username of the agent identified by id. When the Username is available the dataserver event will be raised. The agent identified by id does not need to be in the same region or online at the time of the request.Returns a handle (a key) that is used to identify the dataserver event when it is raised.
If id is not the UUID of an avatar, the dataserver event is not raised.

If the name has been changed some time in the past, this provides only the current name.


## Signature

```lsl
key llRequestUsername(key id);
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

- [SL Wiki](https://wiki.secondlife.com/wiki/llRequestUsername)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llRequestUsername) — scraped 2026-03-18_

Requests the Username of the agent identified by id. When the Username is available the dataserver event will be raised. The agent identified by id does not need to be in the same region or online at the time of the request.Returns a handle (a key) that is used to identify the dataserver event when it is raised. If id is not the UUID of an avatar, the dataserver event is not raised.

## Caveats

- If you merely wish to show the agent username in the viewer window, it may be more straightforward to use Viewer URI Name Space and avoid a dataserver event, e.g.:

```lsl
llSay(0, "secondlife:///app/agent/" + (string)id + "/username");
```
- This function is throttled. The throttle is undocumented, but as of October 2018 the function appears to support bursts of up to 20 requests and sustained use at an average rate of 1.9 requests per second per owner, per region. (Meaning the throttle applies to all objects in the region with the same owner.) Once tripped, the function fails and says "Too many llRequestUsername requests.  Throttled until average falls." on DEBUG_CHANNEL.

## Examples

```lsl
key owner_name_query;

default
{
    state_entry()
    {
        owner_name_query = llRequestUsername(llGetOwner());
    }

    dataserver(key queryid, string data)
    {
        if ( owner_name_query == queryid )
        {
            llSay(0, "The username of the owner of this script : " + data);
        }
    }
}
```

## See Also

### Events

- dataserver

### Functions

- **llGetUsername** — works only for avatars that are present
- **llRequestUserKey** — general way to translate a name to a key

<!-- /wiki-source -->
