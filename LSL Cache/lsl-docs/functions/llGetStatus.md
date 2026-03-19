---
name: "llGetStatus"
category: "function"
type: "function"
language: "LSL"
description: "Returns a boolean (an integer) equal to the status of the object."
signature: "integer llGetStatus(integer status)"
return_type: "integer"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetStatus'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgetstatus"]
---

Returns a boolean (an integer) equal to the status of the object.


## Signature

```lsl
integer llGetStatus(integer status);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `integer (status)` | `status` | A single STATUS_* flag |


## Return Value

Returns `integer`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetStatus)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetStatus) — scraped 2026-03-18_

Returns a boolean (an integer) equal to the status of the object.

## Caveats

- Status is an object attribute; all prims in an object share the same status.

  - STATUS_BLOCK_GRAB only really deals with the root prim. Try STATUS_BLOCK_GRAB_OBJECT instead.
- Querying for STATUS_CAST_SHADOWS always returns FALSE regardless of the setting.
- Only one flag should be specified at a time. As of Second Life Server 2022-09-09.574921, if more than one flag is specified, STATUS_DIE_AT_NO_ENTRY takes priority, followed by STATUS_BLOCK_GRAB_OBJECT, STATUS_DIE_AT_EDGE, STATUS_RETURN_AT_EDGE, STATUS_BLOCK_GRAB, STATUS_SANDBOX, STATUS_ROTATE_Z, STATUS_ROTATE_Y, STATUS_ROTATE_X, STATUS_PHANTOM, and STATUS_PHYSICS.

## Examples

```lsl
default
{
    touch_start(integer total_number)
    {
        if (llGetStatus(STATUS_PHYSICS))
        {
            llSay(0, "This object is physical");
        }
        else
        {
            llSay(0, "This object is not physical");
        }
    }
}
```

## See Also

### Functions

- **llSetStatus** — Sets the object status.

<!-- /wiki-source -->
