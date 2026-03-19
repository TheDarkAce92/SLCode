---
name: "llRemoteDataReply"
category: "example"
type: "example"
language: "LSL"
description: "Send an XML-RPC reply on channel to message_id with payload of string sdata and integer idata"
wiki_url: "https://wiki.secondlife.com/wiki/LlRemoteDataReply"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

/LSL


RemoteDataReplyllRemoteDataReply

***Deprecated** (This function has been deprecated, please use LSL_http_server instead.)* - 1 Summary - 2 Caveats - 3 Examples - 4 See Also - 4.1 Events - 5 Deep Notes - 5.1 Signature ## Summary Function:  **llRemoteDataReply**( key channel, key message_id, string sdata, integer idata );

3.0

Forced Delay

10.0

Energy

Send an XML-RPC reply on channel to message_id with payload of string sdata and integer idata

• key

channel

• key

message_id

• string

sdata

• integer

idata

## Caveats

- This function causes the script to sleep for 3.0 seconds.
- This function has been deprecated, please use LSL_http_server instead.

## Examples

## See Also

### Events

•

remote_data

## Deep Notes

#### Signature

```lsl
function void llRemoteDataReply( key channel, key message_id, string sdata, integer idata );
```