---
name: "Key2Name"
category: "example"
type: "example"
language: "LSL"
description: "The web service this script utilized is no longer available. The URL has been removed as the domain is now being used as a phishing site. This article exists for historical interest."
wiki_url: "https://wiki.secondlife.com/wiki/Key2Name"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

**Dead Service Warning!**

The web service this script utilized is no longer available. The URL has been removed as the domain is now being used as a phishing site. This article exists for historical interest.

## llName2Key Script

```lsl
string black_db_key2name_service = "";
key QID;

string Name;
key UUID;

llGetKey2Name(key UUID)
{
    QID = llHTTPRequest(black_db_key2name_service+llEscapeURL((string)UUID), [], "");
}

default
{
    state_entry()
    {
        llListen(PUBLIC_CHANNEL, "", llGetOwner(), "");
    }
    listen(integer channel, string name, key id, string str)
    {
        UUID = id;
        llGetKey2Name(UUID);
    }
    http_response(key req, integer status, list meta, string body)
    {
        if(req == QID && status == 200)
        {
            Name = llStringTrim(body, STRING_TRIM);
            if(!llStringLength(Name))// if the length is zero
            {
                //None found
            }
            else
            {
                llOwnerSay((string)UUID + "'s name = "+Name);
            }
        }
    }
}
```

## See Also

- Avatar/Name - Name related functions.
- Who