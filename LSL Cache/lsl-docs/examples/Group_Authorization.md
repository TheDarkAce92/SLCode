---
name: "Group Authorization"
category: "example"
type: "example"
language: "LSL"
description: "This script is used to check whether the object is set to the appropriate group (by group key)."
wiki_url: "https://wiki.secondlife.com/wiki/Group_Authorization"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

## Group Authorization

This script is used to check whether the object is set to the appropriate group (by group key).



## The Script

```lsl
//  © 2009 Chase Quinnell and TerraCo Designs
//  http://www.terracodesigns.com
//  Please keep this open source and leave my name reference here

//  This is the group key for the authorized group.
string authgroupkey = "INSERT YOUR GROUP KEY HERE";

Unauthorized()
{
    string thisScript = llGetScriptName();

    llOwnerSay("/me [" + thisScript + "]: Sorry, you're wearing the wrong group tag.");
    llDetachFromAvatar();
    llRemoveInventory(thisScript);
    llDie();
}

default
{
    on_rez(integer start_param)
    {
        llResetScript();
    }

    state_entry()
    {
        key ownerKey = llGetOwner();
        llRequestPermissions(ownerKey, PERMISSION_ATTACH);

        key thisPrimsKey = llGetKey();
        string groupKey = llList2String(llGetObjectDetails(thisPrimsKey, [OBJECT_GROUP]), 0);

        if (groupKey != authgroupkey)
            Unauthorized();
        else
            llOwnerSay("Authorization passed");
    }

    run_time_permissions(integer perm)
    {
        if (!(perm & PERMISSION_ATTACH))
            llResetScript();
    }
}
```