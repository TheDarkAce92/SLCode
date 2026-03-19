---
name: "llName2Key"
category: "function"
type: "function"
language: "LSL"
description: "Returns a key the Agent ID for the named agent in the region. If there is no agent with the specified name currently signed onto the region, this function returns the value NULL_KEY. Names are always provided in the form 'First[ Last]' or 'first[.last]' (first name with an optional last name.) If th"
signature: "key llName2Key(string name)"
return_type: "key"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llName2Key'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
---

Returns a key the Agent ID for the named agent in the region. If there is no agent with the specified name currently signed onto the region, this function returns the value NULL_KEY. Names are always provided in the form "First[ Last]" or "first[.last]" (first name with an optional last name.) If the last name is omitted a last name of "Resident" is assumed. Case is not considered when resolving agent names.


## Signature

```lsl
key llName2Key(string name);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `string` | `name` | Name of the avatar to retrieve the UUID of. |


## Return Value

Returns `key`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llName2Key)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llName2Key) — scraped 2026-03-18_

Returns a key the Agent ID for the named agent in the region. If there is no agent with the specified name currently signed onto the region, this function returns the value NULL_KEY. Names are always provided in the form "First[ Last]" or "first[.last]" (first name with an optional last name.) If the last name is omitted a last name of "Resident" is assumed. Case is not considered when resolving agent names.

## Caveats

- This function does not operate on historical names. For historical name lookup use llRequestUserKey.

## Examples

```lsl
tellName2Key(string avatarName)
{
    key keyFromName = llName2Key(avatarName);
    if (keyFromName == NULL_KEY)
    {
        llSay(0, "There is no agent with the name '" + avatarName + "' currently signed onto the region.");
        return;
    }
    llSay(0, "Avatar key for name '" + avatarName + "': " + (string)keyFromName);
}

default
{
    touch_start(integer total_number)
    {
        tellName2Key("rider.linden");
        tellName2Key("Rider Linden");
        tellName2Key(llDetectedName(0));
    }
}
// If Rider Linden touches the object, the three lines should contain the answer c5a07167-9bbe-4944-a7b0-a9677afa134d
```

## See Also

### Functions

- **llRequestUserKey** — to fetch avatar UUID by current or historical username.

<!-- /wiki-source -->
