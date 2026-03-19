---
name: "Profile Picture"
category: "example"
type: "example"
language: "LSL"
description: "Use this script to get user's profile picture UUID and display it in-world."
wiki_url: "https://wiki.secondlife.com/wiki/Profile_Picture"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

Use this script to get user's profile picture UUID and display it in-world.

### Usage

Create a box, add the code and click.

- Note that the string uuid is set on touch.

```lsl
key DefaultTexture = "9d45f95d-5bb5-0f01-7b3c-29c5297ce67e";
string URL_RESIDENT = "https://world.secondlife.com/resident/";
string uuid;

string meta_find = "