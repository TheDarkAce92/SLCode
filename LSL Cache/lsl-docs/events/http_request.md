---
name: "http_request"
category: "event"
type: "event"
language: "LSL"
description: "Triggered when task receives an HTTP request."
signature: "http_request(key request_id, string method, string body)"
wiki_url: 'https://wiki.secondlife.com/wiki/http_request'
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
deprecated: "false"
parameters: []
---

Triggered when task receives an HTTP request.


## Signature

```lsl
http_request(key request_id, string method, string body)
{
    // your code here
}
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `key (handle)` | `request_id` | HTTP request id for response use, and function response identification. |
| `string` | `method` | GET, POST, PUT, DELETE, URL_REQUEST_GRANTED, URL_REQUEST_DENIED |
| `string` | `body` | Contents of the request. |


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/http_request)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/http_request) — scraped 2026-03-18_

## Caveats

- body is limited to 2048 bytes; anything longer will be truncated to 2048 bytes.

  - As per the above, this function is unaffected by any values passed to llHTTPRequest via HTTP_BODY_MAXLENGTH, as they reside on the Outgoing pipeline, and this function is on the Incoming pipeline.
- headers (accessed with llGetHTTPHeader) are limited to 255 bytes.
- There is a limit of 64 pending http_request

  - Be mindful of the event queue (64) in general as well. http_request events may be discarded if your script's queue is filled by other events, such as incoming listen messages.
- body is not sent with the request unless the method is set to `"POST"`, `"PUT"`, or URL_REQUEST_GRANTED.
- Requests may fail with a [503 status code](https://en.wikipedia.org/wiki/List_of_HTTP_status_codes#5xx_Server_Error) for at least two possible reasons:

  - if the returned body is `ERROR: The requested URL could not be retrieved`, and `(111) Connection refused`, the problem will normally last only a few minutes - this is th nightly maint & log rotation.  It does reliably impact object to object HTTP at that time, and quite probably may impact object to/from web around the same time.  The interruption in service is fairly brief, and the precise timing may vary as LL adjust their nightly maint processes, or due to server load.
  - this response can also happen if too many requests are received by scripts in the region owned by the same owner. In this case, a Retry-After header is returned with a number of seconds to wait before retrying. Note that if you have many requestors, some of them may have to wait longer. A good general strategy is to wait the suggested number of seconds (possibly with a little randomness added in) before retrying, and if that fails increase how long you wait by multiplying by a small number before retrying again. If all your requestors follow some method like this, eventually they'll get through.

## Examples

See LSL_http_server/examples for some examples from the feature design phase.

|  | Important: Never ever forget to release a URL again which you have requested! URLs are region resources just like prims. If you take them all you can get into big trouble with the sim owner and/or estate managers. |
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

- When triggered by either llRequestURL or llRequestSecureURL the method will be either URL_REQUEST_GRANTED or URL_REQUEST_DENIED

  - If the method is URL_REQUEST_GRANTED The body will contain the full url, minus the trailing forward slash.

## See Also

### Functions

- **llRequestURL** — Request a new LSL Server public URL
- **llRequestSecureURL** — Request a new LSL Server public URL
- **llReleaseURL** — Release a URL
- **llHTTPResponse** — For replying to HTTP requests
- **llGetHTTPHeader** — Returns the requested HTTP header's value
- llEscapeURL
- llUnescapeURL

<!-- /wiki-source -->
