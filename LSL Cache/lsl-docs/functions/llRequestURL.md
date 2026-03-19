---
name: "llRequestURL"
category: "function"
type: "function"
language: "LSL"
description: 'Requests one HTTP:// URL for use by this script. The http_request event is triggered with the result of the request.

Returns a handle (a key) used for identifying the result of the request in the http_request event'
signature: "key llRequestURL()"
return_type: "key"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llRequestURL'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llrequesturl"]
---

Requests one HTTP:// URL for use by this script. The http_request event is triggered with the result of the request.

Returns a handle (a key) used for identifying the result of the request in the http_request event


## Signature

```lsl
key llRequestURL();
```


## Return Value

Returns `key`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llRequestURL)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llRequestURL) — scraped 2026-03-18_

Requests one HTTP://  URL for use by this script. The http_request event is triggered with the result of the request.Returns a handle (a key) used for identifying the result of the request in the http_request event.

## Caveats

- HTTP-in is not on the usual HTTP port number; the URL it provided in the http_request event includes the correct port number.
- Your script (and any client that uses it) should not "validate" the provided URL; in particular, do not assume that it maps to any particular address, or is in any particular domain. These will change during the uplift of Second Life to the cloud, and may be more dynamic following that uplift.
- Use of this function is throttled. Although it has no forced sleep time, too many requests (5-ish) in a short period will cause all further requests to be denied until the script stops requesting URLs for at least 1 second. Using an llSleep of 0.6 seconds or greater between each request will prevent you from being throttled.
- When a region is (re)started all HTTP server URLs are automatically released and invalidated.

  - Use CHANGED_REGION_START to detect this so new URL can be requested.
- The number of available URLs is a limited resource, that is to say, a script can only have so many open URLs. See LSL http_server#Resource Limitations for details.
- When abandoning a URL, release it with llReleaseURL, to avoid leaks. Resetting the script, or deleting the prim, will also suffice to release URLs.
- Unlike listeners, URLs persist across state changes

## Examples

A fully worked out example that shows how to get a URL, register that URL with an external client, and do proper backoff and retry for contacting external services can be found at HTTP Server URL Registration.

This script requests a new URL after region restart.

See the discussion page for explanations as to why this particular script never needs to use llReleaseURL().

```lsl
string url;
key urlRequestId;

default
{
	state_entry()
	{
		urlRequestId = llRequestURL();
	}

	on_rez(integer start_param)
	{
		llResetScript();
	}

	changed(integer change)
	{
		if (change & (CHANGED_OWNER | CHANGED_INVENTORY))
		{
			llResetScript();
		}
		if (change & (CHANGED_REGION | CHANGED_REGION_START | CHANGED_TELEPORT))
		{
			urlRequestId = llRequestURL();
		}
	}

	http_request(key id, string method, string body)
	{
		if (id == urlRequestId)
		{
			if (method == URL_REQUEST_DENIED)
			{
				llOwnerSay("The following error occurred while attempting to get a free URL for this device:\n\n" + body);
			}
			else if (method == URL_REQUEST_GRANTED)
			{
				url = body;
				llLoadURL(llGetOwner(), "Click to visit my URL!", url);
			}
		}
	}
}
```

It's important to keep in mind that if you request another URL, that the old one will not be released, it will remain active. The following script drives home this point.

Try the following code ONLY if you can use all your URLs on your land.
Removing the prim/script will release all URLs previous assigned.

```lsl
// WARNING:
//
//      This script is only for proof-of-concept (demo purposes).
//      DO NOT use it if you don't have the sim owners and/or
//      estate managers OK to test this script.
//      This script can possibly block HTTP communication from and to the sim.
//      ...bringing down all networked vendors and/or similar machines.
//
//      This script allocates all available URLs.
//      Deleting the script and/or derezzing the object containing the script,
//      will release all previously taken URLs.

default
{
	state_entry()
	{
		llRequestURL();
	}

	http_request(key id, string method, string body)
	{
		if (method == URL_REQUEST_DENIED)
		{
			llSetText("No free URLs!", <1.0, 0.0, 0.0>, 1.0);
		}
		else if (method == URL_REQUEST_GRANTED)
		{
			llSetText((string)llGetFreeURLs() + " URLs left\n" + body, <1.0, 1.0, 1.0>, 1.0);
			llRequestURL();
		}
		else if (method == "GET")
		{
			llHTTPResponse(id, 200, "Hello there!");
		}
	}
}
```

This script will, as you can see, use all URLs available on your land because it does not remove the old URLs before requesting a new one.

Just store the old URL in a global variable and release it with llReleaseURL.

## Notes

| Another comment on resilient programming: getting a global resource, an HTTP listener in this case, should always be considered an operation that can fail for transitory reasons (as well as permanent ones). In this case, LSL folds retryable and permanent errors into the same error status and there's no opportunity for a script writer to distinguish the two cases. But a reasonable way to handle this is sleeping with limited retries before failing hard in the LSL code. |
| --- |
| Monty Linden |

## See Also

### Functions

- llRequestSecureURL
- llGetFreeURLs
- llReleaseURL
- llHTTPResponse
- llGetHTTPHeader

### Articles

- LSL http server

<!-- /wiki-source -->
