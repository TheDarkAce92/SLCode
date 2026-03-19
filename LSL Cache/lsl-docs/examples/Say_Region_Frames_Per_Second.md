---
name: "Say Region Frames Per Second"
category: "example"
type: "example"
language: "LSL"
description: "llSay(0, \"Region '\" + region + \"' is running at \" + (string)fps + \" fps.\");"
wiki_url: "https://wiki.secondlife.com/wiki/Say_Region_Frames_Per_Second"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

```lsl
default
{
    touch_start(integer num_detected)
    {
        float fps = llGetRegionFPS();
        string region = llGetRegionName();

        llSay(0, "Region '" + region + "' is running at " + (string)fps + " fps.");

        string moreInfo = "CAUTION: '" + region + "' is in danger of crashing.";

        if (fps > 15)
            moreInfo = "'" + region + "' is running slowly.");

        if (fps > 27)
            moreInfo = "'" + region + "' is running smoothly.");

        llSay(0, moreInfo);
    }
}
```