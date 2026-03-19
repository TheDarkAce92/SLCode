---
name: "llRequestUserKey"
category: "function"
type: "function"
language: "LSL"
description: 'Requests the Agent ID for the agent identified by name from the dataserver. The name given may be either the current name of an avatar or a historical name that has been used in the past. If no agent can be found with the supplied name this function returns the value NULL_KEY.

Returns a handle (a k'
signature: "key llRequestUserKey(string name)"
return_type: "key"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llRequestUserKey'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
---

Requests the Agent ID for the agent identified by name from the dataserver. The name given may be either the current name of an avatar or a historical name that has been used in the past. If no agent can be found with the supplied name this function returns the value NULL_KEY.

Returns a handle (a key) that can be used to identify the request when the dataserver event is raised.

The agent being searched for with this function does not need to be signed on to Second Life.


## Signature

```lsl
key llRequestUserKey(string name);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `string` | `username` | the username of the avatar to retrieve the UUID of. |


## Return Value

Returns `key`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llRequestUserKey)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llRequestUserKey) — scraped 2026-03-18_

Requests the Agent ID for the agent identified by name from the dataserver. The name given may be either the current name of an avatar or a historical name that has been used in the past. If no agent can be found with the supplied name this function returns the value NULL_KEY.

## Caveats

- This function is throttled. The throttle is undocumented, but as of October 2018 the function appears to support bursts of up to 20 requests and sustained use at an average rate of 1.9 requests per second per owner, per region. (Meaning the throttle applies to all objects in the region with the same owner.) Once tripped, the function fails and says "Too many llRequestUserKey requests.  Throttled until average falls." on DEBUG_CHANNEL.
- This function will return a NULL_KEY for any agent that has yet to log on to the grid the function is used on.

## Examples

```lsl
key name_key_query;
default
{
   state_entry()
   {
       name_key_query = llRequestUserKey("rider.linden");
   }

   dataserver(key queryid, string data)
   {
       if ( name_key_query == queryid )
       {
           llSay(0, "The key for this user is : " + data);
       }
   }
}
```

## Notes

Names are always provided in the form "First[ Last]" or "first[.last]" (first name with an optional last name.) If the last name is omitted a last name of "Resident" is assumed. Case is not considered when resolving agent names.

## See Also

### Functions

- **llRequestUsername** — to translate a key to a name
- **llName2Key** — to fetch avatar UUID by name.

<!-- /wiki-source -->
