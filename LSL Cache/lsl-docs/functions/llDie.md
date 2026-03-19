---
name: "llDie"
category: "function"
type: "function"
language: "LSL"
description: 'Deletes the object. The object does not go to the owners Inventory:Trash.

If called in any prim in the link set the result will be the deletion of the entire object.
To remove a single prim from an object use llBreakLink first.'
signature: "void llDie()"
return_type: "void"
sleep_time: ""
energy_cost: ""
wiki_url: 'https://wiki.secondlife.com/wiki/llDie'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["lldie"]
---

Deletes the object. The object does not go to the owners Inventory:Trash.

If called in any prim in the link set the result will be the deletion of the entire object.
To remove a single prim from an object use llBreakLink first.


## Signature

```lsl
void llDie();
```


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llDie)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llDie) — scraped 2026-03-18_

Deletes the object. The object does not go to the owner's Inventory 🗑 Trash.

## Caveats

- The script may not stop executing immediately after this function is called ([SVC-7421](https://jira.secondlife.com/browse/SVC-7421)).
- After this function is called, there is no way to undo the deletion of the object.
- Has no effect if called from within an attachment; there is no way to delete an attachment.

  - To detach an object from the avatar, call llDetachFromAvatar.
  - Detaching a temporary attachment will cause the attachment to be deleted.

## See Also

### Functions

- llDetachFromAvatar
- llBreakLink

### Articles

- Attachment

<!-- /wiki-source -->
