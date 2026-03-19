---
name: "llApplyRotationalImpulse"
category: "function"
type: "function"
language: "LSL"
description: "Applies rotational impulse to object."
signature: "void llApplyRotationalImpulse(vector force, integer local)"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llApplyRotationalImpulse'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llapplyrotationalimpulse"]
---

Applies rotational impulse to object.


## Signature

```lsl
void llApplyRotationalImpulse(vector force, integer local);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `vector` | `force` |  |
| `integer (boolean)` | `local` | boolean, if TRUE force is treated as a local directional vector, if FALSE force is treated as a region directional vector |


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llApplyRotationalImpulse)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llApplyRotationalImpulse) — scraped 2026-03-18_

Applies rotational impulse to object.

## Caveats

- Only works in  physics-enabled objects.
- It does **not** work on attachments.

## Examples

```lsl
default
{
    state_entry()
    {
        llApplyRotationalImpulse(<0,5,0>,TRUE); //Rotates object.
    }
}
```

## See Also

### Functions

- llApplyImpulse
- llSetAngularVelocity

<!-- /wiki-source -->
