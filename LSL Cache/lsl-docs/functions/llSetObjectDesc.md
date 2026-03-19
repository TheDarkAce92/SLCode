---
name: "llSetObjectDesc"
category: "function"
type: "function"
language: "LSL"
description: "Sets the prims description"
signature: "void llSetObjectDesc(string desc)"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llSetObjectDesc'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llsetobjectdesc"]
---

Sets the prims description


## Signature

```lsl
void llSetObjectDesc(string desc);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `string` | `description` |  |


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llSetObjectDesc)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llSetObjectDesc) — scraped 2026-03-18_

Sets the prims description

## Caveats

- The prim description is limited to 127 bytes; any string longer then that will be truncated. This truncation does not always happen when the attribute is set or read.
- The prim description may only contain printable ASCII characters (code points 32-126), except the pipe character '|', which is not permitted for historical reasons. All other characters will be replaced with one '?' character per illegal UTF-8 byte.
- Note that when people have "Hover Tips on All Objects" selected in the viewer's "View" menu, they'll see the object description pop-up for any object under their mouse pointer.  For that reason, it is good practice to only set human-friendly information in the description, e.g. keys and such.
- When an attached object is detached, changes made by script to the name and description (of the root prim) of the attachment will be lost. While the object is attached the name and description can be changed but it will not be reflected in inventory. This caveat does *not* apply to child prims.
- Changing the object description does not trigger a changed event.

## Examples

| Set this prim's description | Set the root prim's description |
| --- | --- |
| ```lsl default { state_entry() { llSetObjectDesc("NEW PRIM DESCRIPTION"); } } ``` | ```lsl default { state_entry() { llSetLinkPrimitiveParamsFast(LINK_ROOT, [PRIM_DESC, "NEW ROOT PRIM DESCRIPTION"]); } } ``` |

## Notes

- Object descriptions are often used to store data that needs to be protected from script resets (see, for example, Prim Attribute Overloading). However, descriptions are not immutable and can be tampered with by users or other scripts, either intentionally or accidentally, so this method should only be considered a last resort for data storage.

  - llLinksetDataWrite and associated functions are generally better suited for this purpose, because they allow for significantly more data storage and are much more secure against tampering.

## See Also

### Functions

- **llGetObjectDesc** — Gets the prim description.
- **llGetObjectName** — Gets the prim name.
- **llSetObjectName** — Sets the prim name.

### Articles

- **Limits** — SL limits and constrictions

<!-- /wiki-source -->
