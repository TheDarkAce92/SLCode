---
name: "llCloseRemoteDataChannel"
category: "function"
type: "function"
language: "LSL"
description: "Closes XML-RPC channel."
signature: "void llCloseRemoteDataChannel(key channel)"
return_type: "void"
sleep_time: "1.0"
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llCloseRemoteDataChannel'
deprecated: "true"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llcloseremotedatachannel"]
---

Closes XML-RPC channel.


## Signature

```lsl
void llCloseRemoteDataChannel(key channel);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `key` | `channel` |  |


## Caveats

- Forced delay: **1.0 seconds** — the script sleeps after each call.
- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llCloseRemoteDataChannel)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llCloseRemoteDataChannel) — scraped 2026-03-18_

Closes XML-RPC channel.

## Caveats

- This function causes the script to sleep for 1.0 seconds.
- This function has been deprecated, please use LSL_http_server instead.

<!-- /wiki-source -->
