---
name: "BuildSlurl (NewAge)"
category: "example"
type: "example"
language: "LSL"
description: "A way of creating SLURL's by using a pre-made function;"
wiki_url: "https://wiki.secondlife.com/wiki/BuildSlurl_(NewAge)"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

A way of creating SLURL's by using a pre-made function;

```lsl
BuildSlurl(string region_name, vector pos);
```

*Pre-made Function*

```lsl
string BuildSlurl(string region_name, vector pos){
    return "secondlife://" + llEscapeURL(region_name)
            + "/"+ (string)((integer)pos.x)
            + "/"+ (string)((integer)pos.y)
            + "/"+ (string)(llCeil(pos.z));
}
```

*Example Script*

```lsl
string BuildSlurl(string region_name, vector pos){
    return "secondlife://" + llEscapeURL(region_name)
            + "/"+ (string)((integer)pos.x)
            + "/"+ (string)((integer)pos.y)
            + "/"+ (string)(llCeil(pos.z));
}

default
{
    touch_start(integer x)
    {
        llWhisper(0, BuildSlurl(llGetRegionName(), llGetPos()));
        //Returns slurl like this;
        //       secondlife://Phoenix%20Rising/214/160/24
    }
}
```