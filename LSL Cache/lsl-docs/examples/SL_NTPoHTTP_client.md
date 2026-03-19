---
name: "SL NTPoHTTP client"
category: "example"
type: "example"
language: "LSL"
description: "LSL example: SL NTPoHTTP client."
wiki_url: "https://wiki.secondlife.com/wiki/SL_NTPoHTTP_v1.1_client"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

```lsl
key http_id;
string timezone = "America/Los_Angeles"; // See http://uk.php.net/manual/en/timezones.php
                                         // for full list of supported timezones.
string format = "llGetWallClock"; // "llGetWallClock", "RFC 2822" and "ISO 8601"
                                  // are the supported formats.
default
{
    state_entry()
    {
        http_id = llHTTPRequest("http://services.slopenid.net/SLNTPoHTTP/" + llEscapeURL(format) + "/"
+ (string)llGetUnixTime() + "/" + timezone + "/",[],"");
    }
    http_response(key q,integer s,list m,string r)
    {
        if(q == http_id)
        {
            llOwnerSay(r);
        }
    }
}
```