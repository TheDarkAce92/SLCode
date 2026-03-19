---
name: "Object Size"
category: "example"
type: "example"
language: "LSL"
description: "Reports the dimensions and footprint of a linkset."
wiki_url: "https://wiki.secondlife.com/wiki/Object_Size"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

## Object Size

Reports the dimensions and footprint of a linkset.

```lsl
default
{
    state_entry()
    {
        float temp;

        list box = llGetBoundingBox(llGetKey());
        vector size = llList2Vector(box, 1) * llGetRot() - llList2Vector(box, 0) * llGetRot();

        if (llAbs(llRound(size.x)) < llAbs(llRound(size.y))) {
            float temp = size.y;
            size.y = size.x;
            size.x = temp;
        }
        llOwnerSay("Your object is roughly " + (string)llAbs(llRound(size.x)) + "m long by " + (string)llAbs(llRound(size.y)) + "m wide by " + (string)llAbs(llRound(size.z)) + "m tall.");
        llOwnerSay("With an area of " + (string)llAbs(llRound(size.x*size.y)));
        llRemoveInventory(llGetScriptName());
    }
}
```