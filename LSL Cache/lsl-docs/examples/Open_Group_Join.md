---
name: "Open Group Join"
category: "example"
type: "example"
language: "LSL"
description: "No bot needed for this script."
wiki_url: "https://wiki.secondlife.com/wiki/Open_Group_Join"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

## User Touches Object to Join Group

No bot needed for this script.

User Touches object for a link in Local Chat that when clicked from History will open the Group Information Window. If Group is set to Open Enrollment the user may JOIN.

The object this script is in must be set to the group you want people to join.

```lsl
findgroupkey()
{
    list TempList = llGetObjectDetails(llGetKey(), [OBJECT_GROUP]);
    key groupkey = llList2Key(TempList, 0);
    if (groupkey == NULL_KEY)
    {
        llWhisper(0, "Set the Group for this object in EDIT under the GENERAL tab and be sure your Group is Open Enrollment.");
    }
    else
    {
        llWhisper(0, "Click the link from Chat History (Ctrl+H) and then click on JOIN button! secondlife:///app/group/" + (string) groupkey + "/about");
    }
}

default
{
    state_entry()
    {
        llSetText("Touch to Join\nour Group", <1, 1, 1>, 1.0); // white and opaque floating text, optional
        findgroupkey();
    }

    touch_start(integer total_number)
    {
        findgroupkey();
    }
}
```

If the object Group must be different because of land settings use this object somewhere where you are allowed and Copy the message said from Chat History. Then create a simple script that whispers this message when Touched.



More scripts: [http://www.aliciastella.com](http://www.aliciastella.com)