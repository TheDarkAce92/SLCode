---
name: "LibraryDisplayLandScreenshot"
category: "example"
type: "example"
language: "LSL"
description: "This is nothing special, but it gets the job done. :) --Jon Desmoulins 17:49, 16 February 2010 (UTC)"
wiki_url: "https://wiki.secondlife.com/wiki/LibraryDisplayLandScreenshot"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

This is nothing special, but it gets the job done. :)
--Jon Desmoulins 17:49, 16 February 2010 (UTC)

NOTE: Your location has to be in the search for this to work. (this limitation appears to have been removed.)  Also, it may take some time for your location to appear in search if you just checked the "Show in Search" button in your land settings.  (I forget the cache time) (this limitation appears to have been removed, but there can still be delays for pages to update.)

Edits:

- 2/19/2010 - Erased my own land's key from the code, forgot to omit this on submission.
- 10/4/2010 (Cerise) - whacked a typo and shuffled some deck chairs

```lsl
// Credit goes to Jana Kamachi/Solar Alter
// for discovering this concept first
// and taking it beyond just displaying the profile picture
// see http://forums.secondlife.com/showthread.php?t=225460
// and https://wiki.secondlife.com/wiki/User:Jana_Kamachi/Profile
// for further information

/*
    Modified by Jon Desmoulins to use the new PARCEL_DETAILS_ID
    to fetch the image that displays on the world.secondlife.com pages
    It's a little hacky, but it works.
*/

string gLandUrl = "http://world.secondlife.com/place/";  //Base URL for world search
string gMetaTag = "