---
name: "Textbox2Hovertext"
category: "example"
type: "example"
language: "LSL"
description: "integer listenhandle;"
wiki_url: "https://wiki.secondlife.com/wiki/Textbox2Hovertext"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

```lsl
// Textbox2Hovertext by Ackley Bing & Omei Qunhua
// A simple script to allow object owners to change the "hovertext"
// on their prims using a text entry box (llTextBox).

integer listenhandle;

default
{
    touch_start(integer num)
    {
        key Writer = llDetectedKey(0);
        if(Writer!=llGetOwner()) return; // remove this line to allow anyone to change the hover text
        llListenRemove(listenhandle);
        llSetTimerEvent(60.0); // Time to input text until script closes listener in case target doesnt enter anything into textbox
        listenhandle=llListen(-12345, "", Writer, "");
        llTextBox( Writer, "Set Hovertext", -12345);
    }
    listen(integer channel, string name, key id, string message)
    {
        llSetText(message, <1, 1, 1>, 1);
        llListenRemove(listenhandle);
        llSetTimerEvent(0.0);
    }
    timer()
    {
        llListenRemove(listenhandle);
        llSetTimerEvent(0.0);
    }
}
```