---
name: "Go transparent when walking"
category: "example"
type: "example"
language: "LSL"
description: "An attachment that goes invisible when you walk and when you stop walking it becomes visible again. I don't know what this could be used for, though."
wiki_url: "https://wiki.secondlife.com/wiki/Go_transparent_when_walking"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

## A what?

An attachment that goes invisible when you walk and when you stop walking it becomes visible again. I don't know what this could be used for, though.

```lsl
key owner;

default
{
    on_rez(integer start_param)
    {
        llResetScript();
    }

    changed(integer change)
    {
        if (change & (CHANGED_OWNER | CHANGED_INVENTORY))
            llResetScript();
    }

    state_entry()
    {
        owner = llGetOwner();
        llSetTimerEvent(1.0);
    }

    timer()
    {
        integer ownerInfo = llGetAgentInfo(owner);

        if(ownerInfo & AGENT_WALKING)
            llSetAlpha((float)FALSE, ALL_SIDES);
        else
            llSetAlpha((float)TRUE, ALL_SIDES);
    }
}
```