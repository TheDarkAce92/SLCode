---
name: "llGetParcelMusicURL"
category: "function"
type: "function"
language: "LSL"
description: 'Returns a string containing the parcel streaming audio URL.

The object owner must also be the land owner. If the land is deeded to a group the object will need to be deeded to the same group for this function to work.'
signature: "string llGetParcelMusicURL()"
return_type: "string"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetParcelMusicURL'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgetparcelmusicurl"]
---

Returns a string containing the parcel streaming audio URL.

The object owner must also be the land owner. If the land is deeded to a group the object will need to be deeded to the same group for this function to work.


## Signature

```lsl
string llGetParcelMusicURL();
```


## Return Value

Returns `string`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetParcelMusicURL)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetParcelMusicURL) — scraped 2026-03-18_

Returns a string containing the parcel streaming audio URL.

## Examples

```lsl
string parcel_music_url()
{
    string parcelMusicURL = llGetParcelMusicURL();

    if (parcelMusicURL != "")
        return parcelMusicURL;
//  else
        return "Sorry, could not retrieve parcel's music URL.\n"
            + "You'll either need to be the land owner or able to deed me.";

}

default
{
    touch_start(integer num_detected)
    {
        // PUBLIC_CHANNEL has the integer value 0
        llSay(PUBLIC_CHANNEL, parcel_music_url() );
    }
}
```

## See Also

### Functions

- **llSetParcelMusicURL** — Sets the music stream URL for the parcel object is on

<!-- /wiki-source -->
