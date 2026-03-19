---
name: "linkset_data"
category: "event"
type: "event"
language: "LSL"
description: "The linkset_data event fires in all scripts in a linkset whenever the datastore has been modified through a call to one of the llLinksetData functions."
signature: "linkset_data(integer action, string name, string value)"
wiki_url: 'https://wiki.secondlife.com/wiki/linkset_data'
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
deprecated: "false"
parameters: []
---

The linkset_data event fires in all scripts in a linkset whenever the datastore has been modified through a call to one of the llLinksetData functions.


## Signature

```lsl
linkset_data(integer action, string name, string value)
{
    // your code here
}
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `integer` | `action` | Action taken on the linkset Datastore |
| `string` | `name` | The key of the name:value pair. |
| `string` | `value` | The new value of the pair. Empty string if pair was deleted or is password-protected (see llLinksetDataWriteProtected). |


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/linkset_data)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/linkset_data) — scraped 2026-03-18_

## Examples

```lsl
default
{
    linkset_data(integer action, string name, string value)
    {
        if (action == LINKSETDATA_RESET)
        {
            llOwnerSay("Link set datastore has been cleared.");
            // name and value will both be empty strings, ""
        }
        else if (action == LINKSETDATA_DELETE)
        {
            llOwnerSay("Link set datastore key \"" + name + "\" has been deleted.");
            // value is an empty string, ""
        }
        else if (action == LINKSETDATA_UPDATE)
        {
            llOwnerSay("Link set datastore key \"" + name + "\" = \"" + value + "\".");
        }
    }
}
```

## See Also

### Functions

- llLinksetDataDelete
- llLinksetDataReset
- llLinksetDataWrite
- llLinksetDataWriteProtected

<!-- /wiki-source -->
