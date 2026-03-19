---
name: "http_response"
category: "event"
type: "event"
language: "LSL"
description: "Fires when an HTTP response is received for a request made by llHTTPRequest"
wiki_url: "https://wiki.secondlife.com/wiki/Http_response"
first_fetched: "2026-03-09"
last_updated: "2026-03-09"
signature: "http_response(key request_id, integer status, list metadata, string body)"
parameters:
  - name: "request_id"
    type: "key"
    description: "Matches the key returned by llHTTPRequest"
  - name: "status"
    type: "integer"
    description: "HTTP status code (200 = success; 499 = timeout/SSL error)"
  - name: "metadata"
    type: "list"
    description: "HTTP_* metadata constants and their values"
  - name: "body"
    type: "string"
    description: "Response body from the remote server"
deprecated: "false"
---

# http_response

```lsl
http_response(key request_id, integer status, list metadata, string body)
{
    if (request_id != myRequestKey) return;
    // handle response
}
```

Fires in **all scripts in the prim** when an HTTP response arrives for any `llHTTPRequest` made from any script in that prim. Always filter by `request_id`.

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `request_id` | key | Matches the key returned by `llHTTPRequest` |
| `status` | integer | HTTP status code |
| `metadata` | list | Response metadata (`HTTP_BODY_TRUNCATED`) |
| `body` | string | Response body (may be truncated per `HTTP_BODY_MAXLENGTH`) |

## Status Codes

| Status | Meaning |
|--------|---------|
| 200 | OK — successful response |
| 404 | Not Found |
| 499 | SL-specific: request timed out (60s), SSL failure, or unescaped spaces in URL |
| 502 | Bad Gateway — in-world object did not respond in time |
| 503 | Service Unavailable — request throttled |

## Metadata Constants

| Constant | Type | Description |
|----------|------|-------------|
| `HTTP_BODY_TRUNCATED` | integer | Byte offset at which the body was truncated |

## Caveats

- **Fires in ALL scripts in the prim** — always compare `request_id` to filter.
- **No guarantee of delivery** — if the script changes region before the response arrives, it is lost.
- **Body size limit** — controlled by `HTTP_BODY_MAXLENGTH` in the request (default 2048, max 16384 for Mono).

## Example

```lsl
key requestId;

default
{
    state_entry()
    {
        requestId = llHTTPRequest("https://example.com/api", [], "");
    }

    http_response(key request_id, integer status, list metadata, string body)
    {
        if (request_id != requestId) return;

        if (status == 200)
            llOwnerSay("Got: " + body);
        else
            llOwnerSay("HTTP error: " + (string)status);
    }
}
```

## See Also

- `llHTTPRequest` — initiate the HTTP request
- `llHTTPResponse` — send an HTTP response (for URL endpoints)
- `http_request` event — for in-world URL endpoints


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/http_response) — scraped 2026-03-18_

## Caveats

- This events will be triggered in every script in the prim, not just in the requesting script.
- It is *not* guaranteed that there will be an http_response for every llHTTPRequest().

  - If the script moves to a different region before the remote HTTP server can respond, the response will be lost. [[1]](https://lists.secondlife.com/pipermail/secondlifescripters/2011-August/006309.html)

## Examples

```lsl
key http_request_id;

default
{
    state_entry()
    {
        http_request_id = llHTTPRequest("url", [], "");
    }

    http_response(key request_id, integer status, list metadata, string body)
    {
        if (request_id == http_request_id)
        {
            llSetText(body, <0,0,1>, 1);
        }
    }
}
```

To parse POST content:

```lsl
string get_post_value(string content, string returns)
{
//  this parses application/x-www-form-urlencoded POST data

//  for instance if the webserver posts 'data1=hi&data2=blah' then
//  calling get_post_value("data1=hi&data2=blah","data1"); would return "hi"
//  written by MichaelRyan Allen, Unrevoked Clarity

    list params =  llParseString2List(content,["&"],[]);
    integer index = ~llGetListLength(params);

    list keys;// = [];
    list values;// = [];

    // start with -length and end with -1
    while (++index)
    {
        list parsedParams =  llParseString2List(llList2String(params, index), ["="], []);
        keys += llUnescapeURL(llList2String(parsedParams, 0));
        values += llUnescapeURL(llList2String(parsedParams, 1));
    }

    integer found = llListFindList(keys, [returns]);
    if(~found)
        return llList2String(values, found);
//  else
        return "";
}
```

Another Example:

|  | Important: Remember to release URLs that you have requested! They are region resources just like prims, and it is possible to use them all and break other scripts. |
| --- | --- |

```lsl
string url;
key urlRequestId;
key selfCheckRequestId;

request_url()
{
    llReleaseURL(url);
    url = "";

    urlRequestId = llRequestURL();
}

throw_exception(string inputString)
{
    key owner = llGetOwner();
    llInstantMessage(owner, inputString);

    // yeah, bad way to handle exceptions by restarting.
    // However this is just a demo script...

    llResetScript();
}

default
{
    on_rez(integer start_param)
    {
        llResetScript();
    }

    changed(integer change)
    {
        if (change & (CHANGED_OWNER | CHANGED_INVENTORY))
        {
            llReleaseURL(url);
            url = "";

            llResetScript();
        }

        if (change & (CHANGED_REGION | CHANGED_REGION_START | CHANGED_TELEPORT))
            request_url();
    }

    state_entry()
    {
        request_url();
    }

    http_request(key id, string method, string body)
    {
        integer responseStatus = 400;
        string responseBody = "Unsupported method";

        if (method == URL_REQUEST_DENIED)
            throw_exception("The following error occurred while attempting to get a free URL for this device:\n \n" + body);

        else if (method == URL_REQUEST_GRANTED)
        {
            url = body;
            key owner = llGetOwner();
            llLoadURL(owner, "Click to visit my URL!", url);

            // check every 5 mins for dropped URL
            llSetTimerEvent(300.0);
        }
        else if (method == "GET")
        {
            responseStatus = 200;
            responseBody = "Hello world!";
        }
        // else if (method == "POST") ...;
        // else if (method == "PUT") ...;
        // else if (method == "DELETE") { responseStatus = 403; responseBody = "forbidden"; }

        llHTTPResponse(id, responseStatus, responseBody);
    }

    http_response(key id, integer status, list metaData, string body)
    {
        if (id == selfCheckRequestId)
        {
            // If you're not usually doing this,
            // now is a good time to get used to doing it!
            selfCheckRequestId = NULL_KEY;

            if (status != 200)
                request_url();
        }

        else if (id == NULL_KEY)
            throw_exception("Too many HTTP requests too fast!");
    }

    timer()
    {
        selfCheckRequestId = llHTTPRequest(url,
                                [HTTP_METHOD, "GET",
                                    HTTP_VERBOSE_THROTTLE, FALSE,
                                    HTTP_BODY_MAXLENGTH, 16384],
                                "");
    }
}
```

## Notes

### Parsing Problems

If for some reason while using llHTTPRequest/http_response you are unable to parse a known good RSS feed or some other form of web contents, you will need to work around it outside of Second Life. This is unlikely to change in the near future since checking the headers requires more overhead at the simulator level.

### Unicode

When serving content with UTF-8 characters be sure your server sets the outgoing `Content-Type` header so that it includes `charset=utf-8` otherwise it will be interpreted incorrectly. See [W3C:Setting the HTTP charset parameter](http://www.w3.org/International/O-HTTP-charset) for further details.

### Request Headers

| Header | Description | Example data |
| --- | --- | --- |
| Connection | Connection options | close |
| Cache-Control | Maximum response age accepted. | max-age=259200 |
| X-Forwarded-For | Used to show the IP address connected to through proxies. | 127.0.0.1 |
| Via | Shows the recipients and protocols used between the User Agent and the server. | 1.1 sim10115.agni.lindenlab.com:3128 (squid/2.7.STABLE9) |
| Content-Length | The size of the entity-body, in decimal number of octets. | 17 |
| Pragma | The message should be forwarded to the server, even if it has a cached version of the data. | no-cache |
| X-SecondLife-Shard | The environment the object is in. "Production" is the main grid and "Testing" is the preview grid | Production |
| X-SecondLife-Region | The name of the region the object is in, along with the global coordinates of the region's south-west corner | Jin Ho (264448, 233984) |
| X-SecondLife-Owner-Name | Legacy name of the owner of the object | Zeb Wyler |
| X-SecondLife-Owner-Key | UUID of the owner of the object | 01234567-89ab-cdef-0123-456789abcdef |
| X-SecondLife-Object-Name | The name of the object containing the script | Object |
| X-SecondLife-Object-Key | The key of the object containing the script | 01234567-89ab-cdef-0123-456789abcdef |
| X-SecondLife-Local-Velocity | The velocity of the object | 0.000000, 0.000000, 0.000000 |
| X-SecondLife-Local-Rotation | The rotation of the object containing the script | 0.000000, 0.000000, 0.000000, 1.000000 |
| X-SecondLife-Local-Position | The position of the object within the region | (173.009827, 75.551231, 60.950001) |
| User-Agent | The user-agent header sent by LSL Scripts. Contains Server version. | Second Life LSL/16.05.24.315768 (http://secondlife.com) |
| Content-Type | The media type of the entity body. | text/plain; charset=utf-8 |
| Accept-Charset | Acceptable character sets from the server. Q being the quality expected when sending the different character sets. | utf-8;q=1.0, *;q=0.5 |
| Accept | Media types the server will accept. | text/*, application/xhtml+xml, application/atom+xml, application/json, application/xml, application/llsd+xml, application/x-javascript, application/javascript, application/x-www-form-urlencoded, application/rss+xml |
| Accept-Encoding | Acceptable content encodings for the server. | deflate, gzip |
| Host | The internet host being requested. | secondlife.com |
| - CGI environments may place the headers into variables by capitalizing the entire name, replacing dashes with underscores, and prefixing the name with "HTTP_", e.g. "X-SecondLife-Object-Name" becomes "HTTP_X_SECONDLIFE_OBJECT_NAME". - HTTP header names are case insensitive [[2]](http://www.w3.org/Protocols/rfc2616/rfc2616-sec4.html#sec4.2). Some ISPs may modify the case of header names, as was seen in [BUG-5094](https://jira.secondlife.com/browse/BUG-5094). |  |  |

## See Also

### Functions

- llHTTPRequest
- llHTTPResponse

<!-- /wiki-source -->
