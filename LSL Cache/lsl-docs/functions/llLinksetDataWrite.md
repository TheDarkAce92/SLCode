---
name: "llLinksetDataWrite"
category: "function"
type: "function"
language: "LSL"
description: 'Creates or updates an unprotected name:value pair from the linkset's datastore.

When these functions are called, the linkset_data event is triggered in all scripts running in the linkset with an action of LINKSETDATA_UPDATE, or LINKSETDATA_DELETE if the pair is deleted.

The linkset datastore can c'
signature: "integer llLinksetDataWrite(string key, string value)"
return_type: "integer"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llLinksetDataWrite'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
---

Creates or updates an unprotected name:value pair from the linkset's datastore.

When these functions are called, the linkset_data event is triggered in all scripts running in the linkset with an action of LINKSETDATA_UPDATE, or LINKSETDATA_DELETE if the pair is deleted.

The linkset datastore can contain up to 131072 bytes (128 KiB) of data and has no impact on script memory usage aside from the functions and events used to interact with it. Every pair written to the datastore consumes a number of bytes in the datastore equal to the length of name plus the length of value, plus an additional 32 bytes if written using llLinksetDataWriteProtected.

This function returns 0 on success or an error code on failure.


## Signature

```lsl
integer llLinksetDataWrite(string key, string value);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `string` | `name` | The key of the name:value pair in the datastore to be updated or created. |
| `string` | `value` | The value of the name:value pair. |
| `string` | `pass` | A pass phrase used to protect the name:value pair. |


## Return Value

Returns `integer`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llLinksetDataWrite)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llLinksetDataWrite) — scraped 2026-03-18_

Creates or updates an unprotected name:value pair from the linkset's datastore.Returns an integer success or failure code.

## Caveats

- Events are only fired if the linkset's datastore is changed.

  - Rewriting an existing value to a **name:value** pair returns LINKSETDATA_NOUPDATE.
  - Writing an empty string to a nonexistent name in the datastore returns LINKSETDATA_NOTFOUND.
- There is currently no way to write to or read from a linkset datastore from another linkset.
- The datastore is accessible from the entire linkset but acts as a property of the root prim alone. Therefore, linking and unlinking prims produces the following results:

  - When linking one linkset to another linkset, the combined linkset datastore includes all pairs from both datastores.

  - If any pairs have conflicting names, the combined linkset datastore will keep the pair from the original linkset and will silently drop conflicting pairs from newly added prim(s).
  - If the combined linkset datastore would exceed 131072 bytes, pairs from the newly linked prim(s) will be added to the combined linkset datastore up to the limit. It is not currently clear in what order pairs are added, so there is no way to predict which will be dropped.
  - When unlinking a child prim from a linkset, the datastore remains in the original linkset and the child prim (now its own root prim) has an empty datastore.

  - If the datastore is too large to cache in a script to be rewritten after unlinking, you may need to devise a custom method of porting the datastore from the original linkset to the child prim, if necessary.
  - When unlinking a root prim from a linkset, the datastore remains in the newly-unlinked root prim and the remaining prims in the original linkset have an empty datastore.
- There is no limit on the size of value aside from the total datastore limit, so care should be taken when writing very large values that could crash other scripts in the linkset via linkset_data.

  - If a script does not define a linkset_data event, it will not load any event parameters into its memory when the datastore is written to, so the script should not crash from another script in the linkset writing to the datastore.
  - If this is a possible risk, consider using **llLinksetDataWriteProtected**, which does not send value in linkset_data, with a static pass.
- It is possible for data to be rolled back to a previous state if the datastore is stored in an object that is restored via a simulator rollback, or in an attachment that is not properly saved back to the server on logout.

  - Viewer crashes can cause attachment states to not be saved, so care should be taken when using these functions in attachments, because datastore rollbacks are likely to occur on occasion for attachments.

## Examples

```lsl
default
{
    touch_start(integer num_detected)
    {
        llLinksetDataWrite("test-name", "See you on the other side!");
        llResetScript();
    }
    state_entry()
    {
        llOwnerSay(llLinksetDataRead("test-name")); // Should print "See you on the other side!" to the owner
    }
}
```

## Notes

- Linkset datastore operations are synchronous and are usually processed within one server frame. Therefore, it is possible to synchronize variables between multiple scripts using the datastore alone without resorting to llMessageLinked, or to use the datastore directly as extended memory for specific workloads that need to work with extremely large datasets.

## See Also

### Events

- linkset_data

### Functions

- llLinksetDataAvailable
- llLinksetDataCountKeys
- llLinksetDataDelete
- llLinksetDataDeleteProtected
- llLinksetDataDeleteFound
- llLinksetDataFindKeys
- llLinksetDataListKeys
- llLinksetDataRead
- llLinksetDataReadProtected
- llLinksetDataReset

<!-- /wiki-source -->
