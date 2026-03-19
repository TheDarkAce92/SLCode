---
name: "llSetObjectPermMask"
category: "function"
type: "function"
language: "LSL"
description: "Sets the given permission mask to the new value on the root object the task is attached to."
signature: "void llSetObjectPermMask(integer mask, integer value)"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llSetObjectPermMask'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
flags: "god-mode"
---

Sets the given permission mask to the new value on the root object the task is attached to.


## Signature

```lsl
void llSetObjectPermMask(integer mask, integer value);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `integer` | `mask` | MASK_* flag |
| `integer` | `value` | bit-field, PERM_* flags |


## Caveats

- Energy cost: **10.0**.
- Available to **god-mode** (Linden Lab internal) only.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llSetObjectPermMask)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llSetObjectPermMask) — scraped 2026-03-18_

Sets the given permission mask to the new value on the root object the task is attached to.

## Caveats

- This function can only be executed in God Mode.

## See Also

### Functions

- llGetObjectPermMask

<!-- /wiki-source -->
