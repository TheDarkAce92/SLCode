---
name: "llGetUsername"
category: "function"
type: "function"
language: "LSL"
description: 'Returns a string that is the unique username of the avatar specified by id.

id must specify a valid avatar key, present in or otherwise known to the sim in which the script is running, otherwise an empty string is returned. This function will still return a valid username if the avatar is a child a'
signature: "string llGetUsername(key id)"
return_type: "string"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetUsername'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgetusername"]
---

Returns a string that is the unique username of the avatar specified by id.

id must specify a valid avatar key, present in or otherwise known to the sim in which the script is running, otherwise an empty string is returned. This function will still return a valid username if the avatar is a child agent of the sim (i.e., in an adjacent sim, but presently able to see into the one the script is in), or for a short period after the avatar leaves the sim (specifically, when the client completely disconnects from the sim, either as a main or child agent).


## Signature

```lsl
string llGetUsername(key id);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `key` | `id` | avatar UUID that is in the same region or is otherwise known to the region |


## Return Value

Returns `string`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetUsername)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetUsername) — scraped 2026-03-18_

Returns a string that is the unique username of the avatar specified by id.

## Caveats

- To get around the "avatar must be present" limitation, you can use the llRequestUsername function and the dataserver event to obtain the avatar's username from a key.
- There is no opposite function (llUsername2Key) available. For Name2Key services see llKey2Name.
- "" can be returned if the region is unable to resolve the username. This can happen even if the avatar is present and display names are enabled on the region. Do not rely on this function to verify avatar presence.
- If you merely wish to show the agent username in the viewer window, it may be more straightforward to use Viewer URI Name Space, e.g.:

```lsl
llSay(0, "secondlife:///app/agent/" + (string)id + "/username");
```

## Examples

```lsl
// Best viewed in Chat History (ctrl-h)
default
{
    collision_start(integer a)//Announce who collided
    {
        llSay(0, "llGetDisplayName: " + llGetDisplayName(llDetectedKey(0)) +
               "\nllGetUsername: " + llGetUsername(llDetectedKey(0)));
    }
    touch_start(integer a)
    {
        llSay(0,"llGetDisplayName: " + llGetDisplayName(llDetectedKey(0)) +
               "\nllGetUsername: " + llGetUsername(llDetectedKey(0)));
    }
}
```

## See Also

### Functions

- llGetDisplayName
- **llRequestUsername** — dataserver

<!-- /wiki-source -->
