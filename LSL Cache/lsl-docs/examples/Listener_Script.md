---
name: "Listener Script"
category: "example"
type: "example"
language: "LSL"
description: "Put this in an object to listen to what people near the box are saying (like spying!) I am not responsible for people cheating on their partners, plots to kill people, etc."
wiki_url: "https://wiki.secondlife.com/wiki/Listener_Script"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

## Listener Script


      ⚠️
      **Warning:** Use of this script without consent from those you listen to could constitute a breach of your agreement with Linden Labs (via the [Terms of Service](http://secondlife.com/corporate/tos.php)) to abide by the [Community Standards](http://secondlife.com/corporate/cs.php) of Second Life.


Put this in an object to listen to what people near the box are saying (like spying!) I am not responsible for people cheating on their partners, plots to kill people, etc.

```lsl
default
{
    state_entry()
    {
        llListen(0, "", NULL_KEY, "");
    }

    listen(integer channel, string name, key id, string message)
    {
        llInstantMessage(llGetOwner(), name + " said: '" + message + "'");
    }
}
```