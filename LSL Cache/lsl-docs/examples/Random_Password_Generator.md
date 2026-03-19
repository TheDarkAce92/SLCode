---
name: "Random Password Generator"
category: "example"
type: "example"
language: "LSL"
description: "string randomPassword(integer length) { string CharSet = \"abcdefghijkmnpqrstuvwxyz23456789\"; // omitting confusable characters string password; integer CharSetLen = llStringLength(CharSet); // Note..."
wiki_url: "https://wiki.secondlife.com/wiki/Random_Password_Generator"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

Code:

```lsl
// Generate Passwords based on String length
// Free to use, share and remix.

string randomPassword(integer length)
{
    string CharSet = "abcdefghijkmnpqrstuvwxyz23456789";    // omitting confusable characters
    string password;
    integer CharSetLen = llStringLength(CharSet);
    // Note: We do NOT add 1 to the length, because the range we want from llFrand() is 0 to length-1 inclusive

    while (length--)
    {
        integer rand = (integer) llFrand(CharSetLen);
        password += llGetSubString(CharSet, rand, rand);
    }
    return password;
}

default
{
    touch_start(integer num)
    {
        llSay(0, randomPassword(10));
    }
}
```