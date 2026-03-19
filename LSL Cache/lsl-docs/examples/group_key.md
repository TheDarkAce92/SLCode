---
name: "group key"
category: "example"
type: "example"
language: "LSL"
description: "Place this script in a prim and touch it to find out the set group's key."
wiki_url: "https://wiki.secondlife.com/wiki/Group_key_finder"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

## The Group Key Finder

Place this script in a prim and touch it to find out the set group's key.

```lsl
default
{
    state_entry()
    {
        // white and opaque text
        llSetText("Touch to learn\nGroup Key", <1.0, 1.0, 1.0>, (float)TRUE);
    }

    touch_start(integer num_detected)
    {
        key thisPrim = llGetKey();

        list objectDetails = llGetObjectDetails(thisPrim, [OBJECT_GROUP]);
      key objectGroup = llList2Key(objectDetails, 0);

        string output = "Please set the group for this object in EDIT under the GENERAL tab first.";

        if (objectGroup != NULL_KEY)
            output = "This object's group key is: '" + (string)objectGroup + "'.";

        // PUBLIC_CHANNEL has the integer value 0
        llWhisper(PUBLIC_CHANNEL, output);
    }
}
```