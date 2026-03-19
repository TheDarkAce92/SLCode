---
name: "llHTTPResponse"
category: "function"
type: "function"
language: "LSL"
description: 'Responds to request_id with status and body.

The response need not be made inside the http_request event but if it does not happen in a timely fashion the request will time out (within 25 seconds).'
signature: "void llHTTPResponse(key request_id, integer status, string body)"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llHTTPResponse'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llhttpresponse"]
---

Responds to request_id with status and body.

The response need not be made inside the http_request event but if it does not happen in a timely fashion the request will time out (within 25 seconds).


## Signature

```lsl
void llHTTPResponse(key request_id, integer status, string body);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `key (handle)` | `request_id` | A valid HTTP request key. |
| `integer` | `status` | HTTP Status (200, 400, 404, etc) |
| `string` | `body` | Contents of the response. |


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llHTTPResponse)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llHTTPResponse) — scraped 2026-03-18_

Responds to request_id with status and body.

## Caveats

- This call must be made by the script containing the http_request event where the request_id was received.
- There is no limit, other than script size, to the amount of data that can be sent by this function.

  - llHTTPRequest can truncate the response length in *receiving* scripts. Be aware when using them together for prim-to-prim communications.
- The response by default has `"content-type: text/plain"`. Use llSetContentType to optionally return a different type, like `"text/html"`.

## Examples

```lsl
string url;

default
{
    changed(integer change)
    {
        if (change & (CHANGED_REGION_START | CHANGED_REGION | CHANGED_TELEPORT))
            llResetScript();
    }

    state_entry()
    {
        llRequestURL();
    }

    touch_start(integer num_detected)
    {
    //  PUBLIC_CHANNEL has the integer value 0
        if (url != "")
            llSay(PUBLIC_CHANNEL, "URL: " + url);
    }

    http_request(key id, string method, string body)
    {
    //  http://en.wikipedia.org/wiki/Create,_read,_update_and_delete
        list CRUDmethods = ["GET", "POST", "PUT", "DELETE"];
    //  it's bit-wise NOT ( ~ ) !!!
        integer isAllowedMethod = ~llListFindList(CRUDmethods, [method]);

        if (isAllowedMethod)
        {
            llHTTPResponse(id, 200, "Body of request below:\n" + body);
        }
        else if (method == URL_REQUEST_GRANTED)
        {
        //  don't forget the trailing slash
            url = body + "/";

            llOwnerSay("URL: " + url);
        }
        else if (method == URL_REQUEST_DENIED)
        {
            llOwnerSay("Something went wrong, no URL.\n" + body);
        }
        else
        {
            llOwnerSay("Ummm... I have no idea what SL just did. Method=\""+method+"\"\n" + body);
        }
    }
}
```

## See Also

### Constants

- CONTENT_TYPE_TEXT
- CONTENT_TYPE_HTML
- CONTENT_TYPE_XML
- CONTENT_TYPE_XHTML
- CONTENT_TYPE_ATOM
- CONTENT_TYPE_JSON
- CONTENT_TYPE_LLSD
- CONTENT_TYPE_FORM
- CONTENT_TYPE_RSS

### Events

- http_request
- http_response

### Functions

- llGetFreeURLs
- llRequestURL
- llRequestSecureURL
- llReleaseURL
- llGetHTTPHeader
- llSetContentType

### Articles

- LSL http server

<!-- /wiki-source -->
