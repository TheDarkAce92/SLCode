---
name: "User talk:Rolig Loon/Float Box Contents"
category: "example"
type: "example"
language: "LSL"
description: "LSL example script: User talk:Rolig Loon/Float Box Contents."
wiki_url: "https://wiki.secondlife.com/wiki/User_talk:Rolig_Loon/Float_Box_Contents"
author: ""
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-10"
---

### Features

- Lists all object contents in hover text
- Includes inventory type in the hovertext label
- Shows 8 contents at a time in a vertical marqee-style display that updates every 5 seconds

### Script

```lsl
// FLOAT BOX CONTENTS  -- Rolig Loon -- November 2009
// Lists object contents in dynamic hover text, labelled by type
//
// Free to copy, modify, or distribute.  Please leave these header lines intact
// Please do not sell this script.  Be nice.
//
// Hover text has a 254 character limit, so this script rotates the contents list into hover text eight at a time, marquee style

list contents = [];
default
{
    state_entry()
    {
        // this is a list of all the possible inventory types, as constants.
        list list_types = [INVENTORY_NONE, INVENTORY_TEXTURE, INVENTORY_SOUND, INVENTORY_LANDMARK,
        INVENTORY_CLOTHING, INVENTORY_OBJECT, INVENTORY_NOTECARD, INVENTORY_SCRIPT,
        INVENTORY_BODYPART, INVENTORY_ANIMATION, INVENTORY_GESTURE];

        // this list is of the string names corresponding to the one above.
        list list_names = ["None", "Texture", "Sound", "Landmark", "Clothing", "Object", "Notecard",
        "Script", "Body Part", "Animation", "Gesture"];

        integer all = llGetInventoryNumber(INVENTORY_ALL);
        integer i;
        for (i=0;i<=all-1;++i)
        {
        integer detected_type = llGetInventoryType(llGetInventoryName(INVENTORY_ALL,i)); // look up which type this object is.
        integer type_index = llListFindList(list_types,[detected_type]); // where in list_types is this type?
        string type_name = llList2String(list_names, type_index); // get the corresponding entry in the names list.
        contents += type_name + ": " + llGetInventoryName(INVENTORY_ALL,i) + "\n "; //Display type of content item and its name
        }
        llSetTimerEvent(5);  // Rotate text every 5 seconds
    }

    changed(integer change)
    {
        if (change && CHANGED_INVENTORY)  // If something is added to or removed from box inventory
        {
            llResetScript();
        }
    }

    timer()
    {
        contents = llList2List(contents,1,-1) + llList2String(contents,0); // Move item 0 to the end of the list
        list temp = llList2List(contents,-8,-1); // Display only the last eight items
        llSetText("THIS BOX CONTAINS: \n " + llDumpList2String(temp,""),<1,1,1>,1.0);
    }

}
```