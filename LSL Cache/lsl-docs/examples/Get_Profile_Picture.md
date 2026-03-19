---
name: "Get Profile Picture"
category: "example"
type: "example"
language: "LSL"
description: "Get Profile Picture by Valentine Foxdale"
wiki_url: "https://wiki.secondlife.com/wiki/Get_Profile_Picture"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

Get Profile Picture by Valentine Foxdale

```lsl
// Snippets and HTTPRequest bits were taken from:
//~ RANDOM PROFILE PROJECTOR v5.4.5 by Debbie Trilling ~

// Get Profile Picture by Valentine Foxdale
// optmisation by SignpostMarv Martin
// workaround for WEB-1384 by Viktoria Dovgal:
//  try meta tag instead of img first, try img as backup in case meta breaks
list sides;
list deftextures;

string profile_key_prefix = ",1);
        //Note: Usage of another person's profile picture without their permission may be viewed as copyright infringement.
        GetDefaultTextures();
    }
    touch_start(integer total_number)
    {
        GetProfilePic(llDetectedKey(0));
    }
    http_response(key req,integer stat, list met, string body)
    {
        integer s1 = llSubStringIndex(body, profile_key_prefix);
        integer s1l = profile_key_prefix_length;
        if(s1 == -1)
        { // second try
            s1 = llSubStringIndex(body, profile_img_prefix);
            s1l = profile_img_prefix_length;
        }

        if(s1 == -1)
        { // still no match?
            SetDefaultTextures();
        }
        else
        {
            s1 += s1l;
            key UUID=llGetSubString(body, s1, s1 + 35);
            if (UUID == NULL_KEY) {
                SetDefaultTextures();
            }
            else {
                llSetTexture(UUID,ALL_SIDES);
            }
        }
    }
}
```