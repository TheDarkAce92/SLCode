---
name: "Drink script"
category: "example"
type: "example"
language: "LSL"
description: "A drink script, used in many parts of Second Life. Whether it's for food or drink, or roleplay potions and what-not, a drink script is always included. If it's not, it's rubbish."
wiki_url: "https://wiki.secondlife.com/wiki/Drink_script"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

### A what?

A drink script, used in many parts of Second Life. Whether it's for food or drink, or roleplay potions and what-not, a drink script is *always* included. If it's not, it's rubbish.

### Okay, okay, let's get this script, then

```lsl
//Emmas Seetan

string animationToBePlayed = "drinking animation";
integer flag;

default
{
    on_rez(integer start_param)
    {
        llResetScript();
    }

    attach(key id)
    {
    //  when being detached
        if(id == NULL_KEY)
        {
            integer currentPerms = llGetPermissions();

            if (currentPerms & PERMISSION_TRIGGER_ANIMATION)
                llStopAnimation(animationToBePlayed);
        }
    }

    changed(integer change)
    {
        if (change & (CHANGED_OWNER | CHANGED_INVENTORY))
        {
        //  stop animation for old owner
            integer currentPerms = llGetPermissions();

            if (currentPerms & PERMISSION_TRIGGER_ANIMATION)
                llStopAnimation(animationToBePlayed);

        //  reset script to get new owner
            llResetScript();
        }
    }

    state_entry()
    {
        key owner = llGetOwner();
        llRequestPermissions(owner, PERMISSION_TRIGGER_ANIMATION);
    }

    run_time_permissions(integer perm)
    {
        if(perm & PERMISSION_TRIGGER_ANIMATION)
        {
            llStartAnimation(animationToBePlayed);

            llSetTimerEvent(15.0);
        }
    }

    timer()
    {
        if(flag & 1)
            llStartAnimation(animationToBePlayed);

        flag = (flag + 1) % 4;
    }
}
```