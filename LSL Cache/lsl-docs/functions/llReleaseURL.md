---
name: "llReleaseURL"
category: "function"
type: "function"
language: "LSL"
description: "Releases the specified URL, it will no longer be usable."
signature: "void llReleaseURL(string url)"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llReleaseURL'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llreleaseurl"]
---

Releases the specified URL, it will no longer be usable.


## Signature

```lsl
void llReleaseURL(string url);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `string` | `url` | URL to release |


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llReleaseURL)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llReleaseURL) — scraped 2026-03-18_

Releases the specified URL, it will no longer be usable.

## Caveats

- URLs are automatically released and invalidated in certain situations. In the following situations, there is no need to call llReleaseURL. But you will have to request a new one afterwards

  - When the region is restarted or goes offline
  - When the script holding the URLs is reset, or recompiled
  - When the object containing the script is deleted, or taken to inventory

## Examples

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
    llSetTimerEvent(0.0);
    urlRequestId = llRequestURL();
}

throw_exception(string inputString)
{
    llInstantMessage(llGetOwner(), inputString);

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
        if (change & CHANGED_OWNER | CHANGED_REGION | CHANGED_REGION_START)
            llResetScript();
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
            llLoadURL(llGetOwner(), "Click to visit my URL!", url);

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

## See Also

### Functions

- llRequestURL
- llRequestSecureURL
- llGetFreeURLs
- llHTTPResponse
- llGetHTTPHeader

### Articles

- LSL http server

<!-- /wiki-source -->
