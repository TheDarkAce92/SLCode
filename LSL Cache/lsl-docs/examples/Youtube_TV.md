---
name: "Youtube TV"
category: "example"
type: "example"
language: "LSL"
description: "Since Youtube changed their format, the TV is not working. I'm working on my new webserver to get it back to work, but it still buggy, mainly in the fact the video url size is too big to be set yet. Use this code as base only."
wiki_url: "https://wiki.secondlife.com/wiki/Youtube_TV"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

## IMPORTANT:

Since Youtube changed their format, the TV is not working.
I'm working on my new webserver to get it back to work, but it still buggy, mainly in the fact the video url size is too big to be set yet.
Use this code as base only.

**This script is not working anymore. Use it only for learning purposes.**

## Code (not working):

**Note: these scripts rely on a private external server, http://secondtools.ismywebsite.com/youtube/getvideotext.php. On 10/15/09, I tried it and that server isn't returning anything meaningful.**
The problem was fixed and some videos are now visible, no update on script needed.

To make a YouTube TV you only need 2 scripts, each one in one prim:

**Get Video.lsl**

```lsl
integer listenid;

default
{
    touch_start(integer i)
    {
        if(llDetectedKey(0) == llGetOwner())
        {
            llOwnerSay("Please type: /65 (Youtube video id) Example: Video URL: http://youtube.com/video?v=blablabla Video ID: blablabla");
            listenid = llListen(65, "", llGetOwner(),"");
        }
    }
    listen(integer c, string n, key k, string m)
    {
        llListenRemove(listenid);
        if(k == llGetOwner())
        {
            llHTTPRequest("http://secondtools.ismywebsite.com/youtube/getvideotext.php?v="+m,[],"");
        }
    }
    http_response(key requestid, integer status, list metadata, string body)
    {
        llOwnerSay("Connecting...");
        llParcelMediaCommandList([PARCEL_MEDIA_COMMAND_URL,body]);
    }
}
```

**Get Texture.lsl**

```lsl
default
{
    state_entry()
    {

    }

    touch_start(integer i)
    {
        if(llDetectedKey(0) == llGetOwner())
        {
            llOwnerSay("Getting Parcel Media Texture...");
            string landTexture;
            landTexture = (string) llParcelMediaQuery([PARCEL_MEDIA_COMMAND_TEXTURE]);
            llSetTexture(landTexture,ALL_SIDES);
        }
    }
}
```

Now is only sit and watch your favorite Youtube videos!