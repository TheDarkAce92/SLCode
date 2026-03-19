---
name: "llParcelMediaCommandList"
category: "function"
type: "function"
language: "LSL"
description: "Controls the playback of movies and other multimedia resources on a parcel or for an agent."
signature: "void llParcelMediaCommandList(list command)"
return_type: "void"
sleep_time: "2.0"
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llParcelMediaCommandList'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llparcelmediacommandlist"]
---

Controls the playback of movies and other multimedia resources on a parcel or for an agent.


## Signature

```lsl
void llParcelMediaCommandList(list command);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `list` | `commandList` | A list of integer PARCEL_MEDIA_COMMAND_* flags and their parameters |


## Caveats

- Forced delay: **2.0 seconds** — the script sleeps after each call.
- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llParcelMediaCommandList)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llParcelMediaCommandList) — scraped 2026-03-18_

Controls the playback of movies and other multimedia resources on a parcel or for an agent.

## Caveats

- This function causes the script to sleep for 2.0 seconds.
- This script's object must be owned by the landowner or the function will silently fail.
- If the script's object is over group owned land, then the object must be deeded to **that** group.
- If the PARCEL_MEDIA_COMMAND_URL value is greater than 254 characters, the command will silently fail.
- If using PARCEL_MEDIA_COMMAND_URL and PARCEL_MEDIA_COMMAND_AGENT, make sure the *Media URL* in the *About Land ...* dialog is unset. See [SVC-4478](https://jira.secondlife.com/browse/SVC-4478).

## Examples

```lsl
key myTexture = llGetTexture(0);
llParcelMediaCommandList([PARCEL_MEDIA_COMMAND_TEXTURE,myTexture,PARCEL_MEDIA_COMMAND_PLAY]);
```

## See Also

### Functions

- llParcelMediaQuery
- llSetTextureAnim
- llSetTexture

<!-- /wiki-source -->
