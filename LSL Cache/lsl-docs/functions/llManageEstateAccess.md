---
name: "llManageEstateAccess"
category: "function"
type: "function"
language: "LSL"
description: 'Use to add or remove agents from the estate's agent access or ban lists or groups from the estate's group access list.Returns a boolean (an integer) TRUE if the call was successful; FALSE if throttled, invalid action, invalid or null id or object owner is not allowed to manage the estate.

Only work'
signature: "integer llManageEstateAccess(integer action, key id)"
return_type: "integer"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llManageEstateAccess'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llmanageestateaccess"]
---

Use to add or remove agents from the estate's agent access or ban lists or groups from the estate's group access list.Returns a boolean (an integer) TRUE if the call was successful; FALSE if throttled, invalid action, invalid or null id or object owner is not allowed to manage the estate.

Only works for objects owned by the Estate Owner or an Estate Manager. By default, the object owner is notified of every change made using this function.  But if the owner grants PERMISSION_SILENT_ESTATE_MANAGEMENT to the script, the owner will not be notified.


## Signature

```lsl
integer llManageEstateAccess(integer action, key id);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `integer` | `action` | ESTATE_ACCESS_* flag |
| `key` | `avatar` | avatar or group UUID |


## Return Value

Returns `integer`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llManageEstateAccess)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llManageEstateAccess) — scraped 2026-03-18_

Use to add or remove agents from the estate's agent access or ban lists or groups from the estate's group access list.Returns a boolean (an integer) TRUE if the call was successful; FALSE if throttled, invalid action, invalid or null id or object owner is not allowed to manage the estate.

## Caveats

- Calls are throttled at a rate of 30 calls per 30 seconds.
- FALSE will be returned...

  - if throttled,
  - if object owner doesn't have power to perform action,
  - if avatar is invalid or null
- If used on mainland the message "llManageEstateAccess does not work on mainland" is shouted on DEBUG_CHANNEL.
- If the object owner is not allowed to manage the estate the message "llManageEstateAccess object owner must manage estate." is shouted on DEBUG_CHANNEL. -- [SRC-233](https://jira.secondlife.com/browse/SRC-233)
- If a legit estate manager tries to exceed the max number of entries in the list the call will return TRUE but the operation be truncated at the limit.

## See Also

### Functions

- llAddToLandPassList
- llAddToLandBanList
- llRemoveFromLandBanList
- llRemoveFromLandPassList
- llResetLandBanList
- llResetLandPassList

<!-- /wiki-source -->
