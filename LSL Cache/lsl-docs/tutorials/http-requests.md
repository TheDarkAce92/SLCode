---
name: "HTTP Requests"
category: "tutorials"
type: "reference"
language: "LSL"
description: "Making HTTP GET and POST requests from LSL using llHTTPRequest and the http_response event, including throttle handling and error codes"
wiki_url: ""
local_only: true
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
---

# HTTP Requests

LSL can make outbound HTTP and HTTPS requests using `llHTTPRequest`. The call is asynchronous — it returns immediately, and the response arrives later via the `http_response` event.

## Basic GET Request

```lsl
key http_id;

default
{
    touch_end(integer num_detected)
    {
        http_id = llHTTPRequest("https://example.com/api/data", [], "");

        if (http_id == NULL_KEY)
        {
            llSay(0, "Request was throttled — try again later.");
        }
    }

    http_response(key request_id, integer status, list metadata, string body)
    {
        if (request_id != http_id)
            return;  // not our request

        if (status == 200)
        {
            llSay(0, "Response: " + body);
        }
        else
        {
            llSay(0, "Error " + (string)status + ": " + body);
        }
    }
}
```

## Return Value and Throttling

`llHTTPRequest` returns a `key` that identifies the pending request. If the request cannot be queued because the object has hit its rate limit, it returns `NULL_KEY`. Always check for this.

Rate limits:
- **25 requests per 20 seconds** per object.
- **1000 requests per 20 seconds** per owner (across all their objects, with higher limits on some regions).

## Matching the Response

`http_response` fires in every script in the object, not just the one that made the request. Always compare `request_id` against your stored key to make sure you are handling your own response.

## POST Request

```lsl
key http_id;

default
{
    touch_end(integer num_detected)
    {
        string payload = "{\"name\":\"SLCode\",\"value\":42}";

        http_id = llHTTPRequest(
            "https://example.com/api/submit",
            [HTTP_METHOD,   "POST",
             HTTP_MIMETYPE, "application/json"],
            payload
        );

        if (http_id == NULL_KEY)
            llSay(0, "Throttled.");
    }

    http_response(key request_id, integer status, list metadata, string body)
    {
        if (request_id != http_id)
            return;

        llSay(0, "Status: " + (string)status + "  Body: " + body);
    }
}
```

## Request Parameters

The second argument to `llHTTPRequest` is a flat list of flag/value pairs:

| Constant | Type | Description |
|---|---|---|
| `HTTP_METHOD` | string | `"GET"` (default), `"POST"`, `"PUT"`, `"DELETE"` |
| `HTTP_MIMETYPE` | string | Content-Type header for the body (default `"text/plain;charset=utf-8"`) |
| `HTTP_BODY_MAXLENGTH` | integer | Max response body bytes to return, 0–16384 (default 2048) |
| `HTTP_VERIFY_CERT` | integer | `TRUE` (default) to verify SSL certificate; `FALSE` to skip |

## Status Codes

| Status | Meaning |
|---|---|
| `200` | Success |
| `404` | Not found |
| `415` | Server response had an unrecognised Content-Type; body not forwarded |
| `499` | Timeout (60 seconds) or SSL error |
| `502` | Server returned no data |
| `503` | Too many requests from this simulator |

Status code `499` is specific to LSL and indicates that the request timed out or failed at the network/SSL level — it is not an HTTP standard code.

## Timeout

Requests time out after **60 seconds** if no response is received. This fires `http_response` with status `499`.

## Multiple Pending Requests

You can have multiple requests in flight at once. Track each with its own key variable.

```lsl
key req_weather;
key req_time;

default
{
    state_entry()
    {
        req_weather = llHTTPRequest("https://example.com/weather", [], "");
        req_time    = llHTTPRequest("https://example.com/time",    [], "");
    }

    http_response(key request_id, integer status, list metadata, string body)
    {
        if (request_id == req_weather)
        {
            llSay(0, "Weather: " + body);
        }
        else if (request_id == req_time)
        {
            llSay(0, "Time: " + body);
        }
    }
}
```

## Caveats

- The request body size is limited only by available script memory, not a fixed cap.
- **GET** requests automatically follow redirects transparently. **POST**, **PUT**, and **DELETE** requests do not — the redirect status code (e.g. 302) is returned directly to the script.
- `http_response` fires in all scripts in the object — always match `request_id`.
- If your script changes state between sending the request and receiving the response, the event is still delivered.
- A per-script error throttle applies: if a script receives 5 or more HTTP 5xx responses within 60 seconds, further requests from that script may be blocked.
