---
name: "llGetDisplayName"
category: "function"
type: "function"
language: "LSL"
description: 'Returns a string that is the non-unique display name of the avatar specified by id.

id must specify a valid avatar key, present in or otherwise known to the sim in which the script is running, otherwise an empty string is returned. This function will still return a valid display name if the avatar '
signature: "string llGetDisplayName(key id)"
return_type: "string"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetDisplayName'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgetdisplayname"]
---

Returns a string that is the non-unique display name of the avatar specified by id.

id must specify a valid avatar key, present in or otherwise known to the sim in which the script is running, otherwise an empty string is returned. This function will still return a valid display name if the avatar is a child agent of the sim (i.e., in an adjacent sim, but presently able to see into the one the script is in), or for a short period after the avatar leaves the sim (specifically, when the client completely disconnects from the sim, either as a main or child agent).


## Signature

```lsl
string llGetDisplayName(key id);
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

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetDisplayName)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetDisplayName) — scraped 2026-03-18_

Returns a string that is the non-unique display name of the avatar specified by id.

## Caveats

- To get around the "avatar must be present" limitation, you can use the llRequestDisplayName function and the dataserver event to obtain the avatar's display name from a key (this is slower).
- There is no opposite function (llDisplayName2Key) available since display names are non-unique.
- Either of `???` or `""` is returned if the region is unable to return display names. This can happen even if display names are enabled on the region, especially the first time a given key is checked. At least one retry may be advisable. Do not rely on this function to verify avatar presence.
- It is possible for `Loading...` to be returned if called before the region has had a chance to resolve the agent's display name.

  - Do *not* retry failed attempts indefinitely in a loop. In a few cases, a display name or username will not be returned for as long as the avatar is in the region.
- If you merely wish to show the agent display name in the viewer window, it may be more straightforward to use Viewer URI Name Space, e.g.:

```lsl
llSay(0, "secondlife:///app/agent/" + (string)id + "/displayname");
```

## Examples

```lsl
// Best viewed in Chat History (ctrl-h)
default
{
    collision_start(integer a)//Announce who collided
    {
        llSay(0, "llGetDisplayName: " + llGetDisplayName(llDetectedKey(0)) +
                 "\nllDetectedName: " + llDetectedName(0));
    }
    touch_start(integer a)
    {
        llSay(0, "llGetDisplayName: " + llGetDisplayName(llDetectedKey(0)) +
                 "\nllDetectedName: " + llDetectedName(0));
    }
}
```

## See Also

### Functions

- **llRequestDisplayName** — dataserver
- llGetUsername
- **llRequestUsername** — dataserver

<!-- /wiki-source -->
