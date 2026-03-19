---
name: "llGetObjectName"
category: "function"
type: "function"
language: "LSL"
description: "Returns a string that is the name of the ''prim'' the script is attached to."
signature: "string llGetObjectName()"
return_type: "string"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetObjectName'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgetobjectname"]
---

Returns a string that is the name of the ''prim'' the script is attached to.


## Signature

```lsl
string llGetObjectName();
```


## Return Value

Returns `string`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetObjectName)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetObjectName) — scraped 2026-03-18_

Returns a string that is the name of the prim the script is attached to.

## Caveats

- The prim name is limited to 63 bytes, any string longer than that will be truncated. This truncation does not always happen when the attribute is set or read.
- This function may return "(Waiting)" sometimes. See: #Notes

## Examples

| Get this prim's name | Get the root prim's name |
| --- | --- |
| ```lsl default { state_entry() { // PUBLIC_CHANNEL has the integer value 0 llSay(PUBLIC_CHANNEL, "This prim's name: " + llGetObjectName() ); } } ``` | ```lsl default { state_entry() { // PUBLIC_CHANNEL has the integer value 0 llSay(PUBLIC_CHANNEL, "Root prim's name: " + llGetLinkName(LINK_ROOT)); } } ``` |

## Notes

#### Erroneous "(Waiting)"

Presumably the function queries the asset server for a predetermined time and returns "(Waiting)" if that elapses.
It then silently proceeds to the next instruction.
A work around therefore, might be to test object name is not "(Waiting)" after calling llGetObjectName.

## See Also

### Functions

- **llSetObjectName** — Set the prims name
- **llGetLinkName** — Get a linked prims name
- **llGetObjectDesc** — Get the prims description
- **llSetObjectDesc** — Sets the prims description
- llGetObjectDetails

### Articles

- **Limits** — SL limits and constrictions
- Prim Attribute Overloading

<!-- /wiki-source -->
