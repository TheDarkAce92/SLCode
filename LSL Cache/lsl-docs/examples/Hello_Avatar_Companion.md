---
name: "Hello Avatar Companion"
category: "example"
type: "example"
language: "LSL"
description: "This script is the unofficial companion to the famous Hello Avatar script from Linden Lab."
wiki_url: "https://wiki.secondlife.com/wiki/Hello_Avatar_Companion"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

/LSL

This script is the unofficial companion to the famous Hello Avatar script from Linden Lab.

```lsl
default
{
    state_entry()
    {
        llListen(0,"","","");
    }
    listen(integer chan, string name, key id, string msg)
    {
        if (msg == "Hello, Avatar!")
        {
        llSay(0, "Hello, " + name + "!");
        }
    }

}
```