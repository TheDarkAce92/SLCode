---
name: "HTTP constants"
category: "constant"
type: "constant"
language: "LSL"
description: "Constants for configuring llHTTPRequest parameters and reading http_response metadata"
wiki_url: "https://wiki.secondlife.com/wiki/HTTP_METHOD"
first_fetched: "2026-03-09"
last_updated: "2026-03-09"
---

# HTTP_* Constants

Used as flag-value pairs in the `parameters` list argument of `llHTTPRequest`, and as keys in `http_response` metadata.

## Request Configuration Constants

| Constant | Type | Default | Description |
|----------|------|---------|-------------|
| `HTTP_METHOD` | integer | — | HTTP method: value is string `"GET"`, `"POST"`, `"PUT"`, `"DELETE"` |
| `HTTP_MIMETYPE` | integer | — | Content-Type header; value is MIME type string |
| `HTTP_BODY_MAXLENGTH` | integer | — | Max response body bytes; value is integer (default 2048, max 16384 Mono) |
| `HTTP_VERIFY_CERT` | integer | — | SSL cert validation; value is TRUE or FALSE |
| `HTTP_VERBOSE_THROTTLE` | integer | — | Suppress throttle errors if FALSE |
| `HTTP_CUSTOM_HEADER` | integer | — | Two string values follow: header name, header value |
| `HTTP_PRAGMA_NO_CACHE` | integer | — | Include Pragma: no-cache; value is TRUE or FALSE |
| `HTTP_USER_AGENT` | integer | — | Appended to LSL user agent; value is string |
| `HTTP_ACCEPT` | integer | — | Accepted response MIME types; value is string |
| `HTTP_EXTENDED_ERROR` | integer | — | Return RFC 7807 error JSON; value is TRUE or FALSE |

## Response Metadata Constants

| Constant | Description |
|----------|-------------|
| `HTTP_BODY_TRUNCATED` | Present in metadata list when body was truncated; value is truncation byte offset |

## Usage

```lsl
key reqId = llHTTPRequest(
    "https://api.example.com/data",
    [
        HTTP_METHOD, "POST",
        HTTP_MIMETYPE, "application/json",
        HTTP_BODY_MAXLENGTH, 16384,
        HTTP_VERIFY_CERT, TRUE,
        HTTP_CUSTOM_HEADER, "Authorization", "Bearer mytoken",
        HTTP_EXTENDED_ERROR, TRUE
    ],
    llList2Json(JSON_OBJECT, ["query", "hello"])
);

http_response(key id, integer status, list meta, string body)
{
    if (id != reqId) return;

    // Check if body was truncated
    integer truncIdx = llListFindList(meta, [HTTP_BODY_TRUNCATED]);
    if (truncIdx != -1)
        llOwnerSay("Body truncated at: " + (string)llList2Integer(meta, truncIdx + 1));

    llOwnerSay("Status: " + (string)status + " Body: " + body);
}
```

## See Also

- `llHTTPRequest` — send HTTP request
- `http_response` event — receive HTTP response
- `HTTP_VERIFY_CERT`, `HTTP_BODY_MAXLENGTH` (individual constant pages)
