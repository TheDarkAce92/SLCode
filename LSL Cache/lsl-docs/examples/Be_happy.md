---
name: "Be happy"
category: "example"
type: "example"
language: "LSL"
description: "Put this script in an attachment to make your avatar smile."
wiki_url: "https://wiki.secondlife.com/wiki/Be_happy"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

Put this script in an attachment to make your avatar smile.

```lsl
//  be happy

default
{
    attach(key attached)
    {
        if (attached)
            llResetScript();
    //  else
    //      has been detached
    }

    state_entry()
    {
        key owner = llGetOwner();

        llRequestPermissions(owner, PERMISSION_TRIGGER_ANIMATION);
    }

    run_time_permissions(integer perm)
    {
        if(perm & PERMISSION_TRIGGER_ANIMATION)
            llSetTimerEvent(5.0);
    }

    timer()
    {
        llStartAnimation("express_toothsmile");
    }
}
```