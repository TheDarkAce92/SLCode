---
name: "Color Changer Plus"
category: "example"
type: "example"
language: "LSL"
description: "// you might want to change this integer listenChannel = 5;"
wiki_url: "https://wiki.secondlife.com/wiki/Color_Changer"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

```lsl
//  Color Changer Plus v1.0
//  by Neo Calcutt
//
//  distributed under the Creative Commons Attribution-Share Alike 3.0 United States License.
//
//  please leave the script full permissions and keep this header intact

//  you might want to change this
integer listenChannel = 5;

default
{
    state_entry()
    {
        llListen(listenChannel, "", NULL_KEY, "");
    }

    listen(integer channel, string name,  key id, string message)
    {
    //  uncomment the next line to only listen to the owner
    //  if (id != llGetOwner()) return;

    //  uncomment the next line to only listen to the owner and other objects by the owner
    //  if (llGetOwnerKey(id) != llGetOwner()) return;

    //  this would be black
        vector color = ZERO_VECTOR;

        if (message == "navy")         color = <0.000, 0.122, 0.247>;
        else if (message == "blue")    color = <0.000, 0.455, 0.851>;
        else if (message == "aqua")    color = <0.498, 0.859, 1.000>;
        else if (message == "teal")    color = <0.224, 0.800, 0.800>;
        else if (message == "olive")   color = <0.239, 0.600, 0.439>;
        else if (message == "green")   color = <0.180, 0.800, 0.251>;
        else if (message == "lime")    color = <0.004, 1.000, 0.439>;
        else if (message == "yellow")  color = <1.000, 0.863, 0.000>;
        else if (message == "orange")  color = <1.000, 0.522, 0.106>;
        else if (message == "red")     color = <1.000, 0.255, 0.212>;
        else if (message == "maroon")  color = <0.522, 0.078, 0.294>;
        else if (message == "fuchsia") color = <0.941, 0.071, 0.745>;
        else if (message == "purple")  color = <0.694, 0.051, 0.788>;
        else if (message == "white")   color = <1.000, 1.000, 1.000>;
        else if (message == "silver")  color = <0.867, 0.867, 0.867>;
        else if (message == "gray")    color = <0.667, 0.667, 0.667>;
        else if (message == "random")
        {
            float r = llFrand(1.0);
            float g = llFrand(1.0);
            float b = llFrand(1.0);
            color = ;
        }
        else if (llSubStringIndex(message, "<") == 0)
            color = (vector)message;

        llSetColor(color, ALL_SIDES);
    }
}
```