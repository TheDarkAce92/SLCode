---
name: "llSetStatus"
category: "function"
type: "function"
language: "LSL"
description: "Sets the object status attributes indicated in the status} mask to value"
signature: "void llSetStatus(integer status, integer value)"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llSetStatus'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llsetstatus"]
---

Sets the object status attributes indicated in the status} mask to value


## Signature

```lsl
void llSetStatus(integer status, integer value);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `integer (status)` | `status` | bit mask, STATUS_* flags |
| `integer` | `value` | boolean, TRUE enables, FALSE disables |


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llSetStatus)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llSetStatus) — scraped 2026-03-18_

Sets the object status attributes indicated in the status} mask to value

## Caveats

- Status is an object attribute; all prims in an object share the same status.

  - Except for STATUS_BLOCK_GRAB, this only affects the prim the script is in, child prims in linked objects will not be affected.

  - Use STATUS_BLOCK_GRAB_OBJECT to block grabbing of a link_set.
- Setting STATUS_PHYSICS fails silently in attached objects. ~ #SVC-6549
- The STATUS_ROTATE_X, STATUS_ROTATE_Y and STATUS_ROTATE_Z flags all require that the object first be made physical to have any effect.

## Examples

```lsl
default
{
    state_entry()
    {
        llSetStatus( STATUS_DIE_AT_EDGE | STATUS_PHYSICS, TRUE);
        llSetStatus( STATUS_ROTATE_X | STATUS_ROTATE_Y, FALSE);
    }
}
```

## See Also

### Functions

- **llGetStatus** — Gets the object status.

<!-- /wiki-source -->
