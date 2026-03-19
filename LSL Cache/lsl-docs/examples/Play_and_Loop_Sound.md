---
name: "Play and Loop Sound"
category: "example"
type: "example"
language: "LSL"
description: "This is a very short and simple script. Just put it in an object along with a sound and it will loop the sound over and over again."
wiki_url: "https://wiki.secondlife.com/wiki/Play_and_Loop_Sound"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

## What does this mean?

This is a very short and simple script. Just put it in an object along with a sound and it will loop the sound over and over again.

## Let's see the script then!

Okay, here we go :D.

```lsl
//Bella all the way xD
//

default
{
    state_entry()
    {
        llLoopSound(llGetInventoryName(INVENTORY_SOUND,0), 1.0);
    }
}
```