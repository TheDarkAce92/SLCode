---
name: "llGetAnimationList"
category: "function"
type: "function"
language: "LSL"
description: "Returns a list of keys of playing animations for avatar."
signature: "list llGetAnimationList(key id)"
return_type: "list"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llGetAnimationList'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llgetanimationlist"]
---

Returns a list of keys of playing animations for avatar.


## Signature

```lsl
list llGetAnimationList(key id);
```


## Parameters


| Type | Name | Description |
|------|------|-------------|
| `key` | `avatar` | avatar UUID that is in the same region |


## Return Value

Returns `list`.


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llGetAnimationList)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llGetAnimationList) — scraped 2026-03-18_

Returns a list of keys of playing animations for avatar.

## Caveats

- There is no internal mechanism to get the name of the animations playing.
- Standard animations can be started and stopped by scripts, so the list returned may not accurately reflect the avatar's state. Use llGetAgentInfo and llGetAnimation when this matters.
- Some motions are local to the viewer and cannot be detected by scripts.
- Animations that are triggered by other animations are local to the viewer and cannot be detected by scripts.

## Examples

This example is a bit involved but there aren't many applications for this function.

```lsl
//Simple Animation Override for Walk
key old_anim = "6ed24bd8-91aa-4b12-ccc7-c97c857ab4e0";
string new_anim="yoga_float";
integer status;
list check;
key owner;

default
{
    state_entry()
    {
        owner = llGetOwner();
        llRequestPermissions(owner, PERMISSION_TRIGGER_ANIMATION);
        check = [old_anim];
    }

    run_time_permissions(integer p)
    {
        if(p & PERMISSION_TRIGGER_ANIMATION)
        {
            llSetTimerEvent(0.2);
        }
    }

    timer()
    {
        if(llGetAgentInfo(owner) & AGENT_WALKING)
        {
            list anims = llGetAnimationList(owner);
            if(~llListFindList(anims, check))
            {
                status = 1;
                llStartAnimation(new_anim);
                llStopAnimation(old_anim);
            }
        }
        else if(status)
        {
            llStopAnimation(new_anim);
            status = 0;
        }
    }

    on_rez(integer p)
    {
        llResetScript();
    }
}
```

## See Also

### Functions

- **llGetAgentInfo** — Gets the avatar info
- **llGetAnimation** — Get the avatar's base animation state
- **llStartAnimation** — Start an animation on an avatar
- **llStopAnimation** — Stop an animation playing on an avatar

<!-- /wiki-source -->
