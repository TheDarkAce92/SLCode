---
name: "llSetContentType"
category: "function"
type: "function"
language: "LSL"
description: "Sets the Internet media type 'Content-Type' header of any subsequent LSL HTTP server response via llHTTPResponse."
signature: "void llSetContentType(key request_id, integer content_type)"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llSetContentType'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llsetcontenttype"]
---

Sets the Internet media type "Content-Type" header of any subsequent LSL HTTP server response via llHTTPResponse.


## Signature

```lsl
void llSetContentType(key request_id, integer content_type);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `key (handle)` | `request_id` | a valid http_request() key |
| `integer` | `content_type` | Media type to use with any following llHTTPResponse(request_id, ...) |


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llSetContentType)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llSetContentType) — scraped 2026-03-18_

Sets the  Internet media type "Content-Type" header of any subsequent LSL HTTP server response via llHTTPResponse.

## Caveats

- When using CONTENT_TYPE_HTML, this setting will be ignored unless all of these conditions are met:

  1. the web browser is the Second Life client
  1. the user (logged into the SL client viewing the page) is the owner of the object.
  1. the user (logged into the SL client viewing the page) is connected to the region the object is located in

Obviously this is not compatible with group owned objects. One way around this limitation would be to temporarily attach a repeater.

## Examples

```lsl
key url_request;

string HTML_BODY =
"

My First Heading

My first paragraph.

";

default
{
    state_entry()
    {
        url_request = llRequestURL();
    }

    http_request(key id, string method, string body)
    {
        key owner = llGetOwner();
        vector ownerSize = llGetAgentSize(owner);

        if (url_request == id)
        {
        //  if you're usually not resetting the query ID
        //  now is a good time to start!
            url_request = "";

            if (method == URL_REQUEST_GRANTED)
            {
                llOwnerSay("URL: " + body);

            //  if owner in sim
                if (ownerSize)//  != ZERO_VECTOR
                    llLoadURL(owner, "I got a new URL!", body);
            }

            else if (method == URL_REQUEST_DENIED)
                llOwnerSay("Something went wrong, no url:\n" + body);
        }

        else
        {
            llOwnerSay("request body:\n" + body);

        //  if owner in sim
            if (ownerSize)//  != ZERO_VECTOR
            {
                llSetContentType(id, CONTENT_TYPE_HTML);
                llHTTPResponse(id, 200, HTML_BODY);
            }
            else
            {
                llSetContentType(id, CONTENT_TYPE_TEXT);
                llHTTPResponse(id, 200, "OK");
            }
        }
    }
}
```

## Notes

- A workaround for displaying HTML to non-owners inworld can be found here.

## See Also

### Events

- http_request
- http_response

### Functions

- llHTTPResponse

### Articles

- LSL HTTP server
- HTML HUD Demo

<!-- /wiki-source -->
