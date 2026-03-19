---
name: "No Limit Teleporter"
category: "example"
type: "example"
language: "LSL"
description: "Zero - Lag You can do anything, change the code and all more... To use: [+] Set stapos (end of script) to the object position (where to back when the destination is reach). [+] Set dest (end of script) to the object destination."
wiki_url: "https://wiki.secondlife.com/wiki/No_Limit_Teleporter"
author: "BETLOG Hax"
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

Simple Teleporter - No Limitation

Zero - LagYou can do anything, change the code and all more... To use: [+] Set stapos (end of script) to the object position (where to back when the destination is reach). [+] Set dest (end of script) to the object destination. ```lsl //Leave that here //Script created by Morgam Biedermann vector posnow; vector stapos; rotation rotnow; teleport(vector dest) { if(llGetPos() != dest) { llSetPos(dest); teleport(dest); } else { llUnSit(llAvatarOnSitTarget()); teleports(stapos); } } teleports(vector dest) { if(llGetPos() != stapos) { llSetPos(stapos); teleports(stapos); } } default { state_entry() { stapos = ; } touch_start(integer vez) { if(llDetectedKey(0) == llGetOwner()) teleport(); } } ``` ## Critique to the above script by BETLOG Hax The above example is a really bad approach to use for many reasons. Not least of which is that lag is precisely what it will generate. An equivalency check that respects SL's somewhat wiggly precision system, and isn't trying to match a movement to EXACTLY 6 decimal places of precision is needed.```lsl if(llGetPos() != dest) //is bad ``` ```lsl if(llVecDist(llGetPos(),dest)ie: ```lsl teleports(vector dest) { // if(llGetPos() != stapos) // This an inherently bad approach; given 6 decimal places on 3 floats in a vector its // very UNlikely the equivalency will be precisely equal even if its VERY close, this // will become especially evident at high altitude. It'll look like its stopped, // but the llSetPos() will be still thrashing away. Possibly for quite some time/forever. // // the below will stop in a timely manner. if(llVecDist(llGetPos(),dest) And a system that has a user function call itself from within itself is probably not good. This is MUCH better: [**MUST** be compiled in MONO]

```lsl
teleports(vector dest)
{   list l=[PRIM_POSITION,dest];
    l+=l;l+=l;l+=l;l+=l;l+=l;l+=l;l+=l;l+=l;l+=l;
    llSetPrimitiveParams(l);
}
```