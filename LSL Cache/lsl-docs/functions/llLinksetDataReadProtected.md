---
name: "llLinksetDataReadProtected"
category: "function"
type: "function"
language: "LSL"
description: 'Reads a protected name:value pair from the datastore.

Returns a string value corresponding to name

If name is not found return an empty string.'
signature: "string llLinksetDataReadProtected(string key, string password)"
return_type: "string"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llLinksetDataReadProtected'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
---

Reads a protected name:value pair from the datastore.

Returns a string value corresponding to name

If name is not found return an empty string.


## Signature

```lsl
string llLinksetDataReadProtected(string key, string password);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `string` | `name` | The key of the linkset name:value pair to be read. |
| `string` | `pass` | The pass phrase protecting the name:value pair. |


## Return Value

Returns `string`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llLinksetDataReadProtected)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llLinksetDataReadProtected) — scraped 2026-03-18_

Reads an unprotected name:value pair from the linkset's datastore.Returns a string value corresponding to name

## See Also

### Functions

- llLinksetDataAvailable
- llLinksetDataCountKeys
- llLinksetDataDelete
- llLinksetDataDeleteProtected
- llLinksetDataDeleteFound
- llLinksetDataFindKeys
- llLinksetDataListKeys
- llLinksetDataReset
- llLinksetDataWrite
- llLinksetDataWriteProtected

<!-- /wiki-source -->
