---
name: "Give InvItem every n hours"
category: "example"
type: "example"
language: "LSL"
description: "This script will give an inventory item on touch only every n hours, even if somebody touches the object more than once."
wiki_url: "https://wiki.secondlife.com/wiki/Give_InvItem_every_n_hours"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

This script will give an inventory item on touch only every n hours, even if somebody touches the object more than once.

```lsl
// Idea and written by Criz Collins
// Don't sell this FREE script!!!

string  giveitem    =   "name of item in objects inventory";
float   giveevery   =   24;  // hours!

/////////////////////////////////////////////

list  visitors;
list lastsent;
integer n;

default
{
    on_rez( integer param )
    {
        llResetScript();
    }

    changed(integer change)
    {
        if (change & CHANGED_INVENTORY)
        {
            llResetScript();
        }
    }

    touch_start(integer total_number)
    {
        for (n=0; n