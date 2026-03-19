---
name: "PosJump"
category: "example"
type: "example"
language: "LSL"
description: "Here's an interesting method for bypassing the 10m limitation in Non-Physical movement. Be aware that IT WILL NOT WORK FOREVER, there are plans to fix this bug - for long-term use, rely on warpPos. Alternatives that offer the same functionality are being considered. Until there's an alternative, this bug may be allowed to persist. More information here."
wiki_url: "https://wiki.secondlife.com/wiki/PosJump"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

Here's an interesting method for bypassing the 10m limitation in Non-Physical movement. **Be aware that IT WILL NOT WORK FOREVER, there are plans to fix this bug - for long-term use, rely on warpPos.**  Alternatives that offer the same functionality are being considered.  Until there's an alternative, this bug *may* be allowed to persist.  More information [here.](http://jira.secondlife.com/browse/SVC-4089)

**A replacement function llSetRegionPos() has been released and is now live grid-wide.**

**As of August 13th, 2012 there are already reported breakages of this function on some Channels.**

```lsl
posJump(vector target_pos)
{
// An alternative to the warpPos trick without all the overhead.
// Trickery discovered by Uchi Desmoulins and Gonta Maltz.  More exact value provided by Fake Fitzgerald.
	llSetLinkPrimitiveParamsFast(!!llGetLinkNumber(), [PRIM_POSITION, <1.304382E+19, 1.304382E+19, 0.0>, PRIM_POSITION, target_pos]);
}
//the !!llGetLinkNumber() thing is a little trick to always point to the root regardless of where the script is or whether the linkset got only one or more prims.
// If you are using a single prim object, you can substitute 0 or LINK_THIS. If it is a multiple prim object, you can substitute LINK_ROOT.
```



If the target position turns out to be no-entry, your object will go offworld.  So Alias Turbo included a step that sends the object back to its starting position (just in case!) before trying the target position again.  So in the case that the target position is no-entry, it will either move 10m at most, or not at all.

```lsl
safe_posJump(vector target_pos)
{
// An alternative to the warpPos trick without all the overhead.
// Trickery discovered by Uchi Desmoulins and Gonta Maltz.  More exact value provided by Fake Fitzgerald.  Safe movement modification provided by Alias Turbo.
      vector start_pos = llGetPos();
	llSetLinkPrimitiveParamsFast(!!llGetLinkNumber(), [PRIM_POSITION, <1.304382E+19, 1.304382E+19, 0.0>, PRIM_POSITION, target_pos, PRIM_POSITION, start_pos, PRIM_POSITION, target_pos]);
}
//the !!llGetLinkNumber() thing is a little trick to always point to the root regardless of where the script is or whether the linkset got only one or more prims.
// If you are using a single prim object, you can substitute 0 or LINK_THIS. If it is a multiple prim object, you can substitute LINK_ROOT.
```