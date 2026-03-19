---
name: "Synchronize"
category: "example"
type: "example"
language: "LSL"
description: "simple synchronize script for two or more separate prims, like wings for instance assuming the task(); is 100% similar in all prims and takes less than 1 sec to implement"
wiki_url: "https://wiki.secondlife.com/wiki/Synchronize"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

simple synchronize script for two or more separate prims, like wings for instance

assuming the task();  is 100% similar in all prims and takes less than 1 sec to implement

```lsl
    float i = llGetTime();
    task();
    float x = llGetTime();
    while (llGetUnixTime()%2 == 0)// do every even second (result 1 for odd seconds)
    {
        llSleep(1-(x-i));// one second minus time that has passed
    }
```