---
name: "llHTTPRequest"
category: "function"
type: "function"
language: "LSL"
description: "Sends an HTTP/HTTPS request and returns a key handle; triggers http_response event on completion"
wiki_url: "https://wiki.secondlife.com/wiki/llHTTPRequest"
first_fetched: "2026-03-09"
last_updated: "2026-03-09"
signature: "key llHTTPRequest(string url, list parameters, string body)"
parameters:
  - name: "url"
    type: "string"
    description: "Valid HTTP or HTTPS URL"
  - name: "parameters"
    type: "list"
    description: "Flag-value pairs configuring the request (HTTP_METHOD, HTTP_MIMETYPE, HTTP_BODY_MAXLENGTH, etc.)"
  - name: "body"
    type: "string"
    description: "Request body content (max 32 KB for Mono)"
return_type: "key"
energy_cost: "10.0"
sleep_time: "0.0"
patterns: ["llhttprequest"]
deprecated: "false"
---

# llHTTPRequest

```lsl
key llHTTPRequest(string url, list parameters, string body)
```

Sends an HTTP request and returns a key handle. Returns `NULL_KEY` if throttled. Triggers the `http_response` event in all scripts in the prim when the response arrives.

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `url` | string | HTTP/HTTPS URL |
| `parameters` | list | Configuration flag-value pairs |
| `body` | string | Request body |

## Configuration Parameters

| Flag | Value Type | Default | Description |
|------|-----------|---------|-------------|
| `HTTP_METHOD` | string | `"GET"` | HTTP method: GET, POST, PUT, DELETE |
| `HTTP_MIMETYPE` | string | `"text/plain;charset=utf-8"` | Content-Type header |
| `HTTP_BODY_MAXLENGTH` | integer | 2048 | Max response body bytes (max 16384 Mono, 4096 LSO) |
| `HTTP_VERIFY_CERT` | integer | TRUE | SSL certificate validation |
| `HTTP_VERBOSE_THROTTLE` | integer | TRUE | Suppress throttle error messages if FALSE |
| `HTTP_CUSTOM_HEADER` | string, string | — | Add custom headers (max 4096 combined) |
| `HTTP_PRAGMA_NO_CACHE` | integer | TRUE | Include Pragma: no-cache header |
| `HTTP_USER_AGENT` | string | — | Appended to LSL user agent string |
| `HTTP_ACCEPT` | string | `"text/plain;charset=utf-8"` | Accepted response MIME types |
| `HTTP_EXTENDED_ERROR` | integer | FALSE | Return RFC 7807 error detail in `http_response` |

## Throttle Limits

| Scope | Limit |
|-------|-------|
| Per object | 25 requests per 20 seconds |
| Per owner | 1000 requests per 20 seconds |
| HTTP 5xx errors | 5 per 60 seconds per script |

Returns `NULL_KEY` when throttled.

## Caveats

- **`http_response` fires in ALL scripts** in the prim — not just the requesting script. Use the key handle to filter.
- **60-second timeout:** Status 499 returned if server does not respond in time.
- **Redirects:** Followed transparently for GET only. Other methods return 302 status.
- **Cannot use `HTTP_CUSTOM_HEADER` to set `Content-Type`** — use `HTTP_MIMETYPE` instead.
- **URL validation:** Spaces and control characters in the URL cause runtime errors.
- **Maintenance windows:** Requests fail with 503 around 06:25 SLT daily.

## Transmitted Headers

SL automatically adds: `X-SecondLife-Shard`, `X-SecondLife-Region`, `X-SecondLife-Owner-Name`, `X-SecondLife-Owner-Key`, `X-SecondLife-Object-Name`, `X-SecondLife-Object-Key`, `X-SecondLife-Local-Position`, `X-SecondLife-Local-Rotation`, `X-SecondLife-Local-Velocity`, `User-Agent`.

## Example

```lsl
key requestId;

default
{
    state_entry()
    {
        requestId = llHTTPRequest("https://example.com/api/data",
            [HTTP_METHOD, "GET",
             HTTP_MIMETYPE, "application/json",
             HTTP_BODY_MAXLENGTH, 16384], "");
    }

    http_response(key request_id, integer status, list metadata, string body)
    {
        if (request_id != requestId) return;  // not our request
        if (status == 200)
            llOwnerSay("Response: " + body);
        else
            llOwnerSay("Error: " + (string)status);
    }
}
```

## Extended Error Response (HTTP_EXTENDED_ERROR)

When `HTTP_EXTENDED_ERROR` is TRUE, errors return JSON per RFC 7807:

```json
{
    "type": "http://wiki.secondlife.com/wiki/llHTTPRequest",
    "title": "Error Title",
    "detail": "Description of error condition.",
    "status": 400
}
```

## See Also

- `http_response` event — receives the response
- `llHTTPResponse` — send HTTP responses from a URL endpoint
- `llRequestURL` — request an HTTP endpoint URL for this script
- `llEscapeURL` / `llUnescapeURL` — URL-encode/decode strings


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llHTTPRequest) — scraped 2026-03-18_

Sends an HTTP request to the specified URL with the body of the request and parameters. When the response is received, a http_response event is raised.Returns a handle (a key) identifying the HTTP request made.

## Caveats

- Spaces, control characters, and other characters that are not allowed in URLs will cause a run time error.
- The corresponding http_response event will be triggered in all scripts in the prim, not just in the requesting script.
- Requests must fully complete after 60 seconds, or else the response will be thrown away and the http_response status code will be 499.
- The response body is limited to 2048 bytes by default, see HTTP_BODY_MAXLENGTH above to increase it. If the response is longer, it will be truncated.
- The request body size (e.g., of POST and PUT requests) is limited only by available script memory. Scripts can hold at most 32k characters in a string, under Mono, as characters are two bytes each, so, scripts cannot upload over 32k UTF-8 characters
- Cannot be used to load textures or images from the internet, for more information see Web Textures.
- If the accessed site is relying on the LSL script to report L$ transactions, then it **must** check the `X-SecondLife-Shard` header to see if the script is running on the beta grid.
- Some servers will return a `405` error if you send POST to a file that can't accept metadata, such as a text or HTML file. Make sure you use the GET method to ensure success in any environment.
- While the HTTP status code from the server is provided to the script, redirect codes such as `302` will result in the redirect being automatically and transparently followed ONLY IF the HTTP_METHOD is GET, with the resulting response being returned.  If the HTTP_METHOD is anything other than GET then you'll get back an http_response with a status code of `302`, but without any way to view the headers, you can't know where you were being redirected to unless that was also included in the body.
- The following applies when making a request to a script using HTTP-In:

  - When appending a query string to a cap URL there **MUST** be a trailing slash between the cap guid and the query string token `"?"`. For example: [https://sim3015.aditi.lindenlab.com:12043/cap/a7717681-2c04-e4ac-35e3-1f01c9861322?arg=gra](https://sim3015.aditi.lindenlab.com:12043/cap/a7717681-2c04-e4ac-35e3-1f01c9861322?arg=gra) will return a 500 HTTP status  [Server Error code](https://en.wikipedia.org/wiki/List_of_HTTP_status_codes%235xx_Server_Error), but [https://sim3015.aditi.lindenlab.com:12043/cap/a7717681-2c04-e4ac-35e3-1f01c9861322/?arg=gra](https://sim3015.aditi.lindenlab.com:12043/cap/a7717681-2c04-e4ac-35e3-1f01c9861322/?arg=gra) will succeed.
- `X-SecondLife-Owner-Name` may return `"(Loading...)"` instead of owner name (still true, 30th of March, 2022)
- Requests made at approx 0625 SLT may fail with a `503` status code, with `"ERROR: The requested URL could not be retrieved"`, and `"(111) Connection refused"` in the body of the response.  This has been confirmed as expected behavior by Kelly, due to the nightly maintenance and log rotation.  It does reliably impact object to object HTTP at that time, and quite probably may impact object to/from web around the same time.  The interruption in service is fairly brief, and the precise timing may vary as LL adjust their nightly maintenance processes, or due to server load.
- Use `HTTP_MIMETYPE` to set the `Content-Type` header. Attempts to use `HTTP_CUSTOM_HEADER` to set it will cause a runtime script error.
- If the origin server does not include a content-type header in its response, LSL will attempt to treat the incoming data as "text/plain; charset=utf-8". This behavior diverges from [RFC 2616](https://datatracker.ietf.org/doc/html/rfc2616#section-7.2.1).

#### Throttles

The LSL function llHTTPRequest is throttled in three ways:  by object, by owner, and by http error.  All group-owned objects are considered together in the same throttle.

The current limits are:

- 25 requests in 20 seconds for each object
- 1000 requests in 20 seconds for each owner with higher limits for some regions
- Five HTTP errors (500 or higher) in 60 seconds for each script

These may change in the future if needed to prevent problems in regions.

It is possible for a large collection of objects or scripts to make many calls to llHTTPRequest and reach one or more throttles.  When a script calls llHTTPRequest with a throttle blocking the request, it will return NULL_KEY.

The calling script must check for the NULL_KEY result and react properly for the script and object to function correctly.  Some things to consider:

- Pause further requests until the throttle clears
- Do not make any additional llHTTPRequest calls until enough time has passed for the throttle to reset.    They will fail and continue to return NULL_KEY otherwise.
- Once reached, the throttles will remain in effect as long as requests continue, but will clear if there is a silent period with no requests at least twice the throttle interval, in the common case 2 * 20 or 40 seconds.‎

Consider how a group of objects behaves.   Developers must consider how multiple objects will interact and how that will affect clearing the throttle.‎
The llHTTPRequest throttle is most likely to be an issue with a large number of objects in a region making requests.  To clear the throttle fastest, when an object encounters the throttle, it should broadcast a region-wide chat message to other objects informing them of the event and stopping their requests. If those objects continue making requests, those requests will fail and just prolong recovery.‎
If an object waits and still gets a failure, it may be a good idea to increase the time before the next request and/or add a small random value to the wait time. This may help prevent failures caused by large groups of objects acting nearly in unison.

- Object requests are throttled at approximately 25 requests per 20 seconds. This is to support a sustained rate of one per second or a maximum burst of up to 25 every 40 seconds (twice the interval for maximum burst), smaller bursts are recommended.
- NULL_KEY is returned if the request is throttled.
- See [this thread](http://forums-archive.secondlife.com/139/72/108960/1.html) and [this thread](http://forums-archive.secondlife.com/139/2c/109571/1.html) for older details.

## Examples

- Writing Headers and HTTP POST Body to a File

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
        if (request_id != http_request_id) return;// exit if unknown

        vector COLOR_BLUE = <0.0, 0.0, 1.0>;
        float  OPAQUE     = 1.0;

        llSetText(body, COLOR_BLUE, OPAQUE);
    }
}
```

Example PHP test script:

```lsl
<?php header("content-type: text/plain; charset=utf-8"); ?>
Headers received:
<?php

/**
 * @author Wouter Hobble
 * @copyright 2008
 */

foreach ($_SERVER as $k => $v)
{
    if( substr($k, 0, 5) == 'HTTP_')
    {
        print "\n". $k. "\t". $v;
    }
}
?>
```

Example PHP wrapper script both capturing Apache headers and global methods

```lsl
<?php
    // Author Waster Skronski.
    // General Public License (GPL).
    // Mind that some headers are not included because they're either useless or unreliable.

    $USE_APACHE_HEADERS = TRUE;// switch to false if you need CGI methods

    if ($USE_APACHE_HEADERS)
    {
        $headers    = apache_request_headers();
        $objectgrid = $headers["X-SecondLife-Shard"];
        $objectname = $headers["X-SecondLife-Object-Name"];
        $objectkey  = $headers["X-SecondLife-Object-Key"];
        $objectpos  = $headers["X-SecondLife-Local-Position"];
        $ownerkey   = $headers["X-SecondLife-Owner-Key"];
        $ownername  = $headers["X-SecondLife-Owner-Name"];
        $regiondata = $headers["X-SecondLife-Region"];
        $regiontmp  = explode ("(",$regiondata);        // cut coords off
        $regionpos  = explode (")",$regiontmp[1]);
        $regionname = substr($regiontmp[0],0,-1);       // cut last space from region name
    } else {
        $db         = $GLOBALS;
        $headers    = $db['$_ENV'];
        $objectgrid = $headers["HTTP_X_SECONDLIFE_SHARD"];
        $objectname = $headers["HTTP_X_SECONDLIFE_OBJECT_NAME"];
        $objectkey  = $headers["HTTP_X_SECONDLIFE_OBJECT_KEY"];
        $ownerkey   = $headers["HTTP_X_SECONDLIFE_OWNER_KEY"];
        $objectpos  = $headers["HTTP_X_SECONDLIFE_LOCAL_POSITION"];
        $ownername  = $headers["HTTP_X_SECONDLIFE_OWNER_NAME"];
        $regiondata = $headers["HTTP_X_SECONDLIFE_REGION"];
        $regiontmp  = explode ("(",$regiondata);
        $regionpos  = explode (")",$regiontmp[1]);
        $regionname = substr($regiontmp[0],0,-1);
    }
?>
```

Example wrapper script for GoDaddy.com Linux PHP servers (fix made by Thomas Conover):

```lsl
<?php
// FETCH HEADERS START

if (!function_exists('apache_request_headers'))
{
    function apache_request_headers() {
        foreach($_SERVER as $key=>$value) {
            if (substr($key,0,5)=="HTTP_") {
                $key=str_replace(" ","-",ucwords(strtolower(str_replace("_"," ",substr($key,5)))));
                $out[$key]=$value;
            }else{
                $out[$key]=$value;
            }
        }
        return $out;
    }
}
// Mind that some headers are not included because they're either useless or unreliable (e.g. X-Secondlife-Local-Position)
$headers    = apache_request_headers();
$objectgrid = $headers["X-Secondlife-Shard"];
$objectname = $headers["X-Secondlife-Object-Name"];
$objectkey  = $headers["X-Secondlife-Object-Key"];
$objectpos  = $headers["X-Secondlife-Local-Position"];
$ownerkey   = $headers["X-Secondlife-Owner-Key"];
$ownername  = $headers["X-Secondlife-Owner-Name"];
$regiondata = $headers["X-Secondlife-Region"];
$regiontmp  = explode ("(",$regiondata);            // cut coords off
$regionname = substr($regiontmp[0],0,-1);           // cut last space from region name
$regiontmp  = explode (")",$regiontmp[1]);
$regionpos  = $regiontmp[0];

// FETCH HEADERS END
?>
```

## Notes

If for some reason while using the function llHTTPRequest or the event http_response you are unable to parse a known good RSS feed or some other form of web contents, you will need to work around it outside of Second Life. This is unlikely to change in the near future since checking the headers requires more overhead at the simulator level.

You may find that some web servers return either a null or a nonsensical result when llHTTPRequest is used, even though the same URL in a PC web browser returns the expected result. This may be due to the fact that the llHTTPRequest User Agent string is not recognised by some web servers as it does not contain `"Mozilla"`, which would identify it as a web browser instead of, for example, a [Shoutcast](https://www.shoutcast.com/) or an RSS client. This is also true when the PHP script relies on [$_COOKIE](https://www.php.net/manual/en/reserved.variables.cookies.php). Neither can the function llHTTPRequest set a cookie nor can the event http_request retrieve them.

CGI environments may place the headers into variables by capitalizing the entire name, replacing dashes with underscores, and prefixing the name with `HTTP_`, e.g. `HTTP_X_SECONDLIFE_OBJECT_NAME`. PHP `$_SERVER` variables do this as well, and so does PHP running inside PHP-FPM (as opposed to an Apache module), which is the standard way to configure PHP on non-Apache webservers (such as [`nginx`](https://nginx.org/nginx)).

Apache can include the headers in its logs, using the `CustomLog` and `LogFormat` directives.  See [the docs](https://httpd.apache.org/docs/2.4/mod/mod_log_config.html#formats) for details on the syntax.

## See Also

### Events

- http_response

### Functions

- llEscapeURL
- llHTTPResponse
- llUnescapeURL

### Articles

- Simulator IP Addresses

<!-- /wiki-source -->
