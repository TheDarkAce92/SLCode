---
name: "llLinksetDataListKeys"
category: "function"
type: "function"
language: "LSL"
description: "The llLinksetDataListKeys function returns a list of up to count keys in the datastore, starting at the one indicated by start. If count is less than 1, then all keys between start and the end are returned. If count minus start exceeds the total number of keys, the returned list will be shorter than"
signature: "list llLinksetDataListKeys(integer start, integer count)"
return_type: "list"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llLinksetDataListKeys'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
---

The llLinksetDataListKeys function returns a list of up to count keys in the datastore, starting at the one indicated by start. If count is less than 1, then all keys between start and the end are returned. If count minus start exceeds the total number of keys, the returned list will be shorter than count, down to a zero-length list if start equals or exceeds the total number of keys.

Returns a list of the keys in the datastore, ordered alphabetically.


## Signature

```lsl
list llLinksetDataListKeys(integer start, integer count);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `integer` | `start` | The first key to return. |
| `integer` | `count` | The number of keys to return. |


## Return Value

Returns `list`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llLinksetDataListKeys)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llLinksetDataListKeys) — scraped 2026-03-18_

The llLinksetDataListKeys function returns a list of up to count keys in the datastore, starting at the one indicated by start. If count is less than 1, then all keys between start and the end are returned. If count minus start exceeds the total number of keys, the returned list will be shorter than count, down to a zero-length list if start equals or exceeds the total number of keys.Returns a list of the keys in the datastore, ordered alphabetically.

## Examples

The following code will list all the keys in a object. Only 1024 characters will be displayed due to limitations of llSay.

```lsl
// Retrieving too many entries from LinksetData can trigger a stack or heap error if the number of entries exceeds the available memory.  Use with caution.

default
{
    state_entry()
    {
        llSay(0, llDumpList2String(llLinksetDataListKeys(0, 0), "\n"));
    }
}
```

## See Also

### Functions

- llLinksetDataAvailable
- llLinksetDataCountKeys
- llLinksetDataDelete
- llLinksetDataDeleteFound
- llLinksetDataFindKeys
- llLinksetDataRead
- llLinksetDataReset
- llLinksetDataWrite

<!-- /wiki-source -->
