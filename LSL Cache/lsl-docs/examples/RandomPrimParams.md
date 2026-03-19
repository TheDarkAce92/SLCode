---
name: "RandomPrimParams"
category: "example"
type: "example"
language: "LSL"
description: "Simple script to show how to set random primitive parameters."
wiki_url: "https://wiki.secondlife.com/wiki/RandomPrimParams"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

Simple script to show how to set random primitive parameters.

```lsl
default
{
    state_entry()
    {
        // set timer to go off every other 5.0 seconds
        llSetTimerEvent(5.0);
    }

    timer()
    {
        vector color = ;

        // set random color on all sides of linkset with opaque as alpha value
        llSetLinkPrimitiveParamsFast(LINK_SET,
            [PRIM_COLOR, ALL_SIDES, color, (float)TRUE]);
    }
}
```