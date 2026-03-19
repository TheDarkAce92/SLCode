---
name: "llGetOwnerKey"
category: "function"
type: "function"
language: "LSL"
description: "Returns a key that is the owner of prim id"
signature: "key llGetOwnerKey(key id)"
return_type: "key"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetOwnerKey'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgetownerkey"]
---

Returns a key that is the owner of prim id


## Signature

```lsl
key llGetOwnerKey(key id);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `key` | `id` | prim UUID that is in the same region |


## Return Value

Returns `key`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetOwnerKey)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetOwnerKey) — scraped 2026-03-18_

Returns a key that is the owner of prim id

## Caveats

- Returns id if id is not found in the region or is not a prim.

  - Owner information becomes unavailable *immediately* on derez or detach. For example, if a prim chats at derez or detach time, id can be returned even inside listen events of nearby objects.
- Also returns id for avatars, use llGetAgentSize instead to distinguish them from prims that do not exist.
- Returns NULL_KEY if the id passed in is not a valid key

## Examples

```lsl
default
{
    state_entry()
    {
    //  listen to anything talking on channel 1
        llListen(1, "", NULL_KEY, "");
    //  Type "/1 " + message (such as "/1 poke") to chat 'message' on channel 1.
    }

    listen(integer channel, string name, key id, string message)
    {
        key ownerOfThisObject = llGetOwner();
        key ownerOfSpeaker = llGetOwnerKey(id);

    //  if whoever is talking is the owner of this object
    //  or if the owner of the object talking is the owner of this object
        if (ownerOfSpeaker == ownerOfThisObject)
        {
            llOwnerSay("'" + name + "' has the same owner as me ^_^");
        }
    }
}
```

## See Also

### Functions

- llKey2Name
- llRequestAgentData
- **llGetObjectDetails** — OBJECT_OWNER
- llGetOwner

<!-- /wiki-source -->
