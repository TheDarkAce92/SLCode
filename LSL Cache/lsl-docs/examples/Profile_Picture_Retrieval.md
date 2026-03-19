---
name: "Profile Picture Retrieval"
category: "example"
type: "example"
language: "LSL"
description: "LSL example: Profile Picture Retrieval."
wiki_url: "https://wiki.secondlife.com/wiki/Profile_Picture_Retrieval"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

/LSL

## Profile Picture Retrieval by Pazako Karu UPDATED 9/5/18

```lsl
//Released as Public Domain
//Pazako Karu 9/5/18
key ppReqID;
key ProfilePic;
getProfilePic(key AvatarKey)
{
    ppReqID = llHTTPRequest( "http://world.secondlife.com/resident/" + (string)AvatarKey,[HTTP_METHOD,"GET"],"");
}
setProfilePic(key Texture)
{
    if (Texture != NULL_KEY)
    {
        llSetTexture(Texture,ALL_SIDES);
    }
    else llOwnerSay("Invalid texture returned!");
}
default
{
    state_entry()
    {
        getProfilePic(llGetOwner());
    }
    http_response(key req,integer stat, list meta, string body)
    {
        if (req == ppReqID)
        {
            integer s1  = llSubStringIndex(body,"