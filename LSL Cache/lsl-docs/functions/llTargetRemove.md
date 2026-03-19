---
name: "llTargetRemove"
category: "function"
type: "function"
language: "LSL"
description: "Removes positional target handle registered with llTarget"
signature: "void llTargetRemove(integer number)"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llTargetRemove'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["lltargetremove"]
---

Removes positional target handle registered with llTarget


## Signature

```lsl
void llTargetRemove(integer number);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `integer (handle)` | `handle` | handle to control at_target and not_at_target events |


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llTargetRemove)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llTargetRemove) — scraped 2026-03-18_

Removes positional target handle registered with llTarget

## Examples

```lsl
integer target_id;
vector target_pos;

default
{
    state_entry()
    {
        target_pos = llGetPos() + <1.0, 0.0, 0.0>;
        target_id = llTarget(target_pos, 0.5);
    }
    at_target(integer tnum, vector targetpos, vector ourpos)
    {
        if (tnum == target_id)
        {
            llOwnerSay("object is within range of target");
            llOwnerSay("target position: " + (string)targetpos + ", object is now at: " + (string)ourpos);
            llOwnerSay("this is " + (string)llVecDist(targetpos, ourpos) + " meters from the target");
            llTargetRemove(target_id);
        }
    }
    not_at_target()
    {
        llOwnerSay(
            "not there yet - object is at " + (string)llGetPos() +
            ", which is " + (string)llVecDist(target_pos, llGetPos()) +
            " meters from the target (" + (string)target_pos + ")"
        );
    }
}
```

## See Also

### Events

- at_target
- not_at_target

### Functions

- llTarget
- llRotTarget
- llRotTargetRemove

<!-- /wiki-source -->
