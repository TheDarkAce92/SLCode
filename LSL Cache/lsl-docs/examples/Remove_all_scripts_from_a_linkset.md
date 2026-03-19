---
name: "Remove all scripts from a linkset"
category: "example"
type: "example"
language: "LSL"
description: "This simple script removes all scripts contained in a linkset. I had found one on the Internet but for an unknown reason, it moves the linkset (see this thread on the forums) ?! This one is simple and works for attachments and rezzed objects. Just drop the script in the linkset (i.e., into the root prim). If the linkset is one single prim, there is nothing else to do. Otherwise, when the script tells you that it is ready, unrez/re-rez the object and set all scripts to running using the menu of the viewer. That's all. An hovertext shows the number of remaining prims to be cleaned up. This script is very useful for example for Firestorm users: indeed, at the time of writing this down[1], the feature is still missing in Firestorm."
wiki_url: "https://wiki.secondlife.com/wiki/Remove_all_scripts_from_a_linkset"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

This simple script removes all scripts contained in a linkset. I had found one on the Internet but for an unknown reason, it moves the linkset (see [this thread on the forums](https://community.secondlife.com/forums/topic/32874-script-remover-for-linksets/)) ?! This one is simple and works for attachments and rezzed objects. Just drop the script in the linkset (i.e., into the root prim). If the linkset is one single prim, there is nothing else to do. Otherwise, when the script tells you that it is ready, unrez/re-rez the object and set all scripts to running using the menu of the viewer. That's all. An hovertext shows the number of remaining prims to be cleaned up. This script is very useful for example for Firestorm users: indeed, at the time of writing this down, the feature is still missing in Firestorm.

```lsl
//  Script eraser by Dahlia Orfan (2012)
//  Drop this script in a linkset (rezzed on the ground or attachment)
//  When the script tells that it is ready, unrez and rerez the linkset
//  Set all scripts to running using the menu of the viewer
//  Wait until it is done.   http://pastebin.com/gqi7mKFE

integer prims;
integer DELETE;

//  remove all other scripts, then this one
remove_scripts()
{
    string thisScript = llGetScriptName();

    integer index = llGetInventoryNumber(INVENTORY_SCRIPT);
    string scriptName;

    //  start with last script which has the index (numberOfScripts - 1)
    do
    {
        --index;
        scriptName = llGetInventoryName(INVENTORY_SCRIPT, index);

        if (scriptName != thisScript)
            llRemoveInventory(scriptName);
    }
    while (index);

    //  at last remove this script
    llRemoveInventory(thisScript);
}

default
{
    state_entry()
    {
        //  set an ident number code
        DELETE = (integer) ("0x" + (string) llGetOwner() );
        integer link = llGetLinkNumber();

        //  the root prim has link number 0 for single prim objects and 1 for linksets
        if (link < 2)
        {
            prims = llGetObjectPrimCount(llGetKey() );        // Get number of prims excluding seated avatars

            //  if single prim, else linkset
            if (prims == 1)
            {
                llSay(0, "Done removing scripts.");
                remove_scripts();
            }
            else
            {
                integer n = prims;
                while(n > 1)
                {
                    llGiveInventory(llGetLinkKey(n), llGetScriptName());
                    --n;
                }
                llSay(0, "Please take this object back to your inventory and "
                    + "rez it again. Then edit the object (ctrl+3), go to the menu at the "
                    + "top of your viewer and select BUILD > SCRIPTS > SET SCRIPTS TO RUNNING.");
            }
        }
        else//  not the root prim
        {
            llMessageLinked(LINK_ROOT, DELETE, "", NULL_KEY);
            remove_scripts();
        }
    }

    link_message(integer sender_num, integer num, string str, key id)
    {
        //  if the received linkmessage contains the ident number code previously stored...
        if (num == DELETE)
        {
            --prims;
            if (prims == 1)
            {
                llSay(0, "Done removing scripts.");
                remove_scripts();
            }
        }
    }
}
```

### Notes

1. ↑ February 2012