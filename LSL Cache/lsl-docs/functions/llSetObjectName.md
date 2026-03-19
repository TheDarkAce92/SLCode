---
name: "llSetObjectName"
category: "function"
type: "function"
language: "LSL"
description: 'Sets the prim's name according to the name parameter.

If this function is called from a child prim in a linked set, it will change the name of the child prim and not the root prim.'
signature: "void llSetObjectName(string name)"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llSetObjectName'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llsetobjectname"]
---

Sets the prim's name according to the name parameter.

If this function is called from a child prim in a linked set, it will change the name of the child prim and not the root prim.


## Signature

```lsl
void llSetObjectName(string name);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `string` | `name` |  |


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llSetObjectName)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llSetObjectName) — scraped 2026-03-18_

Sets the prim's name according to the name parameter.

## Caveats

- The name is limited to 63 characters. Longer prim names are cut short.
- Names can only consist of the 95 printable characters found in the [ASCII-7](http://en.wikipedia.org/wiki/ASCII#ASCII_printable_characters) (non-extended) character set, with the exception of the vertical bar/pipe ("|") character.

  - Invalid characters in the range 1 to 31, as well as the pipe character (124) are replaced with a question mark ("?").
  - Other invalid characters in the range 128 and above are replaced with two or more question marks, depending on how many bytes their UTF-8 representation requires.
  - Objects with all-whitespace names (e.g., a space or a series of spaces) will appear as "(Unnamed)" if they emit chat via llSay, llOwnerSay, llInstantMessage, etc., although this behaviour may vary in third-party viewers.
- While an object is attached, the script cannot change the name of the object as it appears in the user's inventory.

  - Changes to the name of the root prim (with llSetObjectName for example) will not be saved to inventory; when the attachment is detached (to inventory, not dropped) this name change is discarded and the name in inventory is used instead.
  - When attachment is dropped (to the ground) and taking it into inventory, the inventory item will have the new name (not the old).
- Changes to the names of child prims will be saved back to inventory when the object is detached to inventory. They survive detachment.
- Changes to the object name do not trigger a changed event.

## Examples

| Set this prim's name | Set the root prim's name |
| --- | --- |
| ```lsl default { state_entry() { llSetObjectName("NEW PRIM NAME"); } } ``` | ```lsl default { state_entry() { llSetLinkPrimitiveParamsFast(LINK_ROOT, [PRIM_NAME, "NEW ROOT PRIM NAME"]); } } ``` |
| Test if a string is valid as an object name |  |
| ```lsl // Returns TRUE if 'name' is a valid object name, FALSE otherwise integer isValidObjectName(string name) { string original_name = llGetObjectName(); llSetObjectName(name); integer valid_name = llGetObjectName() == name; llSetObjectName(original_name); return valid_name; } ``` |  |

## See Also

### Functions

- **llGetObjectName** — Get the prims name
- **llGetLinkName** — Get a linked prims name
- **llGetObjectDesc** — Get the prims description
- **llSetObjectDesc** — Set the prims description
- **llGetObjectDetails** — Get a list of object details

### Articles

- **Limits** — SL limits and constrictions

<!-- /wiki-source -->
