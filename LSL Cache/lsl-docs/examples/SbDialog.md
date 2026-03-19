---
name: "SbDialog"
category: "example"
type: "example"
language: "LSL"
description: "This is a simple replacement function for llDialog. It re-orders the button list so that the button values, as passed to it, display left-to-right, top-to-bottom. It also opens a listen on the specified channel, and returns the handle."
wiki_url: "https://wiki.secondlife.com/wiki/SbDialog"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

This is a simple replacement function for llDialog. It re-orders the button list so that the button values, as passed to it, display left-to-right, top-to-bottom. It also opens a listen on the specified channel, and returns the handle.

```lsl
integer sbDialog(key keyAgent, string strMessage, list lstButtons, integer intChannel) {
    integer intHandle;

    lstButtons =
        llList2List(lstButtons, -3, -1) +
        llList2List(lstButtons, -6, -4) +
        llList2List(lstButtons, -9, -7) +
        llList2List(lstButtons, -12, -10);

    intHandle = llListen(intChannel, "", keyAgent, "");
    llDialog(keyAgent, strMessage, lstButtons, intChannel);
    return intHandle;
}
```