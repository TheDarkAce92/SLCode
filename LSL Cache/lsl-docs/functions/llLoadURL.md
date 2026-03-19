---
name: "llLoadURL"
category: "function"
type: "function"
language: "LSL"
description: 'Shows dialog to avatar offering to load web page at url with message.
If user clicks yes, launches the page in their web browser, starting the browser if required.

The url is truncated to 255 characters and message is truncated to 254 characters.
The protocol for the url must be specified, currentl'
signature: "void llLoadURL(key avatar, string message, string url)"
return_type: "void"
sleep_time: "0.1"
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llLoadURL'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llloadurl"]
---

Shows dialog to avatar offering to load web page at url with message.
If user clicks yes, launches the page in their web browser, starting the browser if required.

The url is truncated to 255 characters and message is truncated to 254 characters.
The protocol for the url must be specified, currently only "https://" and "http://" are supported.
The URL should be RFC-1738 compliant with proper escapes.


## Signature

```lsl
void llLoadURL(key avatar, string message, string url);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `key` | `avatar` | avatar UUID that is in the same region |
| `string` | `message` | message to be displayed in the dialog box |
| `string` | `url` |  |


## Caveats

- Forced delay: **0.1 seconds** — the script sleeps after each call.
- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llLoadURL)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llLoadURL) — scraped 2026-03-18_

Shows dialog to avatar offering to load web page at url with message.If user clicks yes, launches the page in their web browser, starting the browser if required.

## Caveats

- This function causes the script to sleep for 0.1 seconds.
- This function should not be called from group deeded objects, it will silently fail.
- This function silently fails for an avatar that has muted itself.

## Examples

```lsl
default
{
    touch_start(integer num_detected)
    {
        key id = llDetectedKey(0);
        string info = "Visit the Second Life website!";

        // must start with either "http://..." or "https://..."
        string url = "http://www.secondlife.com/";

        integer avatarInSameRegion = (llGetAgentSize(id) != ZERO_VECTOR); // TRUE or FALSE

        if (avatarInSameRegion)
        {
            llLoadURL(id, info, url);
        }
        else
        {
            // if the agent is not in the same region, send a message instead
            // the viewer will turn the URL clickable
            llInstantMessage(id, info + " " + url);
        }
    }
}
```

## See Also

### Articles

- **Limits** — SL limits and constrictions

<!-- /wiki-source -->
