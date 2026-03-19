---
name: "Profile Picture Retrieval"
category: "tutorials"
type: "reference"
language: "LSL"
description: "Retrieve an avatar profile picture texture UUID via web profile HTML parsing."
wiki_url: "https://wiki.secondlife.com/wiki/Profile_picture_retrieval"
first_fetched: "2026-03-12"
last_updated: "2026-03-12"
---

# Profile Picture Retrieval

LSL does not provide a direct function to fetch an avatar's profile picture texture UUID.
The common approach is to use `llHTTPRequest` to fetch the avatar's web profile HTML and
parse the image UUID from the response.

## Summary

1. Request the web profile page for the avatar UUID.
2. Parse the response body for the profile image UUID.
3. Apply the texture UUID via `llSetTexture` or `llSetLinkTexture`.

## Example (simplified)

```lsl
key req;
key target;

default
{
    state_entry()
    {
        target = llGetOwner();
        req = llHTTPRequest("https://world.secondlife.com/resident/" + (string)target, [], "");
    }

    http_response(key id, integer status, list meta, string body)
    {
        if (id != req || status != 200) return;

        // Find the "imageid" field in the HTML
        integer p = llSubStringIndex(body, "imageid");
        if (p == -1) return;

        string fragment = llGetSubString(body, p, p + 80);
        integer q = llSubStringIndex(fragment, "\"");
        integer r = llSubStringIndex(llGetSubString(fragment, q + 1, -1), "\"");
        if (q == -1 || r == -1) return;

        string img = llGetSubString(fragment, q + 1, q + r);
        if ((key)img)
        {
            llSetTexture(img, ALL_SIDES);
        }
    }
}
```

## Notes

- **This technique may no longer work.** The `world.secondlife.com/resident/` profile pages have changed over time and the `imageid` field may not be present in current HTML. Verify against a live profile page before relying on this approach.
- HTML parsing is inherently fragile — any change to the page markup will silently break the parser and `(key)img` will fail the validity check.
- Consider providing a manual texture UUID override as a fallback.
- There is no officially supported LSL API for retrieving profile picture UUIDs.
