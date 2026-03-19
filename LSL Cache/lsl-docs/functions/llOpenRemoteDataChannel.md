---
name: "llOpenRemoteDataChannel"
category: "function"
type: "function"
language: "LSL"
description: "Creates a channel to listen for XML-RPC calls. Will trigger a remote_data event with channel id once it is available."
signature: "void llOpenRemoteDataChannel()"
return_type: "void"
sleep_time: "1.0"
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llOpenRemoteDataChannel'
deprecated: "true"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llopenremotedatachannel"]
---

Creates a channel to listen for XML-RPC calls. Will trigger a remote_data event with channel id once it is available.


## Signature

```lsl
void llOpenRemoteDataChannel();
```


## Caveats

- Forced delay: **1.0 seconds** — the script sleeps after each call.
- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llOpenRemoteDataChannel)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llOpenRemoteDataChannel) — scraped 2026-03-18_

Creates a channel to listen for XML-RPC calls. Will trigger a remote_data event with channel id once it is available.

## Caveats

- This function causes the script to sleep for 1.0 seconds.
- This function has been deprecated, please use LSL_http_server instead.
- **XML-RPC should not be used anymore. Use http-in instead, see LSL_http_server.**
- If an object moves from one region to another it must re-open the channel

  - The object will get the *same* channel as before, but without re-opening no requests will get through
- Any channel that is not used for 14 days will be cleaned up.

  - May be advisable to somewhat regularly (before expected use or on a regular schedule) check that the channel is good and hasn't changed by calling llOpenRemoteDataChannel and comparing to the previous channel.
- Note: XML-RPC requests often time-out due to the front-end server being overloaded.  LL has continued to upgrade the server hardware periodically, but it has remained unreliable.  LL developers have advised that the XML-RPC design isn't scalable (due to the single server bottle-neck) and that the service is "deprecated".  They suggest using HTTP Polling as an alternative.  If an XML-RPC request does time-out the script's remote_data event may or may not be triggered (and any script response is lost).

## Examples

```lsl
default
{
    state_entry()
    {
        llOpenRemoteDataChannel();
    }
    changed(integer c)
    {
        if(c & (CHANGED_REGION | CHANGED_TELEPORT))
            llOpenRemoteDataChannel();
    }
    remote_data( integer event_type, key channel, key message_id, string sender, integer idata, string sdata )
    {
        if (event_type == REMOTE_DATA_CHANNEL) { // channel created
        }
    }
}
```

<!-- /wiki-source -->
