---
name: "llLinksetDataReset"
category: "function"
type: "function"
language: "LSL"
description: 'The llLinksetDataReset function erases all name:value pairs stored in the linkset's datastore. When this function is called the linkset_data event is triggered in all scripts running in the linkset with an action of LINKSETDATA_RESET.'
signature: "void llLinksetDataReset()"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llLinksetDataReset'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
---

The llLinksetDataReset function erases all name:value pairs stored in the linkset's datastore. When this function is called the linkset_data event is triggered in all scripts running in the linkset with an action of LINKSETDATA_RESET.


## Signature

```lsl
void llLinksetDataReset();
```


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llLinksetDataReset)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llLinksetDataReset) — scraped 2026-03-18_

The llLinksetDataReset function erases all name:value pairs stored in the linkset's datastore. When this function is called the linkset_data event is triggered in all scripts running in the linkset with an action of LINKSETDATA_RESET.

## Caveats

llLinksetDataReset removes all keys. Even those that were created by llLinksetDataWriteProtected.

## Examples

The following code will delete all the keys in a object.

```lsl
// Removes all the keys in linksetdata without a saving throw.
// Warning: This will delete in password protected keys and is irreversible.
// -- Madi Melodious --

default
{
    state_entry()
    {
       llLinksetDataReset();
    }
}
```

## See Also

### Events

- linkset_data

### Functions

- llLinksetDataAvailable
- llLinksetDataCountKeys
- llLinksetDataDelete
- llLinksetDataDeleteFound
- llLinksetDataFindKeys
- llLinksetDataListKeys
- llLinksetDataRead
- llLinksetDataWrite

<!-- /wiki-source -->
