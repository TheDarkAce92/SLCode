---
name: "llRemoteDataReply"
category: "function"
type: "function"
language: "LSL"
description: "Send an XML-RPC reply on channel to message_id with payload of string sdata and integer idata"
signature: "void llRemoteDataReply(key channel, key message_id, string sdata, integer idata)"
return_type: "void"
sleep_time: "3.0"
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llRemoteDataReply'
deprecated: "true"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llremotedatareply"]
---

Send an XML-RPC reply on channel to message_id with payload of string sdata and integer idata


## Signature

```lsl
void llRemoteDataReply(key channel, key message_id, string sdata, integer idata);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `key (channel)` | `channel` |  |
| `key` | `message_id` |  |
| `string` | `sdata` |  |
| `integer` | `idata` |  |


## Caveats

- Forced delay: **3.0 seconds** — the script sleeps after each call.
- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llRemoteDataReply)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llRemoteDataReply) — scraped 2026-03-18_

Send an XML-RPC reply on channel to message_id with payload of string sdata and integer idata

## Caveats

- This function causes the script to sleep for 3.0 seconds.
- This function has been deprecated, please use LSL_http_server instead.

## See Also

### Events

- remote_data

<!-- /wiki-source -->
