---
name: "llGetKey"
category: "function"
type: "function"
language: "LSL"
description: "Returns the UUID of the prim containing the script"
wiki_url: "https://wiki.secondlife.com/wiki/llGetKey"
first_fetched: "2026-03-09"
last_updated: "2026-03-09"
signature: "key llGetKey()"
parameters: []
return_type: "key"
energy_cost: "0.0"
sleep_time: "0.0"
patterns: ["llgetkey"]
deprecated: "false"
---

# llGetKey

```lsl
key llGetKey()
```

Returns the UUID of the prim in which this script is running.

## Return Value

`key` — UUID of the prim containing the script.

## Example

```lsl
default
{
    state_entry()
    {
        llOwnerSay("This prim's key: " + (string)llGetKey());
        // Both lines return the same value:
        llOwnerSay((string)llGetKey());
        llOwnerSay((string)llGetLinkKey(llGetLinkNumber()));
    }
}
```

## See Also

- `llGetOwner` — UUID of the object's owner
- `llGetLinkKey` — UUID of a specific linked prim by link number
- `llGetLinkNumber` — link number of the current prim
- `llGetObjectName` — name of the prim/object


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetKey) — scraped 2026-03-18_

Returns the key of the prim the script is in.

## Examples

```lsl
default
{
    state_entry()
    {
        llOwnerSay(llGetKey());
        llOwnerSay(llGetLinkKey(llGetLinkNumber()));
    }
}
```

## See Also

### Functions

- llGetLinkKey
- llGetLinkNumber

<!-- /wiki-source -->
