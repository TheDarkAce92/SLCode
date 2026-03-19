---
name: "No Auto-Return"
category: "example"
type: "example"
language: "LSL"
description: "Isn't it annoying when you're at a sandbox and you haven't linked a build and you get frustrated because it gets returned and you can't work out where that bit goes again? Well, with this script it stops the objects from getting returned!"
wiki_url: "https://wiki.secondlife.com/wiki/No_Auto-Return"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

## What is No Auto-Return?

Isn't it annoying when you're at a sandbox and you haven't linked a build and you get frustrated because it gets returned and you can't work out where that bit goes again? Well, with this script it stops the objects from getting returned!

My cube has been here for 4 hours!

Note: Only use for long builds that will take a long time; NOTHING ELSE!



      **Note:** Test this with some unimportant build first. I believe this autoreturn hack was nerfed in the last year. --ObviousAltIsObvious Resident (talk) 23:20, 24 January 2015 (PST)


## Example script



      **Important:** Do take note that this script is meant for single-prim-objects, **NOT** linksets!


```lsl
key owner;

default
{
    on_rez(integer param)
    {
        key ownerRightNow = llGetOwner();

        if (owner == ownerRightNow)
            llRequestPermissions(owner, PERMISSION_CHANGE_LINKS);
        else
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

        llRequestPermissions(owner, PERMISSION_CHANGE_LINKS);

        llListen(10240, "", NULL_KEY, "");
    }

    listen(integer channel, string name, key id, string message)
    {
        llDie();
    }

    run_time_permissions(integer perm)
    {
        if(perm & PERMISSION_CHANGE_LINKS)
            llSetTimerEvent(30.0);
    }

    timer()
    {
        key keyThisPrim = llGetKey();
        integer link = llGetLinkNumber();

        llBreakLink(link);

    //  wait a bit to make sure this works
        llSleep(5.0);

        llCreateLink(keyThisPrim, FALSE);
    }
}
```