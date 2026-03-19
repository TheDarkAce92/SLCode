---
name: "SLURL HUD"
category: "example"
type: "example"
language: "LSL"
description: "Touch to get the SLURL."
wiki_url: "https://wiki.secondlife.com/wiki/SLURL_HUD"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

Touch to get the SLURL.

```lsl
string slurl()
{
    string regionname = llGetRegionName();
    vector pos = llGetPos();

    return "http://maps.secondlife.com/secondlife/"
        + llEscapeURL(regionname) + "/"
        + (string)llRound(pos.x) + "/"
        + (string)llRound(pos.y) + "/"
        + (string)llRound(pos.z) + "/";
}

default
{
    touch_start(integer num_detected)
    {
        // PUBLIC_CHANNEL has the integer value 0
        llSay(PUBLIC_CHANNEL, slurl() );
    }
}
```