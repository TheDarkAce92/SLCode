---
name: "llSendRemoteData"
category: "function"
type: "function"
language: "LSL"
description: 'Send an XML-RPC request to dest through channel with payload of channel (in a string), integer idata and string sdata.

Returns a key that is the message_id for the resulting remote_data events.'
signature: "key llSendRemoteData(key channel, string dest, integer idata, string sdata)"
return_type: "key"
sleep_time: "3.0"
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llSendRemoteData'
deprecated: "true"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llsendremotedata"]
---

Send an XML-RPC request to dest through channel with payload of channel (in a string), integer idata and string sdata.

Returns a key that is the message_id for the resulting remote_data events.


## Signature

```lsl
key llSendRemoteData(key channel, string dest, integer idata, string sdata);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `key (channel)` | `channel` |  |
| `string` | `dest` |  |
| `integer` | `idata` |  |
| `string` | `sdata` |  |


## Return Value

Returns `key`.


## Caveats

- Forced delay: **3.0 seconds** — the script sleeps after each call.
- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llSendRemoteData)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llSendRemoteData) — scraped 2026-03-18_

Send an XML-RPC request to dest through channel with payload of channel (in a string), integer idata and string sdata.Returns a key that is the message_id for the resulting remote_data events.

## Caveats

- This function causes the script to sleep for 3.0 seconds.
- This function has been deprecated, please use LSL_http_server instead.

<!-- /wiki-source -->
