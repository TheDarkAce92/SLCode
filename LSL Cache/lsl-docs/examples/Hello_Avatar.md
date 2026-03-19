---
name: "Hello Avatar"
category: "example"
type: "example"
language: "LSL"
description: "The following script contains the default code that is placed in every new script. It says \"Hello, Avatar\" when it is saved or reset and says \"Touched.\" when it is touched. That makes it the LSL representation of the famous Hello world program."
wiki_url: "https://wiki.secondlife.com/wiki/Hello_Avatar"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

/LSL

The following script contains the default code that is placed in every new script. It says "*Hello, Avatar*" when it is saved or reset and says "*Touched.*" when it is touched. That makes it the LSL representation of the famous [Hello world program](http://en.wikipedia.org/wiki/Hello_world_program).

```lsl
default
{
    state_entry()
    {
        llSay(0, "Hello, Avatar!");
    }

    touch_start(integer total_number)
    {
        llSay(0, "Touched.");
    }
}
```

Notes:

- Scripters should learn to call the simpler llOwnerSay rather than llSay, in order to avoid making objects that spam the neighborhood via PUBLIC_CHANNEL zero.

- Scripters should learn to call llInstantMessage rather than llSay, in order to stop losing chat while far away or logged off.