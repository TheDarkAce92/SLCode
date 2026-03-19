---
name: "Materialization Effects"
category: "example"
type: "example"
language: "LSL"
description: "This script is useful code to implement rezzing events where you want the items rezzed to exhibit science fictiony teleportation or materialization effects. It starts off with alpha (transparency) being set to 0.0 (fully transparent) with glow at 1.00 (full glow), and transitions over 20 steps to zero transparency and 10% glow (you can modify the final glow by setting the glow value inside the \"if\" statement to 0.0, and the stepping value from 0.045 to 0.05, if you want it to have zero final glow)."
wiki_url: "https://wiki.secondlife.com/wiki/Materialization_Effects"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

#### Description

This script is useful code to implement rezzing events where you want the items rezzed to exhibit science fictiony teleportation or materialization effects. It starts off with alpha (transparency) being set to 0.0 (fully transparent) with glow at 1.00 (full glow), and transitions over 20 steps to zero transparency and 10% glow (you can modify the final glow by setting the glow value inside the "if" statement to 0.0, and the stepping value from 0.045 to 0.05, if you want it to have zero final glow).

#### Script

```lsl
// Materialization Script 1.0 by Overbrain Unplugged
// This script is placed under MIT X11 Open Source License
// Copyright (c) 2010 Overbrain Unplugged
//Permission is hereby granted, free of charge, to any person obtaining a copy
//of this software and associated documentation files (the "Software"), to deal
//in the Software without restriction, including without limitation the rights
//to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
//copies of the Software, and to permit persons to whom the Software is
//furnished to do so, subject to the following conditions:
//The above copyright notice and this permission notice shall be included in
//all copies or substantial portions of the Software. The author of this software
//shall be credited by and in any derivative works utilizing this software.

//THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
//IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
//FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
//AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
//LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
//OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
//THE SOFTWARE.

float time = 0.01;

default
{
    state_entry()
    {
        llSetLinkPrimitiveParams(LINK_SET,[PRIM_GLOW,ALL_SIDES,1.0]);
        llSetLinkAlpha(LINK_SET,0.0,ALL_SIDES);
        llSetTimerEvent(time);

    }

    on_rez(integer parameters)
    {
        llSetLinkPrimitiveParams(LINK_SET,[PRIM_GLOW,ALL_SIDES,1.0]);
        llSetLinkAlpha(LINK_SET,0.0,ALL_SIDES);
        llSetTimerEvent(time);

    }


    timer()
    {

        float alpha=llGetAlpha(0);

        list params = llGetPrimitiveParams([PRIM_GLOW,0]);
        float glow = llList2Float(params, 0);
        //This next line you can uncomment to use for testing purposes to view the alpha and glow values during each step.
        //llOwnerSay("Glow = " + (string)glow + "Alpha = " + (string)alpha);
        llSetLinkPrimitiveParams(LINK_SET,[PRIM_GLOW,ALL_SIDES,glow-0.045]);
        llSetLinkAlpha(LINK_SET,alpha + 0.05,ALL_SIDES);
        if (alpha >= 1.0)
        {
           llSetTimerEvent(0.0);
           llSetLinkPrimitiveParams(LINK_SET,[PRIM_GLOW,ALL_SIDES,0.1]);
           llSetLinkAlpha(LINK_SET,1.0,ALL_SIDES);
        }
    }


}
```