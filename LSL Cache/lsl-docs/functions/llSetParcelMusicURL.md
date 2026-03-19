---
name: "llSetParcelMusicURL"
category: "function"
type: "function"
language: "LSL"
description: 'Sets the streaming audio URL for the parcel object is on

The object owner must also be the land owner. If the land is deeded to a group the object will need to be deeded to the same group for this function to work.'
signature: "void llSetParcelMusicURL(string url)"
return_type: "void"
sleep_time: "2.0"
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llSetParcelMusicURL'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llsetparcelmusicurl"]
---

Sets the streaming audio URL for the parcel object is on

The object owner must also be the land owner. If the land is deeded to a group the object will need to be deeded to the same group for this function to work.


## Signature

```lsl
void llSetParcelMusicURL(string url);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `string` | `url` |  |


## Caveats

- Forced delay: **2.0 seconds** — the script sleeps after each call.
- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llSetParcelMusicURL)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llSetParcelMusicURL) — scraped 2026-03-18_

Sets the streaming audio URL for the parcel object is on

## Caveats

- This function causes the script to sleep for 2.0 seconds.

## Examples

```lsl
// This script changes the music URL based on time of day.

integer night = FALSE;
string nighturl = "http://205.188.215.228:8006";
string dayurl = "http://208.122.59.30:7156";

default
{
    state_entry()
    {
        llSetTimerEvent(10);
    }

    timer()
    {
        vector pos = llGetSunDirection();

        if ((pos.z < -.75) != night)
        {
            night = !night;
            if (night)
            {
                llSetParcelMusicURL(nighturl);
            }
            else
            {
                llSetParcelMusicURL(dayurl);
            }
        }
    }
}
```

## See Also

### Functions

- **llGetParcelMusicURL** — Gets the music stream URL for the parcel object is on

<!-- /wiki-source -->
