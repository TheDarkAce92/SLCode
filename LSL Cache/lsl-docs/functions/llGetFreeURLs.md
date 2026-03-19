---
name: "llGetFreeURLs"
category: "function"
type: "function"
language: "LSL"
description: "Returns an integer that is the number of available URLs. If attached, return the URLs remaining for the owner. Otherwise, return the available URLs for the region."
signature: "integer llGetFreeURLs()"
return_type: "integer"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetFreeURLs'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgetfreeurls"]
---

Returns an integer that is the number of available URLs. If attached, return the URLs remaining for the owner. Otherwise, return the available URLs for the region.


## Signature

```lsl
integer llGetFreeURLs();
```


## Return Value

Returns `integer`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetFreeURLs)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetFreeURLs) — scraped 2026-03-18_

Returns an integer that is the number of available URLs. If attached, return the URLs remaining for the owner. Otherwise, return the available URLs for the region.

## Caveats

- If called from an attachment, there is no way to get the number of free URLs in the region; it will always return the URL count remaining for the agent.

## Examples

This script will say the number of currently available HTTP-In URLs left in the region.

```lsl
default
{
    touch_start(integer num_detected)
    {
        integer numberOfFreeURLs = llGetFreeURLs();

        if (numberOfFreeURLs)
        {
            llSay(0, "There are " + (string)numberOfFreeURLs + " available HTTP-In URLs left in this region.");
        }
        else
        {
            llSay(0, "WARNING: There are no HTTP-In URLs available anymore.");
        }
    }
}
```

```lsl
// WARNING:
//
//      This script is only for proof-of-concept (demo purposes).
//      DO NOT use it if you don't have the sim owners and/or
//      estate managers OK to test this script.
//      This script can possibly block HTTP communication from and to the sim.
//      ...bringing down all networked vendors and/or similar machines.
//
//      This script allocates all available URLs.
//      Deleting the script and/or derezzing the object containing the script,
//      will release all previously taken URLs.

default
{
    state_entry()
    {
        llRequestURL();
    }

    http_request(key request_id, string method, string body)
    {
        if (method == URL_REQUEST_DENIED)
        {
            llSetText("No free URLs!", <1.0, 0.0, 0.0>, 1.0);
        }
        else if (method == URL_REQUEST_GRANTED)
        {
            llSetText((string)llGetFreeURLs() + " URLs left\n" + body, <1.0, 1.0, 1.0>, 1.0);
            llRequestURL();
        }
        else if (method == "GET")
        {
            llHTTPResponse(id, 200, "Hello there!");
        }
    }
}
```

## Notes

URLs are a finite region resource and should be released when no longer needed.

## See Also

### Functions

- llRequestURL
- llRequestSecureURL
- llReleaseURL
- llHTTPResponse
- llGetHTTPHeader

### Articles

- LSL http server

<!-- /wiki-source -->
