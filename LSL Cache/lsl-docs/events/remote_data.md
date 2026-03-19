---
name: "remote_data"
category: "event"
type: "event"
language: "LSL"
description: "Triggered by various XML-RPC calls."
signature: "remote_data(integer event_type, key channel, key message_id, string sender, integer idata, string sdata)"
wiki_url: 'https://wiki.secondlife.com/wiki/remote_data'
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
deprecated: "false"
parameters: []
---

Triggered by various XML-RPC calls.


## Signature

```lsl
remote_data(integer event_type, key channel, key message_id, string sender, integer idata, string sdata)
{
    // your code here
}
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `integer` | `event_type` |  |
| `key (channel)` | `channel` |  |
| `key` | `message_id` |  |
| `string` | `sender` |  |
| `integer` | `idata` |  |
| `string` | `sdata` |  |


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/remote_data)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/remote_data) — scraped 2026-03-18_

## Caveats

- This event has been deprecated, please use LSL_http_server instead.

## See Also

### Functions

- llRemoteDataReply

<!-- /wiki-source -->
