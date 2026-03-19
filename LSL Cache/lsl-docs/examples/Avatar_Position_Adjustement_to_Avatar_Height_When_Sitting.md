---
name: "Avatar Position Adjustement to Avatar Height When Sitting"
category: "example"
type: "example"
language: "LSL"
description: "This is a piece of code, that is meant to be putted inside a changed event (what is initialized when avatar sits). This snippet is for a prim that is AT THE FLOOR LEVEL mainly for standing and walking animations. If you need a snippet for a chair, just use zero."
wiki_url: "https://wiki.secondlife.com/wiki/Avatar_Position_Adjustement_to_Avatar_Height_When_Sitting"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

### Animation Adjustement According to Avatar Height Snippet

This is a piece of code, that is meant to be putted inside a changed event (what is initialized when avatar sits).


This snippet is for a prim that is AT THE FLOOR LEVEL mainly for standing and walking animations. If you need a snippet for a chair, just use zero.




```lsl
integer agentlinknum = llGetNumberOfPrims(); // when avatar sits it becomes the last child on the linkset

  vector size = llGetAgentSize(llAvatarOnSitTarget()); // we measure the avatar size


    float adjustement = (size.z / 2 );  // size.z is avatar height, pelvis is halfway the avatar



     float avup = (adjustement + ( size.z/10)) + 0.08; // half of avatar + one tenth of avatar + your own tweak (depends on various things, so you have to test what works for you)

llSetLinkPrimitiveParamsFast(agentlinknum,[PRIM_POS_LOCAL,<0,0,avup>,PRIM_ROT_LOCAL,llEuler2Rot(<0,0,0>)]); // here we move the avatar to the new position, the rotation part is the target rotation in euler
```