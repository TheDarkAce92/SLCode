---
name: "llGetObjectDesc"
category: "function"
type: "function"
language: "LSL"
description: 'Returns a string containing the description of the prim the script is attached to.

To get the ''object's'' description (not the current prim's), use PRIM_DESC or OBJECT_DESC.'
signature: "string llGetObjectDesc()"
return_type: "string"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetObjectDesc'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgetobjectdesc"]
---

Returns a string containing the description of the prim the script is attached to.

To get the ''object's'' description (not the current prim's), use PRIM_DESC or OBJECT_DESC.


## Signature

```lsl
string llGetObjectDesc();
```


## Return Value

Returns `string`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetObjectDesc)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetObjectDesc) — scraped 2026-03-18_

Returns a string containing the description of the prim the script is attached to.

## Caveats

- The prim description is limited to 127 bytes; any string longer then that will be truncated. This truncation does not always happen when the attribute is set or read.
- The prim description may only contain printable ASCII characters (code points 32-126), except the pipe character '|', which is not permitted for historical reasons. All other characters will be replaced with one '?' character per illegal UTF-8 byte.
- Note that when people have "Hover Tips on All Objects" selected in the viewer's "View" menu, they'll see the object description pop-up for any object under their mouse pointer.  For that reason, it is good practice to only set human-friendly information in the description, e.g. keys and such.
- When an attached object is detached, changes made by script to the name and description (of the root prim) of the attachment will be lost. While the object is attached the name and description can be changed but it will not be reflected in inventory. This caveat does *not* apply to child prims.
|  | Important: This function does not get the description of the object's rootprim, but the description of the prim containing the script. Please use llList2String(llGetLinkPrimitiveParams(LINK_ROOT, [ PRIM_DESC ]), 0); instead. |
| --- | --- |

## Examples

| Get this prim's description |
| --- |
| ```lsl default { state_entry() { // PUBLIC_CHANNEL has the integer value 0 llSay(PUBLIC_CHANNEL, "This prim's description: " + llGetObjectDesc() ); } } ``` |

| Get the root prim's description |
| --- |
| ```lsl default { state_entry() { // PUBLIC_CHANNEL has the integer value 0 llSay(PUBLIC_CHANNEL, "Rootprim's description: " + llList2String(llGetLinkPrimitiveParams(LINK_ROOT, [ PRIM_DESC ]), 0)); } } ``` |

## See Also

### Functions

- **llSetObjectDesc** — Sets the prim description.
- **llGetObjectName** — Gets the prim name.
- **llSetObjectName** — Sets the prim name.
- llGetObjectDetails

### Articles

- **Limits** — SL limits and constrictions
- Prim Attribute Overloading

<!-- /wiki-source -->
