---
name: "Sound Preloader"
category: "example"
type: "example"
language: "LSL"
description: "This creates a tripwire that will cause the target avatar to preload sound files when they pass through the containing prim, due the one second script delay for each sound file, think carefully about the number of sound files per preloader and their position in relation to where the sounds are actually played."
wiki_url: "https://wiki.secondlife.com/wiki/Sound_Preloader"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

This creates a tripwire that will cause the target avatar to preload sound files when they pass through the containing prim, due the one second script delay for each sound file, think carefully about the number of sound files per preloader and their position in relation to where the sounds are actually played.

This is intended for use when sounds need to be played at a specific point in your users experience.

Example use : User enters a doorway into an empty room, 'Surprise!' sound is played as part of a separate script that fills the room with balloons. The 'Surprise!' sound and this script was placed at the start of the corridor leading into this room.

This is not suitable or necessary for repeating ambient effects or sound events that are not strictly tied to events or locations.

**This script does not play any sound.**

- Rez a prim and add the following script.
- Name the prim something meaningful.
- Add a number of sound files from inventory.
- Place prim where avatars will walk through it at least 1 second per file ahead of where the sounds will trigger.
- Set the prim to 100% alpha.

1kb script memory can be saved by removing the changed event and manually resetting the script when files are added, however if you are hitting memory issues due to the number of files in a single preloader it would be better to split the load between multiple preloaders staggered around your build.

Think carefully about positioning and walk your build.

"It takes 10 seconds to walk from here to the surprise sound effect, if I place the tripwire here I can request at most 10 sounds be preloaded, but realistically and factoring time to download, 5 is probably the max....."

Don't just place one of these at the landing point and put every sound file you use in your entire build inside it, it won't provide any benefit.



```lsl
// Sound Preloader Script
// Copyright (C) 2014 Trinity Dejavu (Catznip Viewer http://catznip.com)
// Released under the MIT Licence (http://opensource.org/licenses/MIT)

// Documentation
// https://wiki.secondlife.com/wiki/Sound_Preloader
// http://catznip.com/index.php/Sound_Preloader_(LSL)

integer SOUNDS_COUNT;
list    SOUNDS;

default
{
    state_entry()
    {
        // Setup the containing prim so people can walk through it
        // and trigger the required collision events.
        llSetLinkPrimitiveParamsFast(LINK_SET,[PRIM_PHANTOM,FALSE]);
        llVolumeDetect(TRUE);

        // Index the sounds contained
        integer x;
        SOUNDS_COUNT= llGetInventoryNumber(INVENTORY_SOUND);
        for (x=0;x