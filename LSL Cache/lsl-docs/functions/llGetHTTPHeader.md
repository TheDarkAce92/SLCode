---
name: "llGetHTTPHeader"
category: "function"
type: "function"
language: "LSL"
description: 'Returns a string that is the value for header for request_id.

Returns an empty string if the header is not found, if the request_id is not a valid key received through the http_request event, or if the headers can no longer be accessed. Headers can only be accessed before llHTTPResponse is called a'
signature: "string llGetHTTPHeader(key request_id, string header)"
return_type: "string"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetHTTPHeader'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgethttpheader"]
---

Returns a string that is the value for header for request_id.

Returns an empty string if the header is not found, if the request_id is not a valid key received through the http_request event, or if the headers can no longer be accessed. Headers can only be accessed before llHTTPResponse is called and with-in the first 30&nbsp;seconds after the http_request event is queued.


## Signature

```lsl
string llGetHTTPHeader(key request_id, string header);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `key (handle)` | `request_id` | A valid HTTP request key. |
| `string` | `header` | Lower case header value name. |


## Return Value

Returns `string`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetHTTPHeader)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetHTTPHeader) — scraped 2026-03-18_

Returns a string that is the value for header for request_id.

## Caveats

- Header information becomes inaccessible after 30 seconds or if llHTTPResponse is called.
- Function returns an empty string in any context outside the http_request event. For instance, it cannot be used in the http_response event.
- Custom headers are not supported, only the headers listed in the specification are supported.
- LSL is not a CGI environment

  - "Content-Type" is an example of a normal header name, in a CGI environment the name would be "HTTP_CONTENT_TYPE".
- **header** must be lower case (or it will match nothing). All header names are converted to lower case when they are received.
- When making a request...

  - The path part of the URL must be prefixed with a forward slash

  - Good: [https://sim3015.aditi.lindenlab.com:12043/cap/a7717681-2c04-e4ac-35e3-1f01c9861322/foo](https://sim3015.aditi.lindenlab.com:12043/cap/a7717681-2c04-e4ac-35e3-1f01c9861322/foo)
  - Bad: [https://sim3015.aditi.lindenlab.com:12043/cap/a7717681-2c04-e4ac-35e3-1f01c9861322foo](https://sim3015.aditi.lindenlab.com:12043/cap/a7717681-2c04-e4ac-35e3-1f01c9861322foo)
  - In order to use the query string, you must include a path (even if it is just a slash)

  - Good: [https://sim3015.aditi.lindenlab.com:12043/cap/a7717681-2c04-e4ac-35e3-1f01c9861322/?arg=gra](https://sim3015.aditi.lindenlab.com:12043/cap/a7717681-2c04-e4ac-35e3-1f01c9861322/?arg=gra)
  - Bad: [https://sim3015.aditi.lindenlab.com:12043/cap/a7717681-2c04-e4ac-35e3-1f01c9861322?arg=gra](https://sim3015.aditi.lindenlab.com:12043/cap/a7717681-2c04-e4ac-35e3-1f01c9861322?arg=gra)

## Examples

```lsl
key url_request;

default
{
    state_entry()
    {
        url_request = llRequestURL();
    }

    http_request(key id, string method, string body)
    {
        if (url_request == id)
        {
        //  if you're usually not resetting the query ID
        //  now is a good time to start!
            url_request = "";

            if (method == URL_REQUEST_GRANTED)
            {
                llOwnerSay("URL: " + body);

                key owner = llGetOwner();
                vector ownerSize = llGetAgentSize(owner);

                if (ownerSize)//  != ZERO_VECTOR
                    llLoadURL(owner, "I got a new URL!", body);
            }

            else if (method == URL_REQUEST_DENIED)
                llOwnerSay("Something went wrong, no url:\n" + body);
        }

        else
        {
            list headerList = ["x-script-url",
                            "x-path-info", "x-query-string",
                            "x-remote-ip", "user-agent"];

            integer index = -llGetListLength(headerList);
            do
            {
                string header = llList2String(headerList, index);
                llOwnerSay(header + ": " + llGetHTTPHeader(id, header));
            }
            while (++index);

            llOwnerSay("body:\n" + body);
            llHTTPResponse(id, 200, body);
        }
    }
}
```

## See Also

### Events

- http_request

### Functions

- llGetFreeURLs
- llRequestURL
- llRequestSecureURL
- llReleaseURL
- llHTTPResponse

### Articles

- LSL http server

<!-- /wiki-source -->
