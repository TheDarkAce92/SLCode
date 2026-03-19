---
name: "llSetForce"
category: "function"
type: "function"
language: "LSL"
description: 'Applies force to the object (if the object is physical)

Continuous force. llApplyImpulse has instantaneous push.'
signature: "void llSetForce(vector force, integer local)"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llSetForce'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llsetforce"]
---

Applies force to the object (if the object is physical)

Continuous force. llApplyImpulse has instantaneous push.


## Signature

```lsl
void llSetForce(vector force, integer local);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `vector` | `force` | directional force |
| `integer (boolean)` | `local` | boolean, if TRUE force is treated as a local directional vector, if FALSE force is treated as a region directional vector |


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llSetForce)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llSetForce) — scraped 2026-03-18_

Applies force to the object (if the object is physical)

## Caveats

- Only works in  physics-enabled objects.Only works on physical objects and attachments (non-physical as well as physical).  Used on an attachment, it will apply the force to the avatar.

## Examples

```lsl
//A simple rocket script. Launches object up when touched.
//Sit on it for an interesting ride!
default
{
    touch_start(integer i)
    {
        llSetStatus(STATUS_PHYSICS, TRUE);
        llSetForce(<0,0,0x7FFFFFFF>, 0);  //FLY!
    }
}
```

## See Also

### Functions

- llSetForceAndTorque
- llSetTorque
- **llApplyImpulse** — Instantaneous force

<!-- /wiki-source -->
