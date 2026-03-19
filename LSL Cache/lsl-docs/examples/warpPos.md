---
name: "warpPos"
category: "example"
type: "example"
language: "LSL"
description: "WarpPos is a method by which the 10m limit on non-physical movement can be avoided, by exploiting a misfeature in llSetPrimitiveParams in which multiple parameters of the same flag type are executed in a single server frame."
wiki_url: "https://wiki.secondlife.com/wiki/WarpPos"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

WarpPos is a method by which the 10m limit on non-physical movement can be avoided, by exploiting a misfeature in llSetPrimitiveParams in which multiple parameters of the same flag type are executed in a single server frame.

**Note that llSetRegionPos now offers similar functionality.**

You should probably use it instead of this workaround.

```lsl
 warpPos( vector destpos )
 {   //R&D by Keknehv Psaltery, 05/25/2006
     //with a little poking by Strife, and a bit more
     //some more munging by Talarus Luan
     //Final cleanup by Keknehv Psaltery
     //Changed jump value to 411 (4096 ceiling) by Jesse Barnett
     // Compute the number of jumps necessary
     integer jumps = (integer)(llVecDist(destpos, llGetPos()) / 10.0) + 1;
     // Try and avoid stack/heap collisions
     if (jumps > 411)
         jumps = 411;
     list rules = [ PRIM_POSITION, destpos ];  //The start for the rules list
     integer count = 1;
     while ( ( count = count << 1 ) < jumps)
         rules = (rules=[]) + rules + rules;   //should tighten memory use.
     llSetPrimitiveParams( rules + llList2List( rules, (count - jumps) << 1, count) );
     if ( llVecDist( llGetPos(), destpos ) > .001 ) //Failsafe
         while ( --jumps )
             llSetPos( destpos );
 }
```

## Quote: warpPos -- llSetPos without the limits ~~ Keknehv Psaltery

A few observations:

Sim crossings are perilous for AVs. Depending on connection speed and whether or not you are connected to the sim (can see it on the mini-map), it may screw up your client. However, it seems like objects, by themselves, can cross great distances. I managed to send an object 4 sims away diagonally. Further testing would help us to understand these things.

...

The average time this function takes to execute is under .2 seconds, which is barely noticeable at all, and can easily be attributed to general lag. A simple optimization for an object with a known destination might be to calculate the list beforehand, and then call llSetPrimitiveParams with that list.

...

a Linden ... response ... go ahead and find a workaround - I'd love to see it, I'm sure it is useful, but it might not work very well across sim borders